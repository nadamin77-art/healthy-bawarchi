# ============================================================
# Healthy Bawarchi — AI Recipe Engine
# GPT-4o-mini calls with structured JSON output + Urdu fields
# ============================================================

import json
import base64
import openai
import streamlit as st
from flavor_matrix import CUISINE_PROFILES, FLAVOR_RULES, INDIGENOUS_INGREDIENTS, get_flavor_profile_text

# ------------------------------------
# JSON Schema description injected into system prompt
# ------------------------------------
RECIPE_JSON_SCHEMA = """
You MUST return a single valid JSON object with EXACTLY these fields (no extras, no markdown):

{
  "recipe_name": "Creative English name for the dish",
  "recipe_name_ur": "تخلیقی اردو نام",
  "description": "One-line poetic English description",
  "description_ur": "ایک سطری اردو تفصیل",
  "cuisine": "Pakistani | Chinese | Italian | Mexican",
  "prep_time_min": <integer>,
  "cook_time_min": <integer>,
  "servings": <integer>,
  "ingredients": [
    {
      "item": "ingredient name in English",
      "item_ur": "اجزاء کا اردو نام",
      "quantity": "amount with unit e.g. 100g, 2 tbsp, 1 cup",
      "price_pkr": <integer estimate in Pakistani Rupees>
    }
  ],
  "instructions": [
    "Step 1: Clear English instruction.",
    "Step 2: ..."
  ],
  "instructions_ur": [
    "مرحلہ 1: واضح اردو ہدایت۔",
    "مرحلہ 2: ..."
  ],
  "health_tips": "2-3 sentences on why this recipe is healthy (English).",
  "health_tips_ur": "2-3 جملے اس ریسیپی کے صحت کے فوائد پر (اردو)۔",
  "serving_suggestions": "English serving suggestion.",
  "serving_suggestions_ur": "اردو میں پیش کرنے کا مشورہ۔",
  "sustainability_tip": "One English sentence on food waste reduction or local sourcing.",
  "sustainability_tip_ur": "کھانے کے ضیاع میں کمی یا مقامی اجزاء پر ایک اردو جملہ۔",
  "closing_remark": "A short fun closing in Hinglish/Urdu mix e.g. 'Bilkul easy hai, try karo!'"
}

CRITICAL RULES:
- Return ONLY the JSON object. No markdown, no code fences, no explanation before or after.
- All string values must be properly escaped JSON strings.
- "instructions" and "instructions_ur" must have the SAME number of steps.
- "quantity" must always include a unit (g, tbsp, cup, tsp, piece, etc.).
- Do NOT include a "nutrition_per_serving" field — nutrition is calculated separately.
"""

# ------------------------------------
# System Prompt — Bawarchi AI persona
# ------------------------------------
SYSTEM_PROMPT = f"""
You are "Bawarchi AI" — a creative nutritionist and culinary inventor for Healthy Bawarchi,
a smart recipe app designed for Pakistani users who want healthy, affordable, and
sustainable meal ideas.

Your personality: warm, encouraging, creative, and practical. You think like a nutritionist
but cook like a street food innovator. You are fluent in both English and Urdu.

## Your Core Rules:
1. ALWAYS invent a NOVEL recipe — never suggest a standard dish. Give it a creative name.
2. Use ONLY the ingredients the user provides. You may add 1-2 small pantry staples
   (salt, oil, water) if absolutely needed, but flag them clearly.
3. Adapt the recipe to the requested cuisine style using the Culture Flavor Matrix principles.
4. Keep recipes AFFORDABLE and achievable in a basic Pakistani kitchen.
5. Prioritize HEALTH: minimize oil, maximize vegetables and protein, avoid excess sugar.
6. Provide ALL text fields in BOTH English and Urdu as specified in the schema.
7. Estimate ingredient prices in Pakistani Rupees (PKR) — be realistic for 2024-2025 prices.

## Curated Pakistani Ingredient List (draw from these when suggesting pantry staples):
{', '.join(INDIGENOUS_INGREDIENTS)}

{RECIPE_JSON_SCHEMA}
"""


def _get_openai_client() -> openai.OpenAI:
    """Return an OpenAI client using the API key from Streamlit secrets."""
    api_key = st.secrets["OPENAI_API_KEY"]
    return openai.OpenAI(api_key=api_key)


def build_user_prompt(ingredients: str, cuisine: str, max_ingredients: int) -> str:
    """Build the user-turn prompt with cuisine profile and constraints injected."""
    flavor_profile = get_flavor_profile_text(cuisine)

    return f"""I have the following ingredients available:
{ingredients}

Please create a novel, healthy recipe with these constraints:
- Cuisine style: {cuisine}
- Culture Flavor Matrix for this cuisine:
{flavor_profile}

- Use a MAXIMUM of {max_ingredients} main ingredients from my list above
- The recipe must be suitable for a Pakistani household kitchen
- Prioritize health, affordability, and minimal food waste
- Provide all text in both English and Urdu as required by the JSON schema

Return ONLY the JSON object as specified. No other text.
"""


def _parse_recipe_json(raw: str) -> dict:
    """
    Parse GPT response as JSON. Strips markdown fences if present.
    Raises ValueError if parsing fails.
    """
    # Strip markdown code fences if GPT wraps in ```json ... ```
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last fence lines
        cleaned = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    return json.loads(cleaned)


def _validate_recipe(recipe: dict) -> list[str]:
    """
    Validate required fields are present and non-empty.
    Returns list of missing/invalid field names (empty = valid).
    """
    required_fields = [
        "recipe_name", "recipe_name_ur", "description", "description_ur",
        "cuisine", "prep_time_min", "cook_time_min", "servings",
        "ingredients", "instructions", "instructions_ur",
        "health_tips", "health_tips_ur",
        "serving_suggestions", "serving_suggestions_ur",
        "sustainability_tip", "sustainability_tip_ur",
        "closing_remark",
    ]
    issues = []
    for field in required_fields:
        val = recipe.get(field)
        if val is None or val == "" or val == [] or val == {}:
            issues.append(field)

    # Check instructions/instructions_ur have same length
    en_steps = recipe.get("instructions", [])
    ur_steps = recipe.get("instructions_ur", [])
    if isinstance(en_steps, list) and isinstance(ur_steps, list):
        if len(en_steps) != len(ur_steps):
            issues.append("instructions_ur length mismatch")

    return issues


def generate_recipe(ingredients: str, cuisine: str, max_ingredients: int) -> dict:
    """
    Generate a recipe from text ingredients.
    Returns parsed recipe dict.
    Raises ValueError on parse failure after one retry.
    """
    client = _get_openai_client()
    user_prompt = build_user_prompt(ingredients, cuisine, max_ingredients)

    def _call_api() -> str:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.85,
            max_tokens=2000,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    # First attempt
    raw = _call_api()
    try:
        recipe = _parse_recipe_json(raw)
        issues = _validate_recipe(recipe)
        if not issues:
            return recipe
    except (json.JSONDecodeError, ValueError):
        pass

    # One automatic retry with lower temperature for reliability
    raw = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
            {"role": "assistant", "content": raw},
            {"role": "user",   "content": "Your response was not valid JSON. Please return ONLY the JSON object, no other text."},
        ],
        temperature=0.3,
        max_tokens=2000,
        response_format={"type": "json_object"},
    ).choices[0].message.content

    recipe = _parse_recipe_json(raw)
    return recipe


def identify_ingredients_from_image(image_bytes: bytes) -> str:
    """
    Use GPT-4o-mini vision to identify ingredients from an uploaded image.
    Returns a comma-separated string of detected ingredients.
    """
    client = _get_openai_client()
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are a kitchen assistant. Look at this image carefully and list ALL "
                            "the food ingredients you can see. Be specific (e.g., 'red onion', 'ripe tomato', "
                            "'green chilli'). Return ONLY a comma-separated list of ingredients, nothing else. "
                            "Example: onion, tomato, garlic, green chilli, eggs"
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"},
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


def generate_recipe_from_image(
    image_bytes: bytes, cuisine: str, max_ingredients: int
) -> tuple[str, dict]:
    """
    Full pipeline: image → identify ingredients → generate recipe.
    Returns (detected_ingredients_str, recipe_dict).
    """
    ingredients = identify_ingredients_from_image(image_bytes)
    recipe = generate_recipe(ingredients, cuisine, max_ingredients)
    return ingredients, recipe


def recipe_to_text(recipe: dict, lang: str = "en") -> str:
    """
    Convert a recipe dict to a plain-text string for download.
    lang: 'en' or 'ur'
    """
    if lang == "ur":
        name = recipe.get("recipe_name_ur", recipe.get("recipe_name", ""))
        desc = recipe.get("description_ur", recipe.get("description", ""))
        instructions = recipe.get("instructions_ur", recipe.get("instructions", []))
        health = recipe.get("health_tips_ur", recipe.get("health_tips", ""))
        serving = recipe.get("serving_suggestions_ur", recipe.get("serving_suggestions", ""))
        sustainability = recipe.get("sustainability_tip_ur", recipe.get("sustainability_tip", ""))
    else:
        name = recipe.get("recipe_name", "")
        desc = recipe.get("description", "")
        instructions = recipe.get("instructions", [])
        health = recipe.get("health_tips", "")
        serving = recipe.get("serving_suggestions", "")
        sustainability = recipe.get("sustainability_tip", "")

    lines = [
        f"{'=' * 50}",
        f"HEALTHY BAWARCHI — Recipe",
        f"{'=' * 50}",
        f"",
        f"{name}",
        f"{desc}",
        f"",
        f"Cuisine: {recipe.get('cuisine', '')}",
        f"Prep: {recipe.get('prep_time_min', '?')} min | Cook: {recipe.get('cook_time_min', '?')} min | Serves: {recipe.get('servings', '?')}",
        f"",
        f"INGREDIENTS:",
    ]
    for ing in recipe.get("ingredients", []):
        item = ing.get("item_ur" if lang == "ur" else "item", "")
        qty = ing.get("quantity", "")
        pkr = ing.get("price_pkr", "")
        lines.append(f"  • {item} — {qty}  (~PKR {pkr})")

    lines += [
        f"",
        f"INSTRUCTIONS:",
    ]
    for i, step in enumerate(instructions, 1):
        lines.append(f"  {i}. {step}")

    lines += [
        f"",
        f"HEALTH NOTES:",
        f"  {health}",
        f"",
        f"SERVING SUGGESTIONS:",
        f"  {serving}",
        f"",
        f"SUSTAINABILITY TIP:",
        f"  {sustainability}",
        f"",
        f"{'=' * 50}",
        f"Bawarchi AI says: {recipe.get('closing_remark', '')}",
        f"{'=' * 50}",
        f"",
        f"Nutritional values sourced from USDA FoodData Central where available.",
        f"Values are approximate and not a substitute for medical dietary advice.",
    ]
    return "\n".join(lines)
