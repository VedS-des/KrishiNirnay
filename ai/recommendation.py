import json

# Load the crop data from crops.json
with open("data/crops.json", "r") as file:
    crops = json.load(file)

# Check how many crops were loaded
print("Number of crops:", len(crops))

# Print each crop name
print("\nAvailable crops:")

for crop in crops:
    print("-", crop["name"])

# Farmer information

print("\nEnter Farmer Information")

location = input("Enter location: ")
area = float(input("Enter land area (acres): "))
soil_type = input("Enter soil type (red/black/sandy/loamy/alluvial): ")
soil_ph = float(input("Enter soil pH: "))
water_availability = input("Enter water availability (low/medium/high): ")
budget = float(input("Enter budget (₹): "))
season = input("Enter season (kharif/rabi): ")

farmer = {
    "location": location,
    "area": area,
    "soil_type": soil_type,
    "soil_ph": soil_ph,
    "water_availability": water_availability,
    "budget": budget,
    "season": season
}

print("\nFarmer Information:")
print("Location:", farmer["location"])
print("Area:", farmer["area"], "acres")
print("Soil:", farmer["soil_type"])
print("pH:", farmer["soil_ph"])
print("Water:", farmer["water_availability"])
print("Budget: ₹", farmer["budget"])
print("Season:", farmer["season"])

# Calculate soil suitability score
def calculate_soil_score(farmer, crop):

    score = 0

    # Check soil type
    if farmer["soil_type"] in crop["soil_types"]:
        score += 70

    # Check soil pH
    if crop["ph_min"] <= farmer["soil_ph"] <= crop["ph_max"]:
        score += 30

    return score

# Test soil scores for all crops
print("\nSoil Suitability Scores:")

for crop in crops:
    score = calculate_soil_score(farmer, crop)
    print(crop["name"], ":", score, "/ 100")

    # Calculate water suitability score
def calculate_water_score(farmer, crop):

    farmer_water = farmer["water_availability"]
    crop_water = crop["water_requirement"]

    if farmer_water == crop_water:
        return 100

    # Medium water can support low-water crops,
    # but low water cannot support medium/high-water crops.
    if farmer_water == "medium" and crop_water == "low":
        return 80

    if farmer_water == "high" and crop_water == "medium":
        return 90

    if farmer_water == "high" and crop_water == "low":
        return 100

    return 30

# Test water scores for all crops
print("\nWater Suitability Scores:")

for crop in crops:
    score = calculate_water_score(farmer, crop)
    print(crop["name"], ":", score, "/ 100")

    # Calculate season suitability score
def calculate_season_score(farmer, crop):

    farmer_season = farmer["season"]
    crop_seasons = crop["seasons"]

    # Check whether the farmer's season is suitable for this crop
    if farmer_season in crop_seasons:
        return 100

    return 30


# Test season scores for all crops
print("\nSeason Suitability Scores:")

for crop in crops:
    score = calculate_season_score(farmer, crop)
    print(crop["name"], ":", score, "/ 100")

    # Calculate overall suitability score
def calculate_overall_score(farmer, crop):

    soil_score = calculate_soil_score(farmer, crop)
    water_score = calculate_water_score(farmer, crop)
    season_score = calculate_season_score(farmer, crop)

    overall_score = (
        soil_score * 0.40
        + water_score * 0.30
        + season_score * 0.30
    )

    return overall_score

# Test overall scores for all crops
print("\nOverall Suitability Scores:")

for crop in crops:
    score = calculate_overall_score(farmer, crop)
    print(crop["name"], ":", round(score, 2), "/ 100")

    # Rank crops from highest suitability to lowest
ranked_crops = []

for crop in crops:
    score = calculate_overall_score(farmer, crop)

    ranked_crops.append({
        "name": crop["name"],
        "score": score
    })

ranked_crops.sort(key=lambda x: x["score"], reverse=True)


print("\n🌱 Crop Recommendations:")

for position, crop in enumerate(ranked_crops, start=1):
    print(
        position,
        ".",
        crop["name"],
        "-",
        round(crop["score"], 2),
        "/ 100"
    )

# Generate an explanation for a crop recommendation
def generate_reason(farmer, crop):

    reasons = []

    soil_score = calculate_soil_score(farmer, crop)
    water_score = calculate_water_score(farmer, crop)
    season_score = calculate_season_score(farmer, crop)

    if soil_score >= 70:
        reasons.append("Suitable soil")

    if farmer["soil_ph"] >= crop["ph_min"] and farmer["soil_ph"] <= crop["ph_max"]:
        reasons.append("Suitable soil pH")

    if water_score >= 80:
        reasons.append("Suitable water availability")

    if season_score == 100:
        reasons.append("Suitable season")

    return reasons

print("\n🌾 Recommendation Reasons:")

for position, crop in enumerate(ranked_crops, start=1):

    # Find the complete crop information
    crop_data = next(c for c in crops if c["name"] == crop["name"])

    reasons = generate_reason(farmer, crop_data)

    print("\n", position, ".", crop["name"])
    print("   Score:", round(crop["score"], 2), "/ 100")

    for reason in reasons:
        print("   ✓", reason)

# Estimated yield per acre (kg)
estimated_yield = {
    "Groundnut": 1000,
    "Rice": 1800,
    "Black Gram": 700,
    "Maize": 2200,
    "Sesame": 500
}

# Estimated selling price per kg (₹)
estimated_price = {
    "Groundnut": 70,
    "Rice": 25,
    "Black Gram": 80,
    "Maize": 22,
    "Sesame": 90
}

# Calculate estimated profit
def calculate_profit(crop):

    name = crop["name"]

    revenue = estimated_yield[name] * estimated_price[name]

    cost = crop["cost_per_acre"]

    profit = revenue - cost

    return revenue, cost, profit

print("\n💰 Estimated Profit:")

for crop in ranked_crops:

    crop_data = next(c for c in crops if c["name"] == crop["name"])

    revenue, cost, profit = calculate_profit(crop_data)

    print("\n", crop["name"])
    print("   Revenue: ₹", revenue)
    print("   Cost: ₹", cost)
    print("   Estimated Profit: ₹", profit)

# Final recommendation score
def calculate_final_score(suitability_score, profit):
    profit_score = max(0, min(100, (profit / 50000) * 100))

    final_score = (
        suitability_score * 0.70
        + profit_score * 0.30
    )

    return final_score


print("\n🌾 Final Crop Recommendation:")

final_recommendations = []

for crop in ranked_crops:

    crop_data = next(c for c in crops if c["name"] == crop["name"])

    revenue, cost, profit = calculate_profit(crop_data)

    final_score = calculate_final_score(crop["score"], profit)

    final_recommendations.append({
        "name": crop["name"],
        "score": final_score,
        "profit": profit
    })

final_recommendations.sort(
    key=lambda x: x["score"],
    reverse=True
)

for position, crop in enumerate(final_recommendations, start=1):
    print(
        position,
        ".",
        crop["name"],
        "- Final Score:",
        round(crop["score"], 2),
        "/ 100",
        "- Profit: ₹",
        crop["profit"]
    )

print("\n🌾 FINAL RECOMMENDATION")
print("======================")

best_crop = final_recommendations[0]

best_crop_data = next(
    c for c in crops
    if c["name"] == best_crop["name"]
)

reasons = generate_reason(farmer, best_crop_data)

print("Recommended Crop:", best_crop["name"])
print("Final Score:", round(best_crop["score"], 2), "/ 100")
print("Estimated Profit: ₹", best_crop["profit"])

print("\nWhy this crop?")
for reason in reasons:
    print("✓", reason)