from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import joblib
import requests
import random

# ============================================================
# FASTAPI + CORS
# ============================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow React (5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 1. LOAD ML MODEL
# ============================================================

model = joblib.load("crop_model.pkl")
scaler = joblib.load("scaler.pkl")

def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    x = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])
    x_scaled = scaler.transform(x)
    crop = model.predict(x_scaled)[0]
    return crop


# ============================================================
# 2. SOIL DEFAULTS (BUILT-IN)
# ============================================================

soil_defaults = {
    # Punjab – very fertile, nitrogen rich
    "punjab":      {"N": 95, "P": 55, "K": 65, "ph": 7.3},

    # Haryana – similar but slightly less
    "haryana":     {"N": 85, "P": 50, "K": 55, "ph": 7.4},

    # Rajasthan – desert, low nutrients, alkaline soil
    "rajasthan":   {"N": 30, "P": 18, "K": 25, "ph": 8.2},

    # Gujarat – black soil & coastal mix
    "gujarat":     {"N": 60, "P": 40, "K": 80, "ph": 7.8},

    # Maharashtra – black cotton soil, high potassium
    "maharashtra": {"N": 65, "P": 30, "K": 95, "ph": 7.7},

    # Madhya Pradesh – medium black soil
    "madhya pradesh": {"N": 70, "P": 35, "K": 85, "ph": 7.5},

    # Bihar – alluvial soil, high fertility
    "bihar":       {"N": 65, "P": 45, "K": 90, "ph": 6.8},

    # Uttar Pradesh – alluvial, neutral pH
    "uttar pradesh": {"N": 70, "P": 48, "K": 72, "ph": 7.1},

    # West Bengal – alluvial but acidic zones
    "west bengal": {"N": 50, "P": 42, "K": 60, "ph": 6.2},

    # Odisha – red soil, low nitrogen
    "odisha":      {"N": 40, "P": 35, "K": 45, "ph": 5.9},

    # Andhra Pradesh – red sandy soil
    "andhra pradesh": {"N": 45, "P": 38, "K": 50, "ph": 6.3},

    # Telangana – mix of black & red soil
    "telangana":   {"N": 55, "P": 40, "K": 65, "ph": 7.0},

    # Karnataka – red soil, moderate nutrients
    "karnataka":   {"N": 52, "P": 37, "K": 48, "ph": 6.5},

    # Tamil Nadu – coastal & red soil mix
    "tamil nadu":  {"N": 48, "P": 35, "K": 42, "ph": 6.6},

    # Kerala – highly acidic soil
    "kerala":      {"N": 38, "P": 28, "K": 32, "ph": 5.2},

    # Northeast – highly acidic, high rainfall
    "assam":       {"N": 42, "P": 33, "K": 22, "ph": 5.4},

    # Himachal – mountain soils, acidic
    "himachal pradesh": {"N": 40, "P": 30, "K": 35, "ph": 5.7},

    # Jammu & Kashmir – mountain soil, alkaline patches
    "jammu kashmir": {"N": 55, "P": 32, "K": 40, "ph": 7.8},

    # Default fallback
    "default":     {"N": 60, "P": 45, "K": 40, "ph": 7.0},
}
# ============================================================
# 3. DISH DATABASE
# ============================================================

dish_df = pd.read_csv("Ifood_new.csv")
dish_df["ingredients_clean"] = (
    dish_df["ingredients"].str.lower().str.replace("[^a-z,]", "", regex=True)
)
dish_df["ingredient_list"] = dish_df["ingredients_clean"].str.split(",")
dish_df["ingredient_list"] = dish_df["ingredient_list"].apply(
    lambda x: [i.strip() for i in x]
)

def find_dish(crop):
    crop = crop.lower()
    matches = []
    for _, row in dish_df.iterrows():
        for ing in row["ingredient_list"]:
            if crop in ing:
                matches.append(row)
                break
    return pd.DataFrame(matches)


# ============================================================
# 4. NUTRITION DATABASE
# ============================================================

files = [
    "FOOD-DATA-GROUP1.csv",
    "FOOD-DATA-GROUP2.csv",
    "FOOD-DATA-GROUP3.csv",
    "FOOD-DATA-GROUP4.csv",
    "FOOD-DATA-GROUP5.csv",
]

nutr_df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
nutr_df = nutr_df.drop(columns=[c for c in nutr_df.columns if "Unnamed" in c], errors="ignore")
nutr_df["food"] = nutr_df["food"].str.lower().str.strip()

def get_nutr(ingredient):
    ingredient = ingredient.lower().strip()
    match = nutr_df[nutr_df["food"].str.contains(ingredient, na=False)]
    return None if match.empty else match.iloc[0]

def calculate_dish_nutrients(ingredients):
    total = {}
    for ing in ingredients:
        row = get_nutr(ing)
        if row is None:
            continue
        for col in nutr_df.columns:
            if col == "food":
                continue
            total[col] = total.get(col, 0) + row[col]
    return total


# ============================================================
# 5. Convert numpy → python
# ============================================================

def to_native(x):
    if isinstance(x, (np.integer, np.floating)):
        return x.item()
    return x


# ============================================================
# 6. FINAL ENDPOINT — random dish
# ============================================================

@app.get("/auto_predict")
def auto_predict(city: str):

    city = city.lower().strip()

    # Step 1 → Get Lat/Lon
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    ).json()

    if "results" not in geo or len(geo["results"]) == 0:
        return {"error": "City not found"}

    lat = float(geo["results"][0]["latitude"])
    lon = float(geo["results"][0]["longitude"])

    # Step 2 → Weather
    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true&"
        f"hourly=relativehumidity_2m&daily=rain_sum"
    ).json()

    temperature = float(weather["current_weather"]["temperature"])
    humidity = float(weather["hourly"]["relativehumidity_2m"][0])
    rainfall = float(weather["daily"]["rain_sum"][0])

    # Step 3 → Soil
    soil = soil_defaults.get(city, soil_defaults["default"])
    N, P, K, ph = soil["N"], soil["P"], soil["K"], soil["ph"]

    # Step 4 → Predict crop
    crop = str(predict_crop(N, P, K, temperature, humidity, ph, rainfall))

    # Step 5 → Random dish
    dishes = find_dish(crop)

    if dishes.empty:
        return {"crop": crop, "dish": None, "nutrition": None}

    dish_row = dishes.sample(1).iloc[0]  # RANDOM CHOICE

    dish_name = str(dish_row["name"])
    ingredients = [str(i) for i in dish_row["ingredient_list"]]

    nutrition_raw = calculate_dish_nutrients(ingredients)
    nutrition = {k: to_native(v) for k, v in nutrition_raw.items()}

    # Final response
    return {
        "city": city,
        "lat": lat,
        "lon": lon,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "N": N,
        "P": P,
        "K": K,
        "ph": ph,
        "crop": crop,
        "dish": dish_name,
        "ingredients": ingredients,
        "nutrition": nutrition,
    }
