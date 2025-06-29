import requests
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import get_database_connection


def search_public_recipes():
    search_query = request.form.get("query").strip()
    meal_results = []
    if search_query:
        api_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search_query}"
        response = requests.get(api_url)
        data = response.json()
        meal_results = data.get("meals", [])

        if not meal_results:
            flash(f"No public recipes found for '{search_query}'.", "info")
    else:
        flash("Please enter a search query.", "error")

    return render_template(
        "public_recipe_list_partial.html",
        query=search_query,
        meal_results=meal_results,
        current_user=current_user,
    )


def public_recipe_detail(meal_id):
    api_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(api_url)
    data = response.json()
    meal = data.get("meals", [])[0] if data.get("meals") else None

    if meal:
        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():
                ingredients.append(
                    f"{ingredient.strip()} - {measure.strip()}"
                    if measure and measure.strip()
                    else ingredient.strip()
                )

        meal["parsed_ingredients"] = "\n".join(ingredients)

        return render_template("view_public_recipe.html", meal=meal)
    else:
        flash("Public recipe not found.", "error")
        return redirect(url_for("index"))


def import_public_recipe(meal_id):
    api_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(api_url)
    data = response.json()
    meal = data.get("meals", [])[0] if data.get("meals") else None

    if meal:
        name = meal.get("strMeal", "Imported Recipe")

        ingredients = []
        for i in range(1, 21):
            ingredient = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ingredient and ingredient.strip():
                ingredients.append(
                    f"{ingredient.strip()} - {measure.strip()}"
                    if measure and measure.strip()
                    else ingredient.strip()
                )
        ingredients_str = "\n".join(ingredients)

        instructions = meal.get("strInstructions", "No instructions provided.")
        image_url = meal.get("strMealThumb")
        video_url = meal.get("strYoutube")

        conn = get_database_connection()
        conn.execute(
            "INSERT INTO recipes (user_id, name, ingredients, instructions, image_url, video_url) VALUES (?, ?, ?, ?, ?, ?)",
            (current_user.id, name, ingredients_str, instructions, image_url, video_url),
        )
        conn.commit()
        conn.close()
        flash(f'Recipe "{name}" imported successfully to your collection!', "success")
        return redirect(url_for("index"))
    else:
        flash("Could not import recipe. Details not found.", "error")
        return redirect(url_for("search_public_recipes"))
