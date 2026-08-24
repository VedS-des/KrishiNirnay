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
    form.addEventListener("submit", function (event) {
     
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

        // Crop scores  
        let cropScores = { 
            "Groundnut": 0,
            "Millets": 0, 
            "Cotton": 0,
            "Soybean": 0,
            "Rice": 0,
            "Sugarcane": 0, 
            "Wheat": 0,
            "Watermelon": 0 
        };

        // -------------------------
        // SOIL + pH
        // -------------------------

        if (soil === "red") {

            cropScores["Groundnut"] += 30;
            cropScores["Millets"] += 25;

            if (ph >= 5.5 && ph <= 7.5) {
                cropScores["Groundnut"] += 20;
                cropScores["Millets"] += 15;
                cropScores["Cotton"] += 10;
            }
        }

        if (soil === "black") {

            cropScores["Cotton"] += 30;
            cropScores["Soybean"] += 25;

            if (ph >= 6 && ph <= 8) {
                cropScores["Cotton"] += 20;
                cropScores["Soybean"] += 15;
            }
        }

        if (soil === "alluvial") {

            cropScores["Rice"] += 30;
            cropScores["Wheat"] += 25;
        }

        if (soil === "sandy") {

            cropScores["Groundnut"] += 30;
            cropScores["Millets"] += 25;
            cropScores["Watermelon"] += 20;
        }

        if (soil === "clay") {

            cropScores["Rice"] += 30;
        }

        // -------------------------
        // WATER
        // -------------------------

        if (water === "high") {
            cropScores["Rice"] += 20;
            cropScores["Sugarcane"] += 20;
            cropScores["Watermelon"] += 10;
        }

        if (water === "medium") {
            cropScores["Millets"] += 15;
            cropScores["Groundnut"] += 10;
            cropScores["Cotton"] += 10;
            cropScores["Wheat"] += 10;
        }

        if (water === "low") {
            cropScores["Millets"] += 20;
            cropScores["Groundnut"] += 15;
        }

        // -------------------------
        // SEASON
        // -------------------------

        if (season === "kharif") {
            cropScores["Groundnut"] += 15;
            cropScores["Cotton"] += 15;
            cropScores["Millets"] += 15;
            cropScores["Soybean"] += 15;
        }

        if (season === "rabi") {
            cropScores["Wheat"] += 15;
            cropScores["Millets"] += 15;
            cropScores["Soybean"] += 10;
        }

        if (season === "summer") {
            cropScores["Watermelon"] += 15;
            cropScores["Millets"] += 10;
            cropScores["Groundnut"] += 10;
        }

        // -------------------------
        // BUDGET
        // -------------------------

        if (budget < 50000) {
            cropScores["Millets"] += 15;
            cropScores["Groundnut"] += 10;

            cropScores["Sugarcane"] -= 10;
            cropScores["Cotton"] -= 5;
        }

        if (budget >= 50000 && budget <= 200000) {
            cropScores["Groundnut"] += 10;
            cropScores["Millets"] += 10;
            cropScores["Cotton"] += 5;
        }

        if (budget > 200000) {
            cropScores["Cotton"] += 10;
            cropScores["Sugarcane"] += 10;
            cropScores["Rice"] += 5;
        }

        // -------------------------
        // PREVIOUS CROP
        // -------------------------

        if (previousCrop !== "") {

            Object.keys(cropScores).forEach(function (crop) {

                if (crop.toLowerCase() === previousCrop.toLowerCase()) {
                    cropScores[crop] -= 40;
                }

            });
        }

        // -------------------------
        // CREATE RANKING
        // -------------------------

        let rankedCrops = Object.entries(cropScores)
            .sort(function (a, b) {
                return b[1] - a[1];
            });
 
        // Take top 3 crops
        let topCrops = rankedCrops.slice(0, 3);
        localStorage.setItem("bestCrop", topCrops[0][0]);
        localStorage.setItem("bestCropScore", topCrops[0][1]);

        // ------------------------- 
        // DISPLAY RESULT
        // -------------------------

        const recommendationBox =
            document.getElementById("recommendation");

        const recommendationText =
            document.getElementById("recommendationText");
        let reason = "";

if (topCrops[0][0] === "Millets") {
    reason =
        "Millets are recommended because your farm has " +
        soil + " soil, a soil pH of " + ph +
        ", and " + water +
        " water availability.";
}
else if (topCrops[0][0] === "Groundnut") {
    reason = "Groundnut is suitable because your soil and water conditions support it.";
}
else if (topCrops[0][0] === "Cotton") {
    reason = "Cotton is suitable based on your soil, pH, water availability, season, and budget.";
}
else if (topCrops[0][0] === "Rice") {
    reason = "Rice is suitable because your soil and water availability support it.";
}
else if (topCrops[0][0] === "Wheat") {
    reason = "Wheat is suitable based on your season and farm conditions.";
}
else if (topCrops[0][0] === "Soybean") {
    reason = "Soybean is suitable based on your soil and seasonal conditions.";
}
else if (topCrops[0][0] === "Sugarcane") {
    reason = "Sugarcane is suitable because your water availability and budget support it.";
}
else if (topCrops[0][0] === "Watermelon") {
    reason = "Watermelon is suitable based on your soil and seasonal conditions.";
}
        recommendationText.innerHTML =
            "<strong>Farmer:</strong> " + farmerName + "<br>" +
            "<strong>Location:</strong> " + location + "<br>" +
            "<strong>Farm Area:</strong> " + area + " acres<br>" +
            "<strong>Soil Type:</strong> " + soil + "<br>" +
            "<strong>Soil pH:</strong> " + ph + "<br>" +
            "<strong>Season:</strong> " + season + "<br>" +
            "<strong>Water Availability:</strong> " + water + "<br>" +
            "<strong>Budget:</strong> ₹" + budget + "<br>" +
            "<strong>Previous Crop:</strong> " + previousCrop +
            "<br><br>" +

            "<strong>🌾 Crop Recommendation</strong><br><br>" +

"<strong>🥇 Best Recommended Crop:</strong><br>" +
"<span style='font-size: 24px;'>" +
topCrops[0][0] +
"</span><br>" +
"Score: " + topCrops[0][1] +
"<br>" +

"<strong>Why this crop?</strong><br>" +
reason +
"<br><br>" + 


"<strong>🌱 Other Suitable Crops:</strong><br>" +
"🥈 " + topCrops[1][0] +
" — Score: " + topCrops[1][1] + "<br>" +
"🥉 " + topCrops[2][0] +
" — Score: " + topCrops[2][1];
        recommendationBox.style.display = "block";

    }); 
 
});    
