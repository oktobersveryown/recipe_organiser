from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import get_database_connection


def index():
    if current_user.is_authenticated:
        conn = get_database_connection()
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE user_id = ? ORDER BY name", (current_user.id,)
        ).fetchall()
        conn.close()
        return render_template("index.html", recipes=recipes, show_public_search=False)
    else:
        return render_template("index.html", show_public_search=True)


def live_search_collected_recipes():
    search_query = request.args.get("query", "").strip()
    conn = get_database_connection()
    if search_query:
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE user_id = ? AND (name LIKE ? OR ingredients LIKE ? OR instructions LIKE ?) ORDER BY name",
            (
                current_user.id,
                f"%{search_query}%",
                f"%{search_query}%",
                f"%{search_query}%",
            ),
        ).fetchall()
    else:
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE user_id = ? ORDER BY name", (current_user.id,)
        ).fetchall()
    conn.close()
    return render_template("recipe_list_partial.html", recipes=recipes)


def add_recipe():
    if request.method == "POST":
        name = request.form["name"].strip()
        ingredients = request.form["ingredients"].strip()
        instructions = request.form["instructions"].strip()

        if not name or not ingredients or not instructions:
            flash("All fields are required!", "error")
        else:
            conn = get_database_connection()
            conn.execute(
                "INSERT INTO recipes (user_id, name, ingredients, instructions) VALUES (?, ?, ?, ?)",
                (current_user.id, name, ingredients, instructions),
            )
            conn.commit()
            conn.close()
            flash("Recipe added successfully!", "success")
            return redirect(url_for("index"))
    return render_template(
        "add_edit_recipe.html", recipe=None, form_title="Add New Recipe"
    )


def view_recipe(recipe_id):
    conn = get_database_connection()
    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id = ? AND user_id = ?",
        (recipe_id, current_user.id),
    ).fetchone()
    conn.close()

    if recipe is None:
        flash("Recipe not found or you do not have permission to view it!", "error")
        return redirect(url_for("index"))
    return render_template("view_recipe.html", recipe=recipe)


def edit_recipe(recipe_id):
    conn = get_database_connection()
    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id = ? AND user_id = ?",
        (recipe_id, current_user.id),
    ).fetchone()

    if recipe is None:
        conn.close()
        flash("Recipe not found or you do not have permission to edit it!", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form["name"].strip()
        ingredients = request.form["ingredients"].strip()
        instructions = request.form["instructions"].strip()

        if not name or not ingredients or not instructions:
            flash("All fields are required!", "error")
        else:
            conn.execute(
                "UPDATE recipes SET name = ?, ingredients = ?, instructions = ? WHERE id = ? AND user_id = ?",
                (name, ingredients, instructions, recipe_id, current_user.id),
            )
            conn.commit()
            flash("Recipe updated successfully!", "success")
            return redirect(url_for("view_recipe", recipe_id=recipe_id))
    conn.close()
    return render_template(
        "add_edit_recipe.html", recipe=recipe, form_title="Edit Recipe"
    )


def delete_recipe(recipe_id):
    conn = get_database_connection()
    cursor = conn.execute(
        "DELETE FROM recipes WHERE id = ? AND user_id = ?", (recipe_id, current_user.id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        flash("Recipe not found or you do not have permission to delete it!", "error")
    else:
        flash("Recipe deleted successfully!", "success")
    return redirect(url_for("index"))
