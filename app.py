from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate daily calorie needs
def calculate_calories(age, weight, height, activity, goal):
    # Basic Basal Metabolic Rate (BMR) Calculation (Mifflin-St Jeor Equation)
    bmr = 10 * weight + 6.25 * height - 5 * age + 5  # For males (use -161 for females)

    # Activity multipliers
    activity_levels = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }

    # Adjust for activity level
    cal_needs = bmr * activity_levels.get(activity, 1.2)

    # Adjust for goal (lose/gain weight)
    if goal == "lose":
        cal_needs -= 500  # 500 kcal deficit per day
    elif goal == "gain":
        cal_needs += 500  # 500 kcal surplus per day

    return round(cal_needs)

# Function to generate a simple meal plan
def generate_meal_plan(calories):
    meals = [
        f"Breakfast: Scrambled eggs with toast - {round(calories * 0.3)} kcal",
        f"Lunch: Grilled chicken with quinoa and veggies - {round(calories * 0.4)} kcal",
        f"Dinner: Salmon with brown rice and salad - {round(calories * 0.3)} kcal"
    ]
    return meals

# Flask Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        age = int(request.form["age"])
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        activity = request.form["activity"]
        goal = request.form["goal"]

        # Calculate calories and meal plan
        daily_calories = calculate_calories(age, weight, height, activity, goal)
        meal_plan = generate_meal_plan(daily_calories)

        return render_template("index.html", cal=daily_calories, meal_plan=meal_plan)

    return render_template("index.html", cal=None, meal_plan=None)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
