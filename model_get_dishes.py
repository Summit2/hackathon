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


# def best_dishes(calories, proteins, fat,  carbohydrates ):
#     with open("food.json","r", encoding="utf-8") as f:
#         food_data = json.load(f)



#     item = np.array([calories, proteins, fat,  carbohydrates])

#     breakfast = []
#     lunch = []
#     dinner = []


#     for i in range(len(food_data)):
#         if food_data[i]['meal_type'] == 'Breakfast' :
#             breakfast.append(food_data[i])
#         elif food_data[i]['meal_type'] == 'Dinner' :
#             dinner.append(food_data[i])
#         elif food_data[i]['meal_type'] == 'Lunch' :
#             lunch.append(food_data[i])



#     def get_best_meal(meal, coef):

#         meal_list = []
#         ids_meal = []
#         for i in range(len(meal)):
#             temp = list(meal[i].values())

#             ids_meal.append(temp[1])
#             meal_list.append(temp[2:])

#         meal_list = np.array(meal_list)

#         print(item * coef)
#         cosine_similarity_list = cosine_similarity(item * coef, meal_list)

#         cosine_similarity_list[cosine_similarity_list==1] = 0 
        
#         id_max = np.argmax(cosine_similarity_list)
#         return id_max
    
#     id_br = get_best_meal(breakfast, 0.2)
#     id_lu = get_best_meal(lunch, 0.5)
#     id_di = get_best_meal(dinner, 0.3)

#     return {
#         'Breakfast' : breakfast[id_br],
#         'Lunch' : lunch[id_lu],
#         'Dinner' : dinner[id_di]
#     }
def get_best_meal(item, meal, coef):

        meal_list = []
        ids_meal = []
        for i in range(len(meal)):
            # temp = list(meal[i].values())
            temp = meal[i]
            ids_meal.append(temp[1])
            meal_list.append(temp[1:])

        meal_list = np.array(meal_list)

        # print(item * coef)
        # print(meal_list)
        cosine_similarity_list = cosine_similarity(item * coef, meal_list)

        cosine_similarity_list[cosine_similarity_list==1] = 0 
        
        id_max = np.argmax(cosine_similarity_list)
        return id_max




