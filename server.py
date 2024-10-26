from flask import Flask, request, jsonify
import json
from linear_regression import MyLinearRegression
import numpy as np
from model_get_dishes import best_dishes
app = Flask(__name__)


model_get_jogging_calories = MyLinearRegression()
with open("model_jogging_calories.json", "r") as json_file:
    data = json.load(json_file)
model_get_jogging_calories.weights = data['weights']


@app.route('/methods/get_calories', methods=['POST'])
def get_calories():


    '''
    Input format - {
        "sex": "M" or "F",
        "weight": int,
        "height": int,
        "jog_type": "JL" (Jog Light), "JI" (Jog Intense), or "R" (Running),
        "time": int
    }
    '''

    data = request.json
    
 
    if not isinstance(data, dict):
        return jsonify({"error": "Input data must be a JSON object."}), 400


    required_keys = ["sex", "weight", "height", "jog_type", "time"]
    for key in required_keys:
        if key not in data:
            return jsonify({"error": f"Missing required key: {key}"}), 400


    try:
        sex = data['sex']
        weight = float(data['weight'])
        height = float(data['height'])
        jog_type = data['jog_type']
        time = float(data['time'])

      
        if sex not in ["M", "F"]:
            return jsonify({"error": "Sex must be 'M' or 'F'."}), 400
        
      
        if weight <= 0 or height <= 0 or time < 0:
            return jsonify({"error": "Weight, height, and time must be positive values."}), 400
        

        if jog_type not in ["JL", "JI", "R"]:
            return jsonify({"error": "Jog type must be 'JL', 'JI', or 'R'."}), 400

    except ValueError:
        return jsonify({"error": "Weight, height, and time must be numeric."}), 400

    sex_female = 1 if sex == "F" else 0
    sex_male = 1 if sex == "M" else 0
    jog_light = 1 if jog_type == "JL" else 0
    jog_intense = 1 if jog_type == "JI" else 0
    run = 1 if jog_type == "R" else 0

    input_data = np.array([sex_female, sex_male, weight, height, jog_light, jog_intense, run, time])

    # Make the prediction
    predicted_calories = model_get_jogging_calories.predict(input_data).item()

    # Adjust calories based on jog_type
    if jog_light:
        predicted_calories *= 0.15
    elif jog_intense:
        predicted_calories *= 0.20
    elif run:
        predicted_calories *= 0.3

    result = {'calories': predicted_calories}
    print(result["calories"])
   
    return jsonify(result)


@app.route('/methods/get_dishes', methods=['POST'])
def get_dishes():
    '''
    returns something like that
    {
    "Breakfast": {
        "calories": 200,
        "carbohydrates": 25,
        "dish_name": "Творог с медом и ягодами",
        "fat": 5,
        "meal_type": "Breakfast",
        "protein": 12
    },
    "Dinner": {
        "calories": 550,
        "carbohydrates": 60,
        "dish_name": "Курица с карри и рисом",
        "fat": 25,
        "meal_type": "Dinner",
        "protein": 40
    },
    "Lunch": {
        "calories": 350,
        "carbohydrates": 40,
        "dish_name": "Куриное филе с гречкой",
        "fat": 10,
        "meal_type": "Lunch",
        "protein": 40
    }
}
    '''
    data = request.json
    calories = data.get('Calories', 0)
    proteins = data.get('Proteins', 0)
    fat = data.get('Fat', 0)
    carbohydrates = data.get('Carbohydrates', 0)

    if calories <= 0 or proteins <= 0 or fat <= 0 or carbohydrates <= 0:
        return jsonify({"error": "Each nutrient value should be more than zero"}), 400

   
    dishes = best_dishes(calories, proteins, fat, carbohydrates)
    return jsonify(dishes)

if __name__ == '__main__':
    app.run(debug=True)
