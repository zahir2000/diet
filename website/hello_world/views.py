from django.shortcuts import render
import pandas as pd
from ortools.linear_solver import pywraplp

def calculate(gender, 
    custom_calorie = 0,
    custom_manga = 0,
    custom_zinc = 0,
    custom_iron = 0,
    custom_calc = 0,
    custom_vitK = 0,
    custom_vitE = 0,
    custom_vitD = 0,
    custom_vitC = 0,
    custom_vitA = 0,
    custom_fruit = 0,
    custom_meat = 0,
    custom_chol = 0,
    custom_added_sugar = 0,
    custom_sat_fat = 0,
    custom_carb = 0,
    custom_protein = 0,
    custom_max_sodium = 0,
    custom_min_sodium = 0,
    custom_max_fibre = 0,
    custom_min_fibre = 0,
    custom_max_fat = 0,
    custom_min_fat = 0
):
    df = pd.read_excel("hello_world/NutrientsTest.xlsx")

    veg = df['Category'] == "Vegetables"
    fruit = df['Category'] == "Fruits"

    df['Meat'] = df['Category'] == "Meat"
    df['Meat'] = df['Meat'].astype(int)
    df['FruitVeg'] = fruit | veg
    df['FruitVeg'] = df['FruitVeg'].astype(int)
    df['Condiment'] = df['Category'] == "Condiment"
    df['Condiment'] = df['Condiment'].astype(int)

    #select columns
    columns3 = []
    columns3.append("Category")
    columns3.append("Food Name")
    columns3.append("Price (RM)")
    columns3.append("Fat, total (g/100g)")
    columns3.append("Fibre, total dietary (g/100g)")
    columns3.append("Protein, total; calculated from total nitrogen (g/100g)")
    columns3.append("Sugars, total (g/100g)")
    columns3.append("Fatty acids, total saturated (g/100g)")
    columns3.append("Sugar, added")
    columns3.append("Cholesterol (mg/100g)")
    columns3.append("Energy (kcal/100g)")
    columns3.append("Meat")
    columns3.append("FruitVeg")
    columns3.append("Vitamin C (mg/100g)")
    columns3.append("Vitamin E, alpha-tocopherol equivalents (mg/100g)")
    columns3.append("Calcium (mg/100g)")
    columns3.append("Sodium (mg/100g)")
    columns3.append("Iron (mg/100g)")
    columns3.append("Zinc (mg/100g)")
    columns3.append("Vitamin A, retinol equivalents (µg/100g)")
    columns3.append("Vitamin D (μg/100g)")
    columns3.append("Vitamin K (μg/100g)")
    columns3.append("Manganese (μg/100g)")
    columns3.append("Fat, total (g/100g)")
    columns3.append("Fibre, total dietary (g/100g)")
    columns3.append("Sodium (mg/100g)")
    columns3.append("Condiment")
    columns3

    df2 = df[columns3]
    #df2 = df[df.columns.intersection(columns3)]
    data = df2.values.tolist()

    #create list of coefficients for linear program

    # Nutrient constraints.
    # Nutrient constraints.
    if (gender == 'male'):
        nutrients2 = [
            ["Fat, total (g/100g)", 73],
            ["Fibre, total dietary (g/100g)", 20],
            ["Protein, total; calculated from total nitrogen (g/100g)", 61],
            ["Sugars, total (g/100g)", 325],
            ["Fatty acids, total saturated (g/100g)", 20],
            ["Sugar, added", 50],
            ["Cholesterol (mg/100g)", 300],
            ["Energy (kcal/100g)", 2190],
            ["Meat", 1],
            ["FruitVeg", 4],
            ["Vitamin C (mg/100g)", 70],
            ["Vitamin E, alpha-tocopherol equivalents (mg/100g)", 10],
            ["Calcium (mg/100g)", 1000],
            ["Sodium (mg/100g)", 2300],
            ["Iron (mg/100g)", 9],
            ["Zinc (mg/100g)", 6.5],
            ["Vitamin A, retinol equivalents (µg/100g)", 600],
            ["Vitamin D (μg/100g)", 15], #!!!
            ["Vitamin K (μg/100g)", 65],
            ["Manganese (μg/100g)", 2300],
            ["Fat, total (g/100g)", 61],
            ["Fibre, total dietary (g/100g)", 70],
            ["Sodium (mg/100g)", 1500],
            ["Condiment", 0.06]
        ]
    elif (gender == 'female'):
        nutrients2 = [
            ["Fat, total (g/100g)", 63],
            ["Fibre, total dietary (g/100g)", 20],
            ["Protein, total; calculated from total nitrogen (g/100g)", 52],
            ["Sugars, total (g/100g)", 325],
            ["Fatty acids, total saturated (g/100g)", 20],
            ["Sugar, added", 50],
            ["Cholesterol (mg/100g)", 300],
            ["Energy (kcal/100g)", 1900],
            ["Meat", 1],
            ["FruitVeg", 4],
            ["Vitamin C (mg/100g)", 70],
            ["Vitamin E, alpha-tocopherol equivalents (mg/100g)", 7.5],
            ["Calcium (mg/100g)", 1000],
            ["Sodium (mg/100g)", 2300],
            ["Iron (mg/100g)", 20],
            ["Zinc (mg/100g)", 4.6],
            ["Vitamin A, retinol equivalents (µg/100g)", 600],
            ["Vitamin D (μg/100g)", 15], #!!!
            ["Vitamin K (μg/100g)", 55],
            ["Manganese (μg/100g)", 1800],
            ["Fat, total (g/100g)", 53],
            ["Fibre, total dietary (g/100g)", 70],
            ["Sodium (mg/100g)", 1500],
            ["Condiment", 0.06]
        ]
    elif (gender == 'children'):
        nutrients2 = [
            ["Fat, total (g/100g)", 68],
            ["Fibre, total dietary (g/100g)", 20],
            ["Protein, total; calculated from total nitrogen (g/100g)", 23],
            ["Sugars, total (g/100g)", 325],
            ["Fatty acids, total saturated (g/100g)", 20],
            ["Sugar, added", 50],
            ["Cholesterol (mg/100g)", 300],
            ["Energy (kcal/100g)", 1750],
            ["Meat", 1],
            ["FruitVeg", 4],
            ["Vitamin C (mg/100g)", 35],
            ["Vitamin E, alpha-tocopherol equivalents (mg/100g)", 7],
            ["Calcium (mg/100g)", 1000],
            ["Sodium (mg/100g)", 2300],
            ["Iron (mg/100g)", 6],
            ["Zinc (mg/100g)", 5.7],
            ["Vitamin A, retinol equivalents (µg/100g)", 500],
            ["Vitamin D (μg/100g)", 15], #!!!
            ["Vitamin K (μg/100g)", 25],
            ["Manganese (μg/100g)", 1500],
            ["Fat, total (g/100g)", 49],
            ["Fibre, total dietary (g/100g)", 70],
            ["Sodium (mg/100g)", 1200],
            ["Condiment", 0.06]
        ]

    elif (gender == 'custom'):
        if (custom_calorie == 0):
            custom_calorie = 2190
        if (custom_max_fat == 0):
            custom_max_fat = 73
        if (custom_min_fat == 0):
            custom_min_fat = 61
        if (custom_protein == 0):
            custom_protein = 61
        if (custom_min_fibre == 0):
            custom_min_fibre = 20
        if (custom_max_fibre == 0):
            custom_max_fibre = 70
        if (custom_manga == 0):
            custom_manga = 2300
        if (custom_zinc == 0):
            custom_zinc = 6.5
        if (custom_iron == 0):
            custom_iron = 9
        if (custom_calc == 0):
            custom_calc = 1000
        if (custom_vitK == 0):
            custom_vitK = 65
        if (custom_vitE == 0):
            custom_vitE = 10
        if (custom_vitD == 0):
            custom_vitD = 15
        if (custom_vitC == 0):
            custom_vitC = 70
        if (custom_vitA == 0):
            custom_vitA = 600
        if (custom_fruit == 0):
            custom_fruit = 400
        if (custom_meat == 0):
            custom_meat = 100
        if (custom_chol == 0):
            custom_chol = 300
        if (custom_added_sugar == 0):
            custom_added_sugar = 50
        if (custom_sat_fat == 0):
            custom_sat_fat = 20
        if (custom_carb == 0):
            custom_carb = 325
        if (custom_max_sodium == 0):
            custom_max_sodium = 2300
        if (custom_min_sodium == 0):
            custom_min_sodium = 1500

        nutrients2 = [
           ["Fat, total (g/100g)", custom_max_fat],
           ["Fibre, total dietary (g/100g)", custom_min_fibre],
            ["Protein, total; calculated from total nitrogen (g/100g)", custom_protein],
            ["Sugars, total (g/100g)", custom_carb],
            ["Fatty acids, total saturated (g/100g)", custom_sat_fat],
            ["Sugar, added", custom_added_sugar],
            ["Cholesterol (mg/100g)", custom_chol],
            ["Energy (kcal/100g)", custom_calorie],
            ["Meat", (custom_meat/100)],
            ["FruitVeg", (custom_fruit/100)],
            ["Vitamin C (mg/100g)", custom_vitC],
            ["Vitamin E, alpha-tocopherol equivalents (mg/100g)", custom_vitE],
            ["Calcium (mg/100g)", custom_calc],
            ["Sodium (mg/100g)", custom_max_sodium],
            ["Iron (mg/100g)", custom_iron],
            ["Zinc (mg/100g)", custom_zinc],
            ["Vitamin A, retinol equivalents (µg/100g)", custom_vitA],
            ["Vitamin D (μg/100g)", custom_vitD], #!!!
            ["Vitamin K (μg/100g)", custom_vitK],
            ["Manganese (μg/100g)", custom_manga],
            ["Fat, total (g/100g)", custom_min_fat],
            ["Fibre, total dietary (g/100g)", custom_max_fibre],
            ["Sodium (mg/100g)", custom_min_sodium],
            ["Condiment", 0.06]
        ]

    # our data
    #data = df2.values.tolist()

    # Instantiate a Glop solver and naming it.
    solver = pywraplp.Solver('ZahirDiet',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Declare an array to hold our variables.
    # 0 lower bound, 2 upper bound (max 200 gram per food)
    foods = [solver.NumVar(0, 3, item[1]) for item in data]

    print('Number of variables =', solver.NumVariables())

    more = [ 1, 2, 7, 9, 10, 11, 12, 14,
        15, 16, 17, 18, 19, 20, 22 ] #index of constraints >=

    constraints = []
    print("Constraints:\n")

    for i, nutrient in enumerate(nutrients2):
        if (i in more):
            print('{} >= {:.2f}'.format(nutrient[0], nutrient[1]))
            constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
        else:
            print('{} <= {:.2f}'.format(nutrient[0], nutrient[1]))
            constraints.append(solver.Constraint(-solver.infinity(), nutrient[1]))

        for j, item in enumerate(data):
            constraints[i].SetCoefficient(foods[j], item[i + 3])

    print('\nNumber of constraints =', solver.NumConstraints())

    # Objective function: Minimize the sum of (price-normalized) foods.
    objective = solver.Objective()
    for i, food in enumerate(foods):
        objective.SetCoefficient(food, df2.loc[i]['Price (RM)'])
    objective.SetMinimization()

    status = solver.Solve()

    # Check that the problem has an optimal solution.
    if status != solver.OPTIMAL:
        print('The problem does not have an optimal solution!')
        if status == solver.FEASIBLE:
            print('A potentially suboptimal solution was found.')
        else:
            print('The solver could not solve the problem.')

    if status == solver.OPTIMAL:
        # Display the amounts (in dollars) to purchase of each food.
        nutrients_result = [0] * len(nutrients2)

        print('\nFoods:')
        price_table = []

        for i, food in enumerate(foods):
            if food.solution_value() > 0.0:
                price_table.append([data[i][1], food.solution_value()*100, food.solution_value()*data[i][2]])
                for j, _ in enumerate(nutrients2):
                    nutrients_result[j] += data[i][j + 3] * food.solution_value()

        print('\nOptimal price: RM{:.4f}'.format(objective.Value()))

        print('\nNutrients per day:')
        nutrient_table = []

        for i, nutrient in enumerate(nutrients2):
            if (i in more):
                nutrient_table.append([nutrient[0], '≥ ' + str(nutrient[1]), nutrients_result[i]])
            else:
                nutrient_table.append([nutrient[0], '≤ ' + str(nutrient[1]), nutrients_result[i]])

        column_names = ['Food', 'Weight (g)', 'Price (RM)']
        df_food = pd.DataFrame(price_table, columns = column_names)
        df_food = df_food.sort_values(by = ['Food'], ascending=[True]).reset_index(drop=True)
        df_food = df_food.round(2)

        column_names = ['Nutrient', 'Constraint', 'Current Diet Value']
        df_nutrient = pd.DataFrame(nutrient_table, columns = column_names)
        df_nutrient.loc[df_nutrient["Nutrient"] == "Fat, total (g/100g)", ["Nutrient"]] = "Total Fat (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Calcium (mg/100g)", ["Nutrient"]] = "Calcium (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Cholesterol (mg/100g)", ["Nutrient"]] = "Cholesterol (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Energy (kcal/100g)", ["Nutrient"]] = "Calories (kcal)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Fatty acids, total saturated (g/100g)", ["Nutrient"]] = "Total Sat. Fat (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Fibre, total dietary (g/100g)", ["Nutrient"]] = "Fibre (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "FruitVeg", ["Nutrient"]] = "Fruits & Vegetables (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Meat", ["Nutrient"]] = "Meat (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Vitamin K (μg/100g)", ["Nutrient"]] = "Vitamin K (μg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Vitamin E, alpha-tocopherol equivalents (mg/100g)", ["Nutrient"]] = "Vitamin E (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Vitamin D (μg/100g)", ["Nutrient"]] = "Vitamin D (μg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Iron (mg/100g)", ["Nutrient"]] = "Iron (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Sodium (mg/100g)", ["Nutrient"]] = "Sodium (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Sugar, added", ["Nutrient"]] = "Added Sugar (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Sugars, total (g/100g)", ["Nutrient"]] = "Carbohydrates (g)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Vitamin A, retinol equivalents (µg/100g)", ["Nutrient"]] = "Vitamin A (µg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Vitamin C (mg/100g)", ["Nutrient"]] = "Vitamin C (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Manganese (μg/100g)", ["Nutrient"]] = "Manganese (µg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Zinc (mg/100g)", ["Nutrient"]] = "Zinc (mg)"
        df_nutrient.loc[df_nutrient["Nutrient"] == "Protein, total; calculated from total nitrogen (g/100g)", ["Nutrient"]] = "Protein (g)"
        df_nutrient = df_nutrient.sort_values(by = ['Nutrient', 'Constraint'], ascending=[True, False]).reset_index(drop=True)
        df_nutrient = df_nutrient.round(2)

    try:
        df_food
    except NameError:
        df_food = ""

    try:
        df_nutrient
    except NameError:
        df_nutrient = ""

    return objective.Value(), df_food, df_nutrient
    

from .forms import CHOICES

def hello_world(request):
    obj_val = foods = nutrient = alert = diet_plan = nutrient_check = ""

    form = CHOICES(request.POST)
    selected = None

    if form.is_valid():
        selected = form.cleaned_data.get("NUMS")
        print(form)
        print(selected)

    gender = request.POST.get('gender', False)

    try:
        custom_calorie = float(request.POST.get('custom_calorie', False))
    except Exception as e:
        custom_calorie = 0

    try:
        custom_min_fat = float(request.POST.get('custom_min_fat', False))
    except Exception as e:
        custom_min_fat = 0

    try:
        custom_max_fat = float(request.POST.get('custom_max_fat', False))
    except Exception as e:
        custom_max_fat = 0

    try:
        custom_protein = float(request.POST.get('custom_protein', False))
    except Exception as e:
        custom_protein = 0

    try:
        custom_max_fibre = float(request.POST.get('custom_max_fibre', False))
    except Exception as e:
        custom_max_fibre = 0

    try:
        custom_min_fibre = float(request.POST.get('custom_min_fibre', False))
    except Exception as e:
        custom_min_fibre = 0

    try:
        custom_manga = float(request.POST.get('custom_manga', False))
    except Exception as e:
        custom_manga = 0

    try:
        custom_zinc = float(request.POST.get('custom_zinc', False))
    except Exception as e:
        custom_zinc = 0

    try:
        custom_iron = float(request.POST.get('custom_iron', False))
    except Exception as e:
        custom_iron = 0

    try:
        custom_calc = float(request.POST.get('custom_calc', False))
    except Exception as e:
        custom_calc = 0

    try:
        custom_vitK = float(request.POST.get('custom_vitK', False))
    except Exception as e:
        custom_vitK = 0

    try:
        custom_vitE = float(request.POST.get('custom_vitE', False))
    except Exception as e:
        custom_vitE = 0

    try:
        custom_vitD = float(request.POST.get('custom_vitD', False))
    except Exception as e:
        custom_vitD = 0

    try:
        custom_vitC = float(request.POST.get('custom_vitC', False))
    except Exception as e:
        custom_vitC = 0

    try:
        custom_vitA = float(request.POST.get('custom_vitA', False))
    except Exception as e:
        custom_vitA = 0

    try:
        custom_fruit = float(request.POST.get('custom_fruit', False))
    except Exception as e:
        custom_fruit = 0

    try:
        custom_meat = float(request.POST.get('custom_meat', False))
    except Exception as e:
        custom_meat = 0

    try:
        custom_chol = float(request.POST.get('custom_chol', False))
    except Exception as e:
        custom_chol = 0

    try:
        custom_added_sugar = float(request.POST.get('custom_added_sugar', False))
    except Exception as e:
        custom_added_sugar = 0

    try:
        custom_sat_fat = float(request.POST.get('custom_sat_fat', False))
    except Exception as e:
        custom_sat_fat = 0

    try:
        custom_max_sodium = float(request.POST.get('custom_max_sodium', False))
    except Exception as e:
        custom_max_sodium = 0

    try:
        custom_min_sodium = float(request.POST.get('custom_min_sodium', False))
    except Exception as e:
        custom_min_sodium = 0

    try:
        custom_carb = float(request.POST.get('custom_carb', False))
    except Exception as e:
        custom_carb = 0

    if (gender):
        obj_val, df_food, df_nutrient = calculate(gender,
            custom_calorie,
            custom_manga,
            custom_zinc,
            custom_iron,
            custom_calc,
            custom_vitK,
            custom_vitE,
            custom_vitD,
            custom_vitC,
            custom_vitA,
            custom_fruit,
            custom_meat,
            custom_chol,
            custom_added_sugar,
            custom_sat_fat,
            custom_carb,
            custom_protein,
            custom_max_sodium,
            custom_min_sodium,
            custom_max_fibre,
            custom_min_fibre,
            custom_max_fat,
            custom_min_fat
        )
        obj_val = 'Total (Optimal) Price: RM{:.2f}'.format(float(obj_val))
        alert = "alert-success"
        if (obj_val == "Total (Optimal) Price: RM0.00"):
            obj_val = "We could not find the best diet for you.\nPlease try different nutrient values."
            alert = "alert-danger"
        else:
            diet_plan = "Diet Plan:"
            nutrient_check = "Nutrients:"
    try:
        df_food
    except NameError:
        df_food = ""

    try:
        df_nutrient
    except NameError:
        df_nutrient = ""

    context = {
        'optimal': obj_val,
        'form': form,
        'foods': foods,
        'nutrient': nutrient,
        'alert': alert,
        'custom_calorie': custom_calorie,
        'df_food': df_food,
        'df_nutrient': df_nutrient,
        'diet_plan': diet_plan,
        'nutrient_check': nutrient_check
    }
    return render(request, 'hello_world.html', context)
