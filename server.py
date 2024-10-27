from flask import Flask, request, jsonify
import json
from linear_regression import MyLinearRegression
import numpy as np
from model_get_dishes import get_best_meal
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
    calories = data.get('calories', 0)
    proteins = data.get('protein', 0)
    fat = data.get('fat', 0)
    carbohydrates = data.get('carbohydrates', 0)
    url = data.get('image_url', '')
    print(url)
    if calories <= 0 or proteins <= 0 or fat <= 0 or carbohydrates <= 0:
        return jsonify({"error": "Each nutrient value should be more than zero"}), 400

   
    # dishes = best_dishes(calories, proteins, fat, carbohydrates)
    # print(dishes)
    with open("food.json","r", encoding="utf-8") as f:
        food_data = json.load(f)



    item = np.array([calories, proteins, fat,  carbohydrates])

    breakfast = []
    lunch = []
    dinner = []

    print(food_data[0])
    for i in range(len(food_data)):
        
        temp_food_data = [i, food_data[i][ "calories"],food_data[i][ "protein"],food_data[i][ "fat"] ,food_data[i][ "carbohydrates"] ]
        if food_data[i]['meal_type'] == 'Breakfast' :
            breakfast.append(temp_food_data   )
        elif food_data[i]['meal_type'] == 'Dinner' :
            dinner.append(temp_food_data)
        elif food_data[i]['meal_type'] == 'Lunch' :
            lunch.append(temp_food_data)



    
    
    id_br = get_best_meal(item ,breakfast, 0.2)
    id_lu = get_best_meal(item,lunch, 0.5)
    id_di = get_best_meal(item, dinner, 0.3)

    best_breakfast = 
    best_lunch = 
    best_dinner = 
   
    dishes =  {
        'Breakfast' : breakfast[id_br],
        'Lunch' : lunch[id_lu],
        'Dinner' : dinner[id_di]
    }
    return jsonify(dishes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080,debug=True)
