"""
tests/test_backend.py
---------------------
Integration tests for the KrishiNirnay backend.

Run all tests with:
    pytest tests/ -v

These tests use FastAPI's TestClient (backed by httpx) to call each endpoint
and verify the response format, status codes, and basic correctness.
"""

import pytest
from fastapi.testclient import TestClient

# Import the app from the backend root (run tests from the backend/ directory)
import sys
import os

# Ensure the backend root is on the path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


# ===========================================================================
# HEALTH CHECK
# ===========================================================================

class TestHealthCheck:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_returns_message(self):
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "KrishiNirnay Backend is running"


# ===========================================================================
# FARMS
# ===========================================================================

VALID_FARM = {
    "location": "Tamil Nadu",
    "latitude": 11.0168,
    "longitude": 76.9558,
    "area": 5.0,
    "soil_type": "red",
    "soil_ph": 6.8,
    "water_availability": "medium",
    "budget": 150000,
    "season": "kharif",
    "previous_crop": "groundnut",
}


class TestFarms:
    def test_post_farm_valid_data(self):
        response = client.post("/farms", json=VALID_FARM)
        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert "farm_data" in data
        assert data["farm_data"]["location"] == "Tamil Nadu"

    def test_post_farm_missing_location(self):
        bad = {**VALID_FARM, "location": ""}
        response = client.post("/farms", json=bad)
        assert response.status_code == 422

    def test_post_farm_negative_area(self):
        bad = {**VALID_FARM, "area": -1}
        response = client.post("/farms", json=bad)
        assert response.status_code == 422

    def test_post_farm_negative_budget(self):
        bad = {**VALID_FARM, "budget": -5000}
        response = client.post("/farms", json=bad)
        assert response.status_code == 422

    def test_post_farm_invalid_ph(self):
        bad = {**VALID_FARM, "soil_ph": 20.0}
        response = client.post("/farms", json=bad)
        assert response.status_code == 422

    def test_post_farm_invalid_season(self):
        bad = {**VALID_FARM, "season": "summer"}
        response = client.post("/farms", json=bad)
        assert response.status_code == 422

    def test_post_farm_invalid_water(self):
        bad = {**VALID_FARM, "water_availability": "very_high"}
        response = client.post("/farms", json=bad)
        assert response.status_code == 422


# ===========================================================================
# RECOMMENDATIONS
# ===========================================================================

VALID_RECOMMEND = {
    "location": "Tamil Nadu",
    "area": 5.0,
    "soil_type": "red",
    "soil_ph": 6.8,
    "water_availability": "medium",
    "budget": 150000,
    "season": "kharif",
}


class TestRecommendations:
    def test_post_recommend_returns_200(self):
        response = client.post("/recommend", json=VALID_RECOMMEND)
        assert response.status_code == 200

    def test_post_recommend_structure(self):
        response = client.post("/recommend", json=VALID_RECOMMEND)
        data = response.json()
        assert "location" in data
        assert "season" in data
        assert "recommendations" in data
        assert "disclaimer" in data
        assert isinstance(data["recommendations"], list)
        assert len(data["recommendations"]) > 0

    def test_post_recommend_each_item_structure(self):
        response = client.post("/recommend", json=VALID_RECOMMEND)
        data = response.json()
        for rec in data["recommendations"]:
            assert "crop" in rec
            assert "suitability_score" in rec
            assert "reason" in rec
            assert "estimated_yield_per_acre" in rec
            assert "estimated_cost_inr" in rec
            assert "estimated_revenue_inr" in rec
            assert "estimated_profit_inr" in rec
            assert "risk_level" in rec

    def test_post_recommend_score_range(self):
        response = client.post("/recommend", json=VALID_RECOMMEND)
        data = response.json()
        for rec in data["recommendations"]:
            assert 0 <= rec["suitability_score"] <= 100

    def test_post_recommend_sorted_by_score(self):
        response = client.post("/recommend", json=VALID_RECOMMEND)
        scores = [r["suitability_score"] for r in response.json()["recommendations"]]
        assert scores == sorted(scores, reverse=True)

    def test_post_recommend_disclaimer_present(self):
        response = client.post("/recommend", json=VALID_RECOMMEND)
        data = response.json()
        assert len(data["disclaimer"]) > 0


# ===========================================================================
# CROPS
# ===========================================================================

class TestCrops:
    def test_get_all_crops(self):
        response = client.get("/crops")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_crops_includes_groundnut(self):
        response = client.get("/crops")
        assert "Groundnut" in response.json()

    def test_get_crop_groundnut(self):
        response = client.get("/crops/Groundnut")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Groundnut"
        assert "scientific_name" in data
        assert "suitable_soils" in data
        assert "ideal_ph_min" in data
        assert "ideal_ph_max" in data
        assert "water_requirement" in data
        assert "suitable_seasons" in data
        assert "growing_duration_days" in data
        assert "notes" in data

    def test_get_crop_unknown_returns_404(self):
        response = client.get("/crops/UnknownCrop")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_get_crop_plan_groundnut(self):
        response = client.get("/crops/Groundnut/plan")
        assert response.status_code == 200
        data = response.json()
        assert data["crop"] == "Groundnut"
        assert "stages" in data
        assert isinstance(data["stages"], list)
        assert len(data["stages"]) > 0
        assert "disclaimer" in data

    def test_get_crop_plan_stage_structure(self):
        response = client.get("/crops/Groundnut/plan")
        data = response.json()
        for stage in data["stages"]:
            assert "stage" in stage
            assert "time" in stage
            assert "guidance" in stage

    def test_get_crop_plan_unknown_returns_404(self):
        response = client.get("/crops/UnknownCrop/plan")
        assert response.status_code == 404

    def test_get_all_supported_crops(self):
        """All supported crops must have both an info page and a plan page."""
        crops_response = client.get("/crops")
        for crop in crops_response.json():
            info_resp = client.get(f"/crops/{crop}")
            assert info_resp.status_code == 200, f"{crop} info returned {info_resp.status_code}"
            plan_resp = client.get(f"/crops/{crop}/plan")
            assert plan_resp.status_code == 200, f"{crop} plan returned {plan_resp.status_code}"


# ===========================================================================
# RISK ASSESSMENT
# ===========================================================================

VALID_RISK = {
    "crop": "Groundnut",
    "location": "Tamil Nadu",
    "soil_type": "red",
    "soil_ph": 6.8,
    "water_availability": "medium",
    "season": "kharif",
}


class TestRiskAssessment:
    def test_post_risk_assessment_returns_200(self):
        response = client.post("/risk-assessment", json=VALID_RISK)
        assert response.status_code == 200

    def test_post_risk_assessment_structure(self):
        response = client.post("/risk-assessment", json=VALID_RISK)
        data = response.json()
        assert "crop" in data
        assert "overall_risk" in data
        assert "risk_score" in data
        assert "risks" in data
        assert "disclaimer" in data

    def test_post_risk_assessment_overall_risk_values(self):
        response = client.post("/risk-assessment", json=VALID_RISK)
        data = response.json()
        assert data["overall_risk"] in ("Low", "Medium", "High")

    def test_post_risk_assessment_score_range(self):
        response = client.post("/risk-assessment", json=VALID_RISK)
        data = response.json()
        assert 0 <= data["risk_score"] <= 100

    def test_post_risk_assessment_each_risk_structure(self):
        response = client.post("/risk-assessment", json=VALID_RISK)
        data = response.json()
        for risk in data["risks"]:
            assert "type" in risk
            assert "level" in risk
            assert "description" in risk
            assert "preventive_measure" in risk

    def test_post_risk_assessment_disclaimer_present(self):
        response = client.post("/risk-assessment", json=VALID_RISK)
        data = response.json()
        assert len(data["disclaimer"]) > 0

    def test_post_risk_assessment_unknown_crop(self):
        bad = {**VALID_RISK, "crop": "UnknownCrop"}
        response = client.post("/risk-assessment", json=bad)
        # Should still return 200 with a high-risk result (not a 500)
        assert response.status_code == 200
        data = response.json()
        assert data["overall_risk"] == "High"


# ===========================================================================
# PROFIT
# ===========================================================================

VALID_PROFIT = {
    "crop": "Groundnut",
    "farm_area": 5.0,
    "expected_yield_per_acre": 8.5,
    "market_price_per_unit": 5500,
    "estimated_cost": 72000,
    "transportation_cost": 5000,
}


class TestProfit:
    def test_post_profit_returns_200(self):
        response = client.post("/profit", json=VALID_PROFIT)
        assert response.status_code == 200

    def test_post_profit_structure(self):
        response = client.post("/profit", json=VALID_PROFIT)
        data = response.json()
        assert "crop" in data
        assert "farm_area_acres" in data
        assert "expected_production_quintals" in data
        assert "gross_revenue_inr" in data
        assert "total_cost_inr" in data
        assert "estimated_profit_inr" in data
        assert "profit_margin_percent" in data
        assert "disclaimer" in data

    def test_post_profit_calculation_correctness(self):
        response = client.post("/profit", json=VALID_PROFIT)
        data = response.json()
        # expected_production = 5 * 8.5 = 42.5
        assert data["expected_production_quintals"] == 42.5
        # gross_revenue = 42.5 * 5500 = 233750.0
        assert data["gross_revenue_inr"] == 233750.0
        # total_cost = 72000 + 5000 = 77000
        assert data["total_cost_inr"] == 77000.0
        # estimated_profit = 233750 - 77000 = 156750
        assert data["estimated_profit_inr"] == 156750.0

    def test_post_profit_invalid_negative_area(self):
        bad = {**VALID_PROFIT, "farm_area": -1}
        response = client.post("/profit", json=bad)
        assert response.status_code == 422

    def test_post_profit_invalid_negative_yield(self):
        bad = {**VALID_PROFIT, "expected_yield_per_acre": -5}
        response = client.post("/profit", json=bad)
        assert response.status_code == 422

    def test_post_profit_zero_revenue_no_crash(self):
        """Zero price should not cause division by zero."""
        bad = {**VALID_PROFIT, "market_price_per_unit": 0.001}
        response = client.post("/profit", json=bad)
        # Should return 200 — tiny revenue, not a crash
        assert response.status_code == 200


# ===========================================================================
# MARKET COMPARE
# ===========================================================================

VALID_MARKET = {
    "crop": "Groundnut",
    "quantity": 42.5,
    "production_cost": 72000,
    "markets": [
        {
            "market_name": "Local Market",
            "price_per_unit": 5000,
            "transportation_cost": 2000,
        },
        {
            "market_name": "Regional Market",
            "price_per_unit": 5500,
            "transportation_cost": 6000,
        },
    ],
}


class TestMarketCompare:
    def test_post_market_compare_returns_200(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        assert response.status_code == 200

    def test_post_market_compare_structure(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        data = response.json()
        assert "crop" in data
        assert "best_market" in data
        assert "market_options" in data
        assert "disclaimer" in data

    def test_post_market_compare_ranked_correctly(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        data = response.json()
        options = data["market_options"]
        # Ranks should be 1, 2, 3, ...
        ranks = [o["rank"] for o in options]
        assert ranks == list(range(1, len(options) + 1))

    def test_post_market_compare_sorted_by_profit(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        data = response.json()
        profits = [o["estimated_profit_inr"] for o in data["market_options"]]
        assert profits == sorted(profits, reverse=True)

    def test_post_market_compare_best_market_field(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        data = response.json()
        # best_market must match the rank-1 market
        best = data["market_options"][0]["market_name"]
        assert data["best_market"] == best

    def test_post_market_compare_each_option_structure(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        data = response.json()
        for opt in data["market_options"]:
            assert "market_name" in opt
            assert "price_per_unit" in opt
            assert "gross_revenue_inr" in opt
            assert "transportation_cost_inr" in opt
            assert "total_cost_inr" in opt
            assert "estimated_profit_inr" in opt
            assert "rank" in opt

    def test_post_market_compare_disclaimer_present(self):
        response = client.post("/market/compare", json=VALID_MARKET)
        data = response.json()
        assert len(data["disclaimer"]) > 0
