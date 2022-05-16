import os
import time

import requests
from deta import Deta, app

X_RAPIDAPI_KEY = os.environ["X_RAPIDAPI_KEY"]
DETA_PROJECT_KEY = os.environ["DETA_PROJECT_KEY"]


@app.lib.cron()
def sync_recipes(event):
    start_time = time.time()
    url = "https://random-recipes.p.rapidapi.com/ai-quotes/2199"
    headers = {
        "X-RapidAPI-Host": "random-recipes.p.rapidapi.com",
        "X-RapidAPI-Key": X_RAPIDAPI_KEY,
    }
    response = requests.request("GET", url, headers=headers)
    recipes = response.json()

    deta = Deta(DETA_PROJECT_KEY)
    db = deta.Base("recipes")
    for recipe in recipes:
        id = recipe.pop("id")
        data = {
            "title": recipe["title"].lower(),
            "ingredients": ("-INGREDIENT-").join(recipe["ingredients"]),
            "steps": ("-STEP-").join([item["text"] for item in recipe["instructions"]]),
            "image": recipe["image"],
        }
        db.put(data, str(id))

    print(f"execution time {time.time() - start_time} seconds.")
