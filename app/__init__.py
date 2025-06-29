from flask import Flask
from flask_login import LoginManager, login_required
from database import init_database
from .auth import User, load_user, login, register, logout
from .recipes import (
    index,
    live_search_collected_recipes,
    add_recipe,
    view_recipe,
    edit_recipe,
    delete_recipe,
)
from .public_api import (
    search_public_recipes,
    public_recipe_detail,
    import_public_recipe,
)


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
)

# --- Flask-Login setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.user_loader(load_user)


# --- Database Initialization ---
with app.app_context():
    init_database()

# --- Authentication Routes ---
app.add_url_rule("/register", "register", register, methods=["GET", "POST"])
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", logout, methods=["GET"])

# --- Recipe Management Routes ---
app.add_url_rule("/", "index", index, methods=["GET"])
app.add_url_rule(
    "/live_search_collected_recipes",
    "live_search_collected_recipes",
    login_required(live_search_collected_recipes),
    methods=["GET"],
)
app.add_url_rule(
    "/add", "add_recipe", login_required(add_recipe), methods=["GET", "POST"]
)
app.add_url_rule(
    "/recipe/<int:recipe_id>",
    "view_recipe",
    login_required(view_recipe),
    methods=["GET"],
)
app.add_url_rule(
    "/edit/<int:recipe_id>",
    "edit_recipe",
    login_required(edit_recipe),
    methods=["GET", "POST"],
)
app.add_url_rule(
    "/delete/<int:recipe_id>",
    "delete_recipe",
    login_required(delete_recipe),
    methods=["POST"],
)

# --- Public API Routes ---
app.add_url_rule(
    "/search_public_recipes",
    "search_public_recipes",
    search_public_recipes,
    methods=["POST"],
)
app.add_url_rule(
    "/public_recipe_detail/<string:meal_id>",
    "public_recipe_detail",
    public_recipe_detail,
    methods=["GET"],
)
app.add_url_rule(
    "/import_public_recipe/<string:meal_id>",
    "import_public_recipe",
    login_required(import_public_recipe),
    methods=["POST"],
)


if __name__ == "__main__":
    app.run(debug=False)
