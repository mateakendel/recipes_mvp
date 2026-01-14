from flask import Blueprint, request, jsonify
from app.db import recipes
from bson.objectid import ObjectId
from app.search import create_index, index_recipe, search_recipes

recipes_bp = Blueprint("recipes", __name__)

create_index()


@recipes_bp.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.json

    recipe = {
        "title": data["title"],
        "ingredients": data["ingredients"],
        "steps": data["steps"],
        "category": data["category"],
        "author": data["author"],
        "prep_time": int(data.get("prep_time", 0)),
        "published": True
    }

    result = recipes.insert_one(recipe)

    index_recipe(str(result.inserted_id), recipe)

    return {"message": "Recipe added"}, 201


@recipes_bp.route("/recipes", methods=["GET"])
def get_recipes():
    mode = request.args.get("mode", "all")
    user = request.args.get("user")

    query = {"author": user} if mode == "mine" else {"published": True}

    out = []
    for r in recipes.find(query):
        r["_id"] = str(r["_id"])
        out.append(r)

    return jsonify(out)


@recipes_bp.route("/recipes/search", methods=["GET"])
def search():
    return jsonify(
        search_recipes(
            q=request.args.get("q"),
            category=request.args.get("category"),
            max_time=int(request.args["time"]) if request.args.get("time") else None
        )
    )


@recipes_bp.route("/recipes/reindex", methods=["POST"])
def reindex_all():
    count = 0

    for r in recipes.find({"published": True}):
        recipe_id = str(r["_id"])
        doc = {
            "title": r["title"],
            "ingredients": r["ingredients"],
            "steps": r["steps"],
            "category": r["category"],
            "author": r["author"],
            "prep_time": r.get("prep_time", 0)
        }
        index_recipe(recipe_id, doc)
        count += 1

    return {"message": f"Reindexed {count} recipes"}, 200


@recipes_bp.route("/recipes/<recipe_id>")
def recipe_detail(recipe_id):
    recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    if not recipe:
        return {"message": "Not found"}, 404

    recipe["_id"] = str(recipe["_id"])
    return jsonify(recipe)
