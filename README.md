# Recipe Collector/Organiser

A simple web application to collect, organise, and manage your favorite recipes. You can add your own recipes or search for public recipes using the free [TheMealDB API](https://www.themealdb.com/). This makes it easy to discover new dishes and keep all your culinary ideas in one place.

## Features

- Add, edit, and delete your own recipes.
- Search and import public recipes from TheMealDB API.
- Organise recipes for easy access.

## Setup

1. Create a virtual environment:
    - `python -m venv venv` or `python3 -m venv venv`
2. Install dependencies:
    - `pip install -r requirements.txt`

### Activating the Virtual Environment

#### Windows
- `.\venv\Scripts\activate` or `./venv/bin/activate.ps1`

#### Linux/macOS/Unix
- `source venv/bin/activate`

## Run

Start the Flask development server:
- `flask run` or `flask run --debug`

Visit [http://localhost:5000](http://localhost:5000) in your browser to use the app.

## Notes

- The app uses [TheMealDB API](https://www.themealdb.com/) for fetching public recipes.
- All your own recipes are stored locally.

## TODO
- [x] Add theme support for the application.
- [x] Implement dark mode for improved night-time usability.
- [ ] Implement a better light mode for better readability in bright environments.
- [x] Add a toggle or automatic switching between dark and light modes.
- [x] Ensure theme settings persist across sessions.

Feel free to contribute or suggest improvements!