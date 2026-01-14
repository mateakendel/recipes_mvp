from elasticsearch import Elasticsearch
import time
import os

ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
INDEX_NAME = "recipes"

es = Elasticsearch(ES_HOST)


def wait_for_es():
    for _ in range(30):
        try:
            if es.ping():
                return
        except:
            pass
        time.sleep(1)
    raise RuntimeError("Elasticsearch not available")


def create_index():
    wait_for_es()

    if es.indices.exists(index=INDEX_NAME):
        return

    es.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "title": {"type": "text"},
                "ingredients": {"type": "text"},
                "steps": {"type": "text"},
                "category": {"type": "text"},
                "author": {"type": "keyword"},
                "prep_time": {"type": "integer"}
            }
        }
    )


def normalize_recipe(recipe):
    return {
        "title": recipe["title"].lower(),
        "ingredients": " ".join(i.lower() for i in recipe["ingredients"]),
        "steps": recipe["steps"].lower(),
        "category": recipe["category"].lower(),
        "author": recipe["author"],
        "prep_time": recipe.get("prep_time", 0)
    }


def index_recipe(recipe_id, recipe):
    es.index(
        index=INDEX_NAME,
        id=str(recipe_id),
        document=normalize_recipe(recipe),
        refresh=True  
    )


def search_recipes(q=None, category=None, max_time=None):
    must = []

    if q:
        must.append({
            "multi_match": {
                "query": q.lower(),
                "fields": ["title", "ingredients", "steps"]
            }
        })

    if category:
        must.append({"match": {"category": category.lower()}})

    if max_time is not None:
        must.append({"range": {"prep_time": {"lte": max_time}}})

    query = {"bool": {"must": must}} if must else {"match_all": {}}

    res = es.search(index=INDEX_NAME, query=query)

    return [
        {"_id": hit["_id"], **hit["_source"]}
        for hit in res["hits"]["hits"]
    ]
