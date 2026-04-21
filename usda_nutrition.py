# ============================================================
# Healthy Bawarchi — USDA FoodData Central Nutrition Lookup
# Live nutritional data with Pakistani ingredient name mapping
# ============================================================

import re
import requests
import streamlit as st
from flavor_matrix import CALORIE_REFERENCE

# ------------------------------------
# USDA API configuration
# ------------------------------------
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Nutrient IDs in USDA FoodData Central
NUTRIENT_IDS = {
    "calories": 1008,   # Energy (kcal)
    "protein":  1003,   # Protein (g)
    "carbs":    1005,   # Carbohydrate, by difference (g)
    "fat":      1004,   # Total lipid (fat) (g)
    "fiber":    1079,   # Fiber, total dietary (g)
}

# ------------------------------------
# Pakistani ingredient name → USDA search term mapping
# Covers all 59 INDIGENOUS_INGREDIENTS + common user-typed variants
# ------------------------------------
USDA_NAME_MAP = {
    # Legumes
    "lentils (masoor dal)":         "lentils raw",
    "lentils (moong dal)":          "mung beans raw",
    "chickpeas":                    "chickpeas raw",
    "kidney beans":                 "kidney beans raw",
    # Grains & starches
    "wheat flour (atta)":           "whole wheat flour",
    "rice (basmati)":               "white rice long grain raw",
    "semolina (suji)":              "semolina unenriched",
    "bread (roti)":                 "whole wheat bread",
    # Vegetables
    "eggplant (baingan)":           "eggplant raw",
    "bitter gourd (karela)":        "balsam pear bitter melon raw",
    "bottle gourd (lauki)":         "gourd white flowered raw",
    "methi (fenugreek leaves)":     "fenugreek leaves raw",
    "pumpkin":                      "pumpkin raw",
    "cauliflower":                  "cauliflower raw",
    "cabbage":                      "cabbage raw",
    "spinach":                      "spinach raw",
    "potato":                       "potato raw",
    "peas":                         "peas green raw",
    "carrot":                       "carrots raw",
    "radish":                       "radishes raw",
    "turnip":                       "turnips raw",
    "onion":                        "onions raw",
    "tomato":                       "tomatoes raw",
    "garlic":                       "garlic raw",
    "ginger":                       "ginger root raw",
    "green chilli":                 "peppers hot chili green raw",
    "curry leaves":                 "curry leaves raw",
    # Herbs & fresh
    "mint":                         "spearmint fresh",
    "coriander leaves":             "coriander cilantro leaves raw",
    "lemon":                        "lemon juice raw",
    # Proteins
    "chicken":                      "chicken broilers or fryers meat only raw",
    "beef":                         "beef ground raw",
    "mutton":                       "lamb ground raw",
    "eggs":                         "egg whole raw",
    "paneer":                       "cheese cottage lowfat",
    # Dairy
    "yogurt":                       "yogurt plain whole milk",
    "milk":                         "milk whole 3.25 milkfat",
    # Dried / preserved
    "tamarind":                     "tamarind raw",
    "dried mango powder (amchur)":  "mango raw",
    "anardana (pomegranate seeds)": "pomegranate raw",
    # Spices
    "cumin":                        "cumin seed",
    "coriander":                    "coriander seed",
    "turmeric":                     "turmeric ground",
    "red chilli":                   "chili powder",
    "black pepper":                 "pepper black",
    "garam masala":                 "spices garam masala",
    "mustard seeds":                "mustard seed yellow",
    "fenugreek seeds":              "fenugreek seed",
    "ajwain (carom seeds)":         "carom seeds",
    "chaat masala":                 "spices mixed",
    # Nuts & seeds
    "sesame seeds":                 "sesame seeds whole dried",
    "poppy seeds":                  "seeds poppy",
    "peanuts":                      "peanuts raw",
    "coconut":                      "coconut meat raw",
    # Fats & sweeteners
    "oil":                          "oil vegetable",
    "ghee":                         "butter clarified",
    "sugar":                        "sugar granulated",
    "jaggery (gur)":                "sugars brown",
    "salt":                         "salt table",
}

# ------------------------------------
# Unit → grams conversion table
# Covers common cooking measurements
# ------------------------------------
UNIT_TO_GRAMS = {
    # Weight
    "g": 1.0, "gram": 1.0, "grams": 1.0,
    "kg": 1000.0, "kilogram": 1000.0,
    "mg": 0.001,
    "oz": 28.35, "ounce": 28.35, "ounces": 28.35,
    "lb": 453.6, "pound": 453.6,
    # Volume (approximate for water-density foods)
    "ml": 1.0, "milliliter": 1.0, "milliliters": 1.0,
    "l": 1000.0, "liter": 1000.0,
    "cup": 240.0, "cups": 240.0,
    "tbsp": 15.0, "tablespoon": 15.0, "tablespoons": 15.0,
    "tsp": 5.0, "teaspoon": 5.0, "teaspoons": 5.0,
    # Counts (approximate gram equivalents)
    "piece": 50.0, "pieces": 50.0,
    "slice": 30.0, "slices": 30.0,
    "clove": 5.0, "cloves": 5.0,
    "bunch": 100.0,
    "handful": 30.0,
    "pinch": 0.5,
    "medium": 100.0,
    "large": 150.0,
    "small": 60.0,
}

# Default gram assumption when unit is unrecognised
DEFAULT_GRAMS = 100.0


def _parse_quantity_to_grams(quantity_str: str) -> float:
    """
    Parse a quantity string like '2 tbsp', '100g', '1 cup', '3 medium'
    into an approximate gram weight.
    Returns DEFAULT_GRAMS (100g) if parsing fails.
    """
    if not quantity_str:
        return DEFAULT_GRAMS

    q = quantity_str.lower().strip()

    # Pattern: number (int or float) followed by optional unit
    match = re.match(r"([\d]+(?:[./][\d]+)?)\s*([a-z]*)", q)
    if not match:
        return DEFAULT_GRAMS

    num_str, unit = match.group(1), match.group(2).strip()

    # Handle fractions like 1/2
    try:
        if "/" in num_str:
            parts = num_str.split("/")
            number = float(parts[0]) / float(parts[1])
        else:
            number = float(num_str)
    except (ValueError, ZeroDivisionError):
        return DEFAULT_GRAMS

    gram_factor = UNIT_TO_GRAMS.get(unit, None)
    if gram_factor is None:
        # Unit not recognised — assume grams if no unit, else default
        gram_factor = 1.0 if unit == "" else DEFAULT_GRAMS / number if number > 0 else DEFAULT_GRAMS

    return number * gram_factor


def _get_usda_search_term(ingredient_name: str) -> str:
    """Map a Pakistani ingredient name to a USDA-friendly search term."""
    name_lower = ingredient_name.lower().strip()
    # Direct map lookup
    if name_lower in USDA_NAME_MAP:
        return USDA_NAME_MAP[name_lower]
    # Partial match — check if any map key is contained in the ingredient name
    for key, usda_term in USDA_NAME_MAP.items():
        if key in name_lower or name_lower in key:
            return usda_term
    # Fall back to the raw name
    return name_lower


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_usda_nutrition(ingredient_name: str, usda_api_key: str) -> dict | None:
    """
    Fetch nutrition per 100g for a given ingredient from USDA FoodData Central.
    Returns dict with keys: calories, protein, carbs, fat, fiber (all per 100g).
    Returns None on failure (triggers fallback).
    Cached for 24 hours to avoid redundant API calls.
    """
    search_term = _get_usda_search_term(ingredient_name)

    try:
        response = requests.get(
            USDA_BASE_URL,
            params={
                "query": search_term,
                "dataType": "Foundation,SR Legacy",
                "pageSize": 1,
                "api_key": usda_api_key,
            },
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()

        foods = data.get("foods", [])
        if not foods:
            return None

        food = foods[0]
        nutrients = {n["nutrientId"]: n["value"] for n in food.get("foodNutrients", [])}

        result = {}
        for key, nid in NUTRIENT_IDS.items():
            result[key] = round(nutrients.get(nid, 0.0), 2)

        return result

    except Exception:
        return None


def _fallback_nutrition(ingredient_name: str) -> dict:
    """
    Fallback: use CALORIE_REFERENCE for calories only.
    Other macros set to None (displayed as N/A in UI).
    """
    name_lower = ingredient_name.lower().strip()
    cal = CALORIE_REFERENCE.get(name_lower, None)
    return {
        "calories": cal,
        "protein": None,
        "carbs": None,
        "fat": None,
        "fiber": None,
        "source": "estimated",
    }


def calculate_recipe_nutrition(
    ingredients: list[dict],
    servings: int,
    usda_api_key: str,
) -> dict:
    """
    Calculate per-serving nutrition for a full recipe.

    Args:
        ingredients: List of dicts with keys 'item' and 'quantity'
                     (as returned by GPT JSON output).
        servings: Number of servings the recipe makes.
        usda_api_key: USDA FoodData Central API key.

    Returns:
        dict with keys: calories, protein, carbs, fat, fiber (per serving),
        source ('usda', 'mixed', or 'estimated'),
        usda_count (number of ingredients successfully looked up via USDA).
    """
    if servings < 1:
        servings = 1

    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0, "fiber": 0.0}
    usda_count = 0
    estimated_count = 0
    has_none = False  # tracks if any macro is missing

    for ing in ingredients:
        item = ing.get("item", "")
        quantity_str = ing.get("quantity", "")

        grams = _parse_quantity_to_grams(quantity_str)

        # Try USDA first
        usda_data = fetch_usda_nutrition(item, usda_api_key)

        if usda_data:
            nutrition_per_100g = usda_data
            source = "usda"
            usda_count += 1
        else:
            nutrition_per_100g = _fallback_nutrition(item)
            source = "estimated"
            estimated_count += 1

        # Scale from per-100g to actual quantity used
        scale = grams / 100.0
        for macro in ["calories", "protein", "carbs", "fat", "fiber"]:
            val = nutrition_per_100g.get(macro)
            if val is not None:
                totals[macro] += val * scale
            else:
                has_none = True

    # Divide by servings
    per_serving = {
        macro: round(total / servings, 1) for macro, total in totals.items()
    }

    # Determine overall source label
    if estimated_count == 0:
        overall_source = "usda"
    elif usda_count == 0:
        overall_source = "estimated"
    else:
        overall_source = "mixed"

    per_serving["source"] = overall_source
    per_serving["usda_count"] = usda_count
    per_serving["total_ingredients"] = len(ingredients)
    per_serving["has_incomplete_macros"] = has_none

    return per_serving


def format_nutrition_source_note(nutrition: dict) -> str:
    """Return a short human-readable source note for display in the UI."""
    source = nutrition.get("source", "estimated")
    usda_n = nutrition.get("usda_count", 0)
    total_n = nutrition.get("total_ingredients", 0)

    if source == "usda":
        return "USDA sourced ✓"
    elif source == "mixed":
        return f"USDA sourced ({usda_n}/{total_n} ingredients) ✓"
    else:
        return "AI estimated ~"
