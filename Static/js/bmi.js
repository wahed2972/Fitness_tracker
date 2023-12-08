var weight, height, measure, bmi, error;

function calculate() {
    weight = parseFloat(document.getElementById("weight").value);
    height = parseFloat(document.getElementById("height").value);
    error = "Please enter valid values for weight and height";
    height /= 100; // Convert height to meters
    height *= height;
    bmi = (weight / height).toFixed(1);

    var resultContainer = document.getElementById("results");
    var recommendationsList = document.getElementById("recommendations-list");
    recommendationsList.innerHTML = ''; // Clear previous recommendations

    if (isNaN(weight) || isNaN(height) || weight <= 0 || height <= 0) {
        resultContainer.innerHTML = error;
    } else {
        if (bmi <= 18.4) {
            measure = "Your BMI is " + bmi + " which means you are Underweight. ";

            // Diet and Exercise Recommendations for Underweight
            addRecommendation("Increase calorie intake with nutrient-dense foods.");
            addRecommendation("Include lean proteins, whole grains, healthy fats, and a variety of fruits and vegetables.");
            addRecommendation("Exercise: Focus on strength training exercises to build muscle mass and increase overall body strength. Combine with cardiovascular exercises for overall fitness.");

        } else if (bmi >= 18.5 && bmi <= 24.9) {
            measure = "Your BMI is " + bmi + " which means you are Normal. ";

            // Diet and Exercise Recommendations for Normal Weight
            addRecommendation("Maintain a balanced diet with a variety of foods.");
            addRecommendation("Keep portion sizes in check.");
            addRecommendation("Exercise: Aim for at least 150 minutes of moderate-intensity aerobic activity per week and include strength training exercises at least twice a week.");

        } else if (bmi >= 25 && bmi <= 29.9) {
            measure = "Your BMI is " + bmi + " which means you are Overweight. ";

            // Diet and Exercise Recommendations for Overweight
            addRecommendation("Create a calorie deficit by consuming fewer calories than you burn.");
            addRecommendation("Choose whole, unprocessed foods.");
            addRecommendation("Exercise: Incorporate regular cardiovascular and strength training exercises for overall fitness and weight loss.");

        } else if (bmi >= 30) {
            measure = "Your BMI is " + bmi + " which means you are Obese. ";

            // Diet and Exercise Recommendations for Obese
            addRecommendation("Seek guidance from a registered dietitian or healthcare professional for a personalized weight loss plan.");
            addRecommendation("Focus on nutrient-dense foods and portion control.");
            addRecommendation("Exercise: Engage in regular, vigorous-intensity aerobic activities and strength training exercises to burn calories and build lean muscle.");
        }

        resultContainer.innerHTML = measure;
    }
    if (weight < 0 || height < 0) {
        resultContainer.innerHTML = "Negative Values not Allowed";
    }

    // Function to add recommendations to the list
    function addRecommendation(text) {
        var listItem = document.createElement("li");
        listItem.innerText = text;
        recommendationsList.appendChild(listItem);
    }
}
