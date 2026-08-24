const savedName = localStorage.getItem("userName");
const savedLocation = localStorage.getItem("farmLocation");
const savedArea = localStorage.getItem("farmArea");
const savedSoil = localStorage.getItem("farmSoil");
const savedPH = localStorage.getItem("farmPH");
const savedWater = localStorage.getItem("farmWater");
const savedBudget = localStorage.getItem("farmBudget");
const savedSeason = localStorage.getItem("farmSeason");
const savedPreviousCrop = localStorage.getItem("farmPreviousCrop");
const savedBestCrop = localStorage.getItem("bestCrop");
const savedBestCropScore = localStorage.getItem("bestCropScore");
document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("farmForm");
    document.getElementById("farmerName").value = savedName || "";
    document.getElementById("location").value = savedLocation || "";
    document.getElementById("area").value = savedArea || "";
    document.getElementById("soil").value = savedSoil || "";
    document.getElementById("ph").value = savedPH || "";
    document.getElementById("water").value = savedWater || "";
    document.getElementById("budget").value = savedBudget || "";
    document.getElementById("season").value = savedSeason || "";
    document.getElementById("previousCrop").value = savedPreviousCrop || "";
    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        // Get farm details
        const farmerName = document.getElementById("farmerName").value;
        const location = document.getElementById("location").value;
        const area = parseFloat(document.getElementById("area").value);
        const soil = document.getElementById("soil").value;
        const ph = parseFloat(document.getElementById("ph").value);
        const water = document.getElementById("water").value;
        const budget = parseFloat(document.getElementById("budget").value);
        const season = document.getElementById("season").value;
        const previousCrop = document.getElementById("previousCrop").value.trim();

        // Save farm details
        localStorage.setItem("farmLocation", location);
        localStorage.setItem("farmArea", area);
        localStorage.setItem("farmSoil", soil);
        localStorage.setItem("farmPH", ph);
        localStorage.setItem("farmWater", water);
        localStorage.setItem("farmBudget", budget);
        localStorage.setItem("farmSeason", season);
        localStorage.setItem("farmPreviousCrop", previousCrop);

        // Send farm details to the backend recommendation API
        try {
            const response = await fetch("http://127.0.0.1:8000/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    location: location,
                    area: area,
                    soil_type: soil,
                    soil_ph: ph,
                    water_availability: water,
                    budget: budget,
                    season: season,
                    previous_crop: previousCrop || null
                })
            });

            if (!response.ok) {
                throw new Error("Backend recommendation request failed");
            }

            const data = await response.json();

            const recommendations = data.recommendations;

            if (!recommendations || recommendations.length === 0) {
                throw new Error("No crop recommendations received");
            }

            // Save best crop for other frontend pages
            localStorage.setItem(
                "bestCrop",
                recommendations[0].crop
            );

            localStorage.setItem(
                "bestCropScore",
                recommendations[0].suitability_score
            );

            // Display recommendation from backend

            const recommendationBox =
                document.getElementById("recommendation");

            const recommendationText =
                document.getElementById("recommendationText");

            const bestCrop = recommendations[0];

            let otherCrops = "";

            recommendations.slice(1, 3).forEach(function (crop, index) {

                const medal = index === 0 ? "🥈" : "🥉";

                otherCrops +=
                    medal + " " +
                    crop.crop +
                    " — Score: " +
                    crop.suitability_score +
                    "<br>";
            });

            recommendationText.innerHTML =
                "<strong>Farmer:</strong> " + farmerName + "<br>" +
                "<strong>Location:</strong> " + location + "<br>" +
                "<strong>Farm Area:</strong> " + area + " acres<br>" +
                "<strong>Soil Type:</strong> " + soil + "<br>" +
                "<strong>Soil pH:</strong> " + ph + "<br>" +
                "<strong>Season:</strong> " + season + "<br>" +
                "<strong>Water Availability:</strong> " + water + "<br>" +
                "<strong>Budget:</strong> ₹" + budget + "<br>" +
                "<strong>Previous Crop:</strong> " +
                (previousCrop || "None") +
                "<br><br>" +

                "<strong>🌾 Crop Recommendation</strong><br><br>" +

                "<strong>🥇 Best Recommended Crop:</strong><br>" +
                "<span style='font-size: 24px;'>" +
                bestCrop.crop +
                "</span><br>" +

                "Suitability Score: " +
                bestCrop.suitability_score +
                "<br><br>" +

                "<strong>Why this crop?</strong><br>" +
                bestCrop.reason +
                "<br><br>" +

                "<strong>💰 Estimated Profit:</strong> ₹" +
                bestCrop.estimated_profit_inr +
                "<br>" +

                "<strong>⚠️ Risk Level:</strong> " +
                bestCrop.risk_level +
                "<br><br>" +

                "<strong>🌱 Other Suitable Crops:</strong><br>" +
                otherCrops;

            recommendationBox.style.display = "block";
        } catch (error) {

            console.error("Recommendation API error:", error);

            alert(
                "Could not get crop recommendations from the backend. " +
                "Please make sure the KrishiNirnay backend is running."
            );
        }
    });
});
