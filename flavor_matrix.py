# ============================================================
# Healthy Bawarchi — Culture Flavor Matrix
# Core data layer: ingredients, flavor rules, cuisine profiles
# ============================================================

# ------------------------------------
# Curated affordable Pakistani ingredients (57 total)
# ------------------------------------
INDIGENOUS_INGREDIENTS = [
    "onion", "tomato", "garlic", "ginger", "green chilli", "red chilli",
    "cumin", "coriander", "turmeric", "garam masala", "black pepper",
    "mustard seeds", "fenugreek seeds", "ajwain (carom seeds)",
    "lentils (masoor dal)", "lentils (moong dal)", "chickpeas", "kidney beans",
    "potato", "spinach", "eggplant (baingan)", "bitter gourd (karela)",
    "bottle gourd (lauki)", "pumpkin", "cauliflower", "cabbage", "peas",
    "carrot", "radish", "turnip", "methi (fenugreek leaves)",
    "yogurt", "milk", "paneer", "eggs", "chicken", "beef", "mutton",
    "rice (basmati)", "wheat flour (atta)", "semolina (suji)", "bread (roti)",
    "tamarind", "lemon", "mint", "coriander leaves", "curry leaves",
    "sesame seeds", "poppy seeds", "coconut", "peanuts",
    "sugar", "jaggery (gur)", "salt", "oil", "ghee",
    "dried mango powder (amchur)", "chaat masala", "anardana (pomegranate seeds)"
]

# ------------------------------------
# Flavor Compatibility Rules
# ------------------------------------
FLAVOR_RULES = {
    "umami_base": ["onion", "tomato", "garlic", "ginger"],
    "heat_layer": ["green chilli", "red chilli", "black pepper", "garam masala"],
    "tang_layer": ["tamarind", "lemon", "dried mango powder (amchur)", "yogurt", "anardana (pomegranate seeds)"],
    "earthy_layer": ["cumin", "coriander", "turmeric", "fenugreek seeds"],
    "fresh_finish": ["mint", "coriander leaves", "lemon"],
    "protein_anchor": ["eggs", "chicken", "beef", "mutton", "lentils (masoor dal)", "chickpeas", "paneer"],
    "carb_base": ["rice (basmati)", "wheat flour (atta)", "potato", "semolina (suji)"],
    "crunch_element": ["peanuts", "sesame seeds", "poppy seeds"],
    "sweet_balance": ["jaggery (gur)", "sugar", "coconut", "pumpkin"],
}

# ------------------------------------
# Cuisine Profiles — Culture Flavor Matrix
# ------------------------------------
CUISINE_PROFILES = {
    "Pakistani": {
        "description": "Bold, aromatic, spice-forward. Uses cumin, coriander, garam masala, yogurt marinades, and slow-cooked techniques.",
        "signature_techniques": ["bhunna (dry-frying spices)", "dum (slow steam cooking)", "tarka (tempering oil with spices)"],
        "flavor_emphasis": ["umami_base", "heat_layer", "earthy_layer"],
        "avoid": [],
        "health_focus": "High-fiber legumes, anti-inflammatory spices (turmeric, cumin), low-GI vegetables",
    },
    "Chinese": {
        "description": "Balanced sweet-salty-umami. Uses soy-inspired flavors, quick stir-fry, and sesame. Adapted with local Pakistani ingredients.",
        "signature_techniques": ["stir-fry", "steaming", "quick saute"],
        "flavor_emphasis": ["umami_base", "crunch_element", "sweet_balance"],
        "avoid": ["garam masala", "turmeric"],
        "health_focus": "Light cooking methods, high vegetable content, minimal oil stir-fry",
    },
    "Italian": {
        "description": "Herb-forward, tomato-based, simple and fresh. Adapted using local ingredients like atta for pasta, paneer for cheese.",
        "signature_techniques": ["sauteing", "baking", "slow simmering"],
        "flavor_emphasis": ["umami_base", "fresh_finish", "tang_layer"],
        "avoid": ["garam masala", "cumin"],
        "health_focus": "Tomato-rich antioxidants, olive oil alternatives, high-fiber whole wheat atta pasta",
    },
    "Mexican": {
        "description": "Smoky, tangy, layered heat. Uses beans, tomato, chilli, and lime. Adapted with local Pakistani pantry staples.",
        "signature_techniques": ["roasting", "layering", "wrapping"],
        "flavor_emphasis": ["heat_layer", "tang_layer", "protein_anchor"],
        "avoid": [],
        "health_focus": "Bean-based protein, high fiber, gut-healthy fermented elements like yogurt as sour cream substitute",
    },
}

# ------------------------------------
# Nutritional reference (approximate kcal per 100g)
# Used as fallback when USDA API is unavailable.
# Sources: USDA FoodData Central SR Legacy approximations.
# ------------------------------------
CALORIE_REFERENCE = {
    # Proteins
    "chicken": 165,
    "beef": 250,
    "mutton": 294,
    "eggs": 155,
    "paneer": 265,
    # Legumes
    "lentils (masoor dal)": 116,
    "lentils (moong dal)": 105,
    "chickpeas": 164,
    "kidney beans": 127,
    # Vegetables
    "potato": 77,
    "spinach": 23,
    "eggplant (baingan)": 25,
    "bitter gourd (karela)": 17,
    "bottle gourd (lauki)": 14,
    "pumpkin": 26,
    "cauliflower": 25,
    "cabbage": 25,
    "peas": 81,
    "carrot": 41,
    "radish": 16,
    "turnip": 28,
    "methi (fenugreek leaves)": 49,
    "onion": 40,
    "tomato": 18,
    "garlic": 149,
    "ginger": 80,
    "green chilli": 40,
    "curry leaves": 108,
    # Dairy
    "yogurt": 61,
    "milk": 42,
    # Grains & starches
    "rice (basmati)": 130,
    "wheat flour (atta)": 340,
    "semolina (suji)": 360,
    "bread (roti)": 264,
    # Herbs & fresh
    "mint": 70,
    "coriander leaves": 23,
    "lemon": 29,
    # Dried / preserved
    "tamarind": 239,
    "dried mango powder (amchur)": 320,
    "anardana (pomegranate seeds)": 346,
    # Spices
    "cumin": 375,
    "coriander": 298,
    "turmeric": 354,
    "red chilli": 282,
    "black pepper": 251,
    "garam masala": 379,
    "mustard seeds": 508,
    "fenugreek seeds": 323,
    "ajwain (carom seeds)": 305,
    "chaat masala": 350,
    # Nuts & seeds
    "sesame seeds": 573,
    "poppy seeds": 525,
    "peanuts": 567,
    "coconut": 354,
    # Fats & sweeteners
    "oil": 884,
    "ghee": 900,
    "sugar": 387,
    "jaggery (gur)": 383,
    "salt": 0,
}


def get_flavor_profile_text(cuisine: str) -> str:
    """Return a formatted string of flavor rules for a given cuisine, for prompt injection."""
    profile = CUISINE_PROFILES.get(cuisine, CUISINE_PROFILES["Pakistani"])
    rules = FLAVOR_RULES

    emphasized = []
    for layer in profile["flavor_emphasis"]:
        ingredients = rules.get(layer, [])
        emphasized.append(f"  - {layer.replace('_', ' ').title()}: {', '.join(ingredients)}")

    avoid_str = (
        f"Avoid combining: {', '.join(profile['avoid'])}" if profile["avoid"]
        else "No specific ingredient restrictions."
    )

    return (
        f"Cuisine: {cuisine}\n"
        f"Description: {profile['description']}\n"
        f"Signature techniques: {', '.join(profile['signature_techniques'])}\n"
        f"Flavor emphasis layers:\n" + "\n".join(emphasized) + "\n"
        f"{avoid_str}\n"
        f"Health focus: {profile['health_focus']}"
    )
