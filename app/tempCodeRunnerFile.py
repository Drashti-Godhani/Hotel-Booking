import requests  # noqa: E402

response = requests.get("https://openrouter.ai/api/v1/models")
models = response.json()["data"]

for model in models:
    model_id = model["id"]
    pricing = model.get("pricing", {})

    if pricing.get("prompt") == "0" and pricing.get("completion") == "0":
        print(model_id)