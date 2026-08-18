# KrishiNirnay — MVP

## 1. MVP Goal

Build an AI-powered farm decision support system that helps farmers:

- Select suitable crops
- Understand crop growth stages
- Monitor weather-related risks
- Compare nearby market prices
- Estimate expected profit

The MVP should demonstrate the complete flow:

Farmer Input → Crop Recommendation → Crop Details → Weather → Market Comparison → Profit Estimation


## 2. Farmer Inputs

The farmer will provide:

| Input | Description |
|---|---|
| Location | Farmer's farm location |
| Farm Area | Area of the farm in acres |
| Soil Type | Type of soil |
| Water Availability | Low / Moderate / High |
| Budget | Available farming budget in ₹ |
| Season | Current farming season |


## 3. Core MVP Features

### 3.1 Crop Recommendation

The system will recommend the top 3 suitable crops based on:

- Location
- Soil type
- Water availability
- Farm area
- Budget
- Season

Each recommendation should display:

- Crop name
- Suitability score
- Expected yield
- Estimated cultivation cost
- Expected revenue
- Expected profit
- Risk level


### 3.2 Crop Details

For a selected crop, the system will display:

- Crop name
- Crop duration
- Water requirement
- Suitable soil
- Crop lifecycle
- Important farming activities
- Expected harvest period


### 3.3 Weather Information

The system will display:

- Current temperature
- Humidity
- Rain probability
- Weather condition
- Basic farming risk/alert

Weather data will be obtained from an external weather API.


### 3.4 Market Information

The system will display:

- Available markets
- Market location
- Crop price
- Distance
- Estimated transportation cost
- Estimated net return

The farmer should be able to compare different markets.


### 3.5 Profit Calculation

The system will calculate:

Gross Revenue = Production × Selling Price

Total Cost = Cultivation Cost + Transport Cost + Other Cost

Net Profit = Gross Revenue - Total Cost


## 4. Complete User Flow

Farmer opens KrishiNirnay

↓

Enters farm details

↓

System recommends top 3 crops

↓

Farmer selects a crop

↓

System displays crop details and lifecycle

↓

System displays weather information and alerts

↓

System displays market comparison

↓

System calculates expected profit

↓

Farmer gets a final decision-support summary


## 5. MVP Dashboard

The dashboard should contain:

- Farmer/farm summary
- Recommended crops
- Weather information
- Crop lifecycle/progress
- Market comparison
- Expected profit


## 6. MVP Data

The MVP will use:

- Crop dataset
- Crop lifecycle data
- Market data
- Market price data
- Weather API data

All agricultural values and market prices should be verified using reliable sources before being presented as real information.


## 7. MVP Limitations

The following features are NOT required for the MVP:

- International transactions
- Online payments
- Full e-commerce
- IoT sensor integration
- Drone integration
- Satellite image analysis
- Blockchain
- Voice assistant
- Advanced disease image detection
- Complex export system
- Real-time farmer-to-buyer transactions


## 8. MVP Success Criteria

The MVP will be considered successful when:

1. A farmer can enter farm details.
2. The system can generate crop recommendations.
3. The farmer can view crop details.
4. Weather information can be displayed.
5. Markets can be compared.
6. Expected profit can be calculated.
7. The complete flow works through the website.


## 9. Demo Scenario

The team will maintain one fixed demo scenario for testing.

Example:

Location: Villupuram, Tamil Nadu

Farm Area: 5 acres

Soil Type: Red

Water Availability: Moderate

Budget: ₹1,50,000

Season: Kharif

The values and final crop recommendations used in the demo should be verified by the data/AI team.


## 10. Development Priority

### Priority 1 — MUST WORK

- Farmer input form
- Crop recommendation
- Backend API
- Frontend-backend connection

### Priority 2 — SHOULD WORK

- Crop details
- Weather information
- Market comparison
- Profit calculation

### Priority 3 — ONLY IF TIME REMAINS

- Animations
- Advanced dashboard visuals
- Additional languages
- Advanced AI features
- Extra analytics


## 11. MVP Rule

No new major feature should be added unless all Priority 1 features are working.
