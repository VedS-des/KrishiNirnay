import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestKrishiNirnayBackend(unittest.TestCase):

    # 1. Root Endpoint Test (GET /)
    def test_root_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["status"], "online")
        self.assertIn("endpoints", json_data)

    # 2. Farm Registration with Valid Data (POST /farms)
    def test_create_farm_success(self):
        farm_payload = {
            "location": "Mandya, Karnataka",
            "latitude": 12.52,
            "longitude": 76.89,
            "area": 3.0,
            "soil_type": "Red Sandy Loam",
            "soil_ph": 6.5,
            "water_availability": "Medium",
            "budget": 30000.0,
            "season": "Kharif",
            "previous_crop": "Paddy"
        }
        response = client.post("/farms", json=farm_payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["status"], "success")
        self.assertEqual(json_data["data"]["location"], "Mandya, Karnataka")
        self.assertEqual(json_data["data"]["area"], 3.0)

    # 3. Farm Registration with Invalid Data (POST /farms)
    def test_create_farm_invalid_data(self):
        # Invalid farm payload with area <= 0, budget < 0, pH > 14
        invalid_payload = {
            "location": "Mandya, Karnataka",
            "area": 0.0,  # Invalid: must be > 0
            "soil_type": "Red Sandy Loam",
            "soil_ph": 15.0,  # Invalid: must be <= 14.0
            "water_availability": "Medium",
            "budget": -1000.0,  # Invalid: must be >= 0
            "season": "Kharif"
        }
        response = client.post("/farms", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

    # 4. Crop Recommendations with Valid Data (POST /recommend)
    def test_recommend_crops_success(self):
        payload = {
            "location": "Dharwad, Karnataka",
            "area": 2.5,
            "soil_type": "Red Sandy Loam",
            "soil_ph": 6.8,
            "water_availability": "Medium",
            "budget": 20000.0,
            "season": "Kharif",
            "previous_crop": "Maize"
        }
        response = client.post("/recommend", json=payload)
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["status"], "success")
        self.assertGreater(json_data["total_recommendations"], 0)
        self.assertIsInstance(json_data["recommendations"], list)
        
        top_crop = json_data["recommendations"][0]
        self.assertIn("crop", top_crop)
        self.assertIn("confidence_score", top_crop)
        self.assertIn("suitability", top_crop)
        self.assertIn("reason", top_crop)
        self.assertIn("estimated_duration_days", top_crop)

    # 5. Crop Recommendations Input Validation Failures
    def test_validation_invalid_area(self):
        invalid_payload = {
            "location": "Mandya",
            "area": 0.0,  # Invalid: must be > 0
            "soil_type": "Clay",
            "soil_ph": 6.5,
            "water_availability": "High",
            "budget": 10000.0,
            "season": "Kharif"
        }
        response = client.post("/recommend", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

    def test_validation_negative_budget(self):
        invalid_payload = {
            "location": "Mandya",
            "area": 2.0,
            "soil_type": "Clay",
            "soil_ph": 6.5,
            "water_availability": "High",
            "budget": -500.0,  # Invalid: must be >= 0
            "season": "Kharif"
        }
        response = client.post("/recommend", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

    def test_validation_out_of_range_ph(self):
        invalid_payload = {
            "location": "Mandya",
            "area": 2.0,
            "soil_type": "Clay",
            "soil_ph": 15.5,  # Invalid: pH > 14.0
            "water_availability": "High",
            "budget": 5000.0,
            "season": "Kharif"
        }
        response = client.post("/recommend", json=invalid_payload)
        self.assertEqual(response.status_code, 422)

    # 6. Crop Details (GET /crops/Groundnut and others)
    def test_get_crop_details_groundnut(self):
        response = client.get("/crops/Groundnut")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["crop"], "Groundnut")
        self.assertEqual(json_data["scientific_name"], "Arachis hypogaea")
        self.assertIsInstance(json_data["suitable_soil"], list)
        self.assertEqual(json_data["growing_duration_days"], 120)

    def test_get_crop_details_all_crops(self):
        crops = ["Groundnut", "Black Gram", "Sesame", "Rice", "Maize"]
        for crop in crops:
            response = client.get(f"/crops/{crop}")
            self.assertEqual(response.status_code, 200, f"Failed for crop {crop}")
            json_data = response.json()
            self.assertEqual(json_data["crop"].lower(), crop.lower())
            self.assertIn("scientific_name", json_data)
            self.assertIn("ideal_ph_range", json_data)
            self.assertIn("water_requirement", json_data)
            self.assertIsInstance(json_data["suitable_soil"], list)
            self.assertIsInstance(json_data["suitable_seasons"], list)
            self.assertGreater(json_data["growing_duration_days"], 0)

    def test_get_crop_details_case_insensitive(self):
        for name in ["groundnut", "GROUNDNUT", "rICe", "black gram"]:
            response = client.get(f"/crops/{name}")
            self.assertEqual(response.status_code, 200, f"Case insensitive lookup failed for {name}")

    def test_get_crop_details_unknown_crop_returns_404(self):
        response = client.get("/crops/UnknownCrop")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    # 7. Crop Plan (GET /crops/Groundnut/plan and others)
    def test_get_crop_plan_groundnut(self):
        response = client.get("/crops/Groundnut/plan")
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data["crop"], "Groundnut")
        self.assertIn("disclaimer", json_data)
        self.assertIn("stages", json_data)
        self.assertGreaterEqual(len(json_data["stages"]), 5)
        
        first_stage = json_data["stages"][0]
        self.assertIn("stage", first_stage)
        self.assertIn("time", first_stage)
        self.assertIn("guidance", first_stage)

    def test_get_crop_plans_all_crops(self):
        crops = ["Groundnut", "Black Gram", "Sesame", "Rice", "Maize"]
        for crop in crops:
            response = client.get(f"/crops/{crop}/plan")
            self.assertEqual(response.status_code, 200, f"Failed plan for crop {crop}")
            json_data = response.json()
            self.assertEqual(json_data["crop"].lower(), crop.lower())
            self.assertIn("disclaimer", json_data)
            self.assertIn("stages", json_data)
            self.assertGreaterEqual(len(json_data["stages"]), 5)

    def test_get_crop_plan_unknown_crop_returns_404(self):
        response = client.get("/crops/UnknownCrop/plan")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
