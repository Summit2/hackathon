import numpy as np
import json


def cosine_similarity(elem, arr):

    result = []
    for i in arr:

        dot_product = np.dot(i, elem)
        norm_a = np.linalg.norm(i)
        norm_b = np.linalg.norm(elem)
        result.append(dot_product / (norm_a * norm_b))

    return np.array(result)


def best_dishes(calories, proteins, fat,  carbohydrates ):
    with open("food.json","r", encoding="utf-8") as f:
        food_data = json.load(f)



    item = np.array([calories, proteins, fat,  carbohydrates])

    breakfast = []
    lunch = []
    dinner = []


    for i in range(len(food_data)):
        if food_data[i]['meal_type'] == 'Breakfast' :
            breakfast.append(food_data[i])
        elif food_data[i]['meal_type'] == 'Dinner' :
            dinner.append(food_data[i])
        elif food_data[i]['meal_type'] == 'Lunch' :
            lunch.append(food_data[i])



    def get_best_meal(meal):

        meal_list = []
        ids_meal = []
        for i in range(len(meal)):
            temp = list(meal[i].values())

            ids_meal.append(temp[1])
            meal_list.append(temp[2:])

        meal_list = np.array(meal_list)

        cosine_similarity_list = cosine_similarity(item, meal_list)

        cosine_similarity_list[cosine_similarity_list==1] = 0 
        
        id_max = np.argmax(cosine_similarity_list)
        return id_max
    
    id_br = get_best_meal(breakfast)
    id_lu = get_best_meal(lunch)
    id_di = get_best_meal(dinner)

    return {
        'Breakfast' : breakfast[id_br],
        'Lunch' : lunch[id_lu],
        'Dinner' : dinner[id_di]
    }




