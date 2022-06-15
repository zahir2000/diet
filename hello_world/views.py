from django.shortcuts import render
import pandas as pd
from ortools.linear_solver import pywraplp

def calculate(gender):
    df = pd.read_excel("C:\\Users\\Zahir\\Desktop\\NutrientsTest.xlsx")
    columns3 = []
    columns3.append("Category")
    columns3.append("Food Name")
    columns3.append("Price (RM)")
    columns3.append("Energy (kcal/100g)")
    columns3.append("Sugars, total (g/100g)")
    columns3.append("Fatty acids, total saturated (g/100g)")
    columns3.append("Fat, total (g/100g)")
    columns3.append("Cholesterol (mg/100g)")
    columns3.append("Protein, total; calculated from total nitrogen (g/100g)")
    columns3.append("Fibre, total dietary (g/100g)")
    columns3.append("Vitamin C (mg/100g)")
    columns3.append("Calcium (mg/100g)")
    columns3.append("Sodium (mg/100g)")
    columns3.append("Sugar, added")
    columns3

    df2 = df[df.columns.intersection(columns3)]
    df2.values.tolist()

    # Nutrient constraints.
    if (gender == "male"):
        nutrients2 = [
            ["Energy (kcal/100g)", 2190],
            ["Sugars, total (g/100g)", 325],
            ["Fatty acids, total saturated (g/100g)", 20],
            ["Fat, total (g/100g)", 73],
            ["Cholesterol (mg/100g)", 300],
            ["Protein, total; calculated from total nitrogen (g/100g)", 61],
            ["Fibre, total dietary (g/100g)", 20],
            ["Vitamin C (mg/100g)", 70],
            ["Calcium (mg/100g)", 1000],
            ["Sodium (mg/100g)", 2300],
            ["Sugar, added", 50],
        ]
    else:
        nutrients2 = [
            ["Energy (kcal/100g)", 2190],
            ["Sugars, total (g/100g)", 325],
            ["Fatty acids, total saturated (g/100g)", 20],
            ["Fat, total (g/100g)", 63],
            ["Cholesterol (mg/100g)", 300],
            ["Protein, total; calculated from total nitrogen (g/100g)", 61],
            ["Fibre, total dietary (g/100g)", 20],
            ["Vitamin C (mg/100g)", 70],
            ["Calcium (mg/100g)", 1000],
            ["Sodium (mg/100g)", 2300],
            ["Sugar, added", 50],
        ]

    # our data
    data = df2.values.tolist()

    # Instantiate a Glop solver and naming it.
    solver = pywraplp.Solver('ZahirDiet',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Declare an array to hold our variables.
    # 0 lower bound, 2 upper bound (max 200 gram per food)
    foods = [solver.NumVar(0, 2, item[1]) for item in data]

    print('Number of variables =', solver.NumVariables())

    more = [ 0, 5, 6, 7, 8 ] #index of constraints >=
    less = [ 1, 2, 3, 4, 9, 10 ] #index of constraints <=

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
            exit(1)

    # Display the amounts (in dollars) to purchase of each food.
    nutrients_result = [0] * len(nutrients2)
    print('\nFoods:')

    str_foods = []
    str_nutrient = []

    for i, food in enumerate(foods):
        if food.solution_value() > 0.0:
            print('{:.0f} gram @ RM{:.2f} for {}'.format(food.solution_value()*100,
                                                         food.solution_value()*data[i][2],
                                                         data[i][1]))
            str_foods.append('{:.0f} gram @ RM{:.2f} for {}'.format(food.solution_value()*100,
                                                         food.solution_value()*data[i][2],
                                                         data[i][1]))
            for j, _ in enumerate(nutrients2):
                nutrients_result[j] += data[i][j + 3] * food.solution_value()

    print('\nOptimal price: RM{:.4f}'.format(objective.Value()))

    print('\nNutrients per day:')
    for i, nutrient in enumerate(nutrients2):
        if (i in more):
            print('{}: {:.2f} (min {})'.format(nutrient[0], nutrients_result[i],
                                           nutrient[1]))
            str_nutrient.append('{}: {:.2f} (min {})'.format(nutrient[0], nutrients_result[i],
                                           nutrient[1]))
        else:
            print('{}: {:.2f} (max {})'.format(nutrient[0], nutrients_result[i],
                                           nutrient[1]))
            str_nutrient.append('{}: {:.2f} (max {})'.format(nutrient[0], nutrients_result[i],
                                           nutrient[1]))

    return objective.Value(), str_foods, str_nutrient
    

from .forms import CHOICES

def hello_world(request):
    obj_val = ""
    foods = ""
    nutrient = ""
    alert = ""

    form = CHOICES(request.POST)
    selected = None

    if form.is_valid():
        selected = form.cleaned_data.get("NUMS")
        print(form)
        print(selected)
    
    gender = request.POST.get('gender', False)    
    if (gender):
        obj_val, foods, nutrient = calculate(gender)
        obj_val = 'Optimal Price: RM{:.2f}'.format(float(obj_val))
        alert = "alert-success"

    context = {
        'optimal': obj_val,
        'form': form,
        'foods': foods,
        'nutrient': nutrient,
        'alert': alert
    }
    return render(request, 'hello_world.html', context)
