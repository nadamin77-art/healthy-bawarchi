# ============================================================
# Healthy Bawarchi — Internationalization (i18n)
# Bilingual EN/UR string dictionary + RTL CSS injector
# ============================================================

import streamlit as st

# ------------------------------------
# Full bilingual string dictionary
# ------------------------------------
T = {
    "en": {
        # App identity
        "title": "Healthy Bawarchi",
        "title_ur": "صحت مند باورچی",
        "subtitle": "Your AI-powered Smart Culinary Interface",
        "tagline": "Khaao Sehat Se • Eat Healthy",
        "page_title": "Healthy Bawarchi — Smart Recipe Generator",

        # Language toggle
        "lang_toggle": "🇵🇰 اردو",

        # Sidebar
        "sidebar_settings": "About",
        "sidebar_about": (
            "Healthy Bawarchi helps you create healthy, affordable recipes "
            "from whatever ingredients you have at home — reducing food waste "
            "and promoting sustainable eating in Pakistan."
        ),
        "sidebar_disclaimer": (
            "Nutritional data sourced from USDA FoodData Central where available. "
            "Values are approximate and not a substitute for medical dietary advice."
        ),

        # Cuisine selector
        "choose_cuisine": "Choose Your Cuisine Style",

        # Ingredient count
        "max_ingredients_label": "How many ingredients to use?",
        "max_ingredients_caption": "The recipe will use at most **{n} main ingredients** — keeping it simple and affordable.",

        # Input section
        "what_ingredients": "What ingredients do you have?",
        "tab_type": "✏️ Type Ingredients",
        "tab_photo": "📷 Upload a Photo",
        "type_placeholder": "e.g. eggs, onion, tomato, green chilli, yogurt, leftover roti...",
        "type_caption": "Separate ingredients with commas. Don't worry about exact amounts — Bawarchi AI will figure it out!",
        "photo_caption": "Bawarchi AI will scan this image and identify the ingredients automatically.",
        "photo_detected": "🔍 **Ingredients detected from your photo:**",

        # Generate button
        "generate_btn": "✨ Generate My Recipe!",

        # Spinner
        "spinner": "Bawarchi AI is cooking something special for you...",

        # Errors
        "error_no_input": "Please type your ingredients or upload a photo first.",
        "error_retry": "Could not parse recipe response. Please try again.",
        "error_api_key": "Invalid OpenAI API key. Please check your configuration.",
        "error_quota": "API quota exceeded. Please check your OpenAI account billing.",
        "error_generic": "Something went wrong: {msg}",

        # Recipe output
        "recipe_header": "Your Recipe",
        "cuisine_label": "Cuisine",
        "prep_label": "Prep",
        "cook_label": "Cook",
        "servings_label": "Servings",
        "min_label": "min",
        "ingredients_header": "Ingredients",
        "nutrition_header": "Nutrition per Serving",
        "calories_label": "Calories",
        "protein_label": "Protein",
        "carbs_label": "Carbs",
        "fat_label": "Fat",
        "fiber_label": "Fiber",
        "usda_badge": "USDA sourced ✓",
        "estimated_badge": "AI estimated ~",
        "instructions_header": "Cooking Method",
        "health_header": "Health Notes",
        "sustainability_header": "Sustainability Tip",
        "serving_header": "Serving Suggestions",
        "closing_header": "Bawarchi AI says",
        "price_label": "Est. Price (PKR)",
        "total_label": "Total",

        # Download
        "download_btn": "📥 Download Recipe",
        "download_filename": "healthy_bawarchi_recipe.txt",

        # Footer
        "footer": (
            "Healthy Bawarchi &nbsp;|&nbsp; Promoting healthy, sustainable eating in Pakistan 🇵🇰<br>"
            "<em>\"Sehat mand khaana, khushaal zindagi — yahi hai Healthy Bawarchi!\"</em>"
        ),
    },

    "ur": {
        # App identity
        "title": "صحت مند باورچی",
        "title_ur": "Healthy Bawarchi",
        "subtitle": "آپ کا AI سے چلنے والا ذہین کھانا انٹرفیس",
        "tagline": "کھاؤ صحت سے • Khaao Sehat Se",
        "page_title": "صحت مند باورچی — ذہین ریسیپی جنریٹر",

        # Language toggle
        "lang_toggle": "🇬🇧 English",

        # Sidebar
        "sidebar_settings": "ہمارے بارے میں",
        "sidebar_about": (
            "صحت مند باورچی آپ کو گھر میں موجود اجزاء سے صحت مند اور سستی ریسیپیاں بنانے میں مدد کرتا ہے — "
            "کھانے کا ضیاع کم کرتا ہے اور پاکستان میں پائیدار کھانے کو فروغ دیتا ہے۔"
        ),
        "sidebar_disclaimer": (
            "غذائی معلومات جہاں ممکن ہو USDA FoodData Central سے لی گئی ہیں۔ "
            "یہ اقدار تخمینی ہیں اور طبی غذائی مشورے کا متبادل نہیں ہیں۔"
        ),

        # Cuisine selector
        "choose_cuisine": "اپنا کھانے کا انداز چنیں",

        # Ingredient count
        "max_ingredients_label": "کتنے اجزاء استعمال کریں؟",
        "max_ingredients_caption": "ریسیپی میں زیادہ سے زیادہ **{n} اہم اجزاء** استعمال ہوں گے — سادہ اور سستا۔",

        # Input section
        "what_ingredients": "آپ کے پاس کون سے اجزاء ہیں؟",
        "tab_type": "✏️ اجزاء لکھیں",
        "tab_photo": "📷 تصویر اپلوڈ کریں",
        "type_placeholder": "مثلاً انڈے، پیاز، ٹماٹر، ہری مرچ، دہی، بچی ہوئی روٹی...",
        "type_caption": "اجزاء کو کاما سے الگ کریں۔ صحیح مقدار کی فکر نہ کریں — باورچی AI سنبھال لے گا!",
        "photo_caption": "باورچی AI اس تصویر کو اسکین کر کے اجزاء خود پہچانے گا۔",
        "photo_detected": "🔍 **آپ کی تصویر سے پہچانے گئے اجزاء:**",

        # Generate button
        "generate_btn": "✨ میری ریسیپی بنائیں!",

        # Spinner
        "spinner": "باورچی AI آپ کے لیے کچھ خاص پکا رہا ہے...",

        # Errors
        "error_no_input": "براہ کرم پہلے اجزاء لکھیں یا تصویر اپلوڈ کریں۔",
        "error_retry": "ریسیپی کا جواب پارس نہیں ہو سکا۔ دوبارہ کوشش کریں۔",
        "error_api_key": "OpenAI API کی غلط ہے۔ براہ کرم اپنی ترتیب چیک کریں۔",
        "error_quota": "API کوٹہ ختم ہو گیا۔ اپنا OpenAI اکاؤنٹ چیک کریں۔",
        "error_generic": "کچھ غلط ہو گیا: {msg}",

        # Recipe output
        "recipe_header": "آپ کی ریسیپی",
        "cuisine_label": "کھانے کا انداز",
        "prep_label": "تیاری",
        "cook_label": "پکانا",
        "servings_label": "افراد",
        "min_label": "منٹ",
        "ingredients_header": "اجزاء",
        "nutrition_header": "فی سرونگ غذائیت",
        "calories_label": "کیلوریز",
        "protein_label": "پروٹین",
        "carbs_label": "کاربس",
        "fat_label": "چکنائی",
        "fiber_label": "فائبر",
        "usda_badge": "USDA تصدیق شدہ ✓",
        "estimated_badge": "AI تخمینہ ~",
        "instructions_header": "پکانے کا طریقہ",
        "health_header": "صحت کے فوائد",
        "sustainability_header": "پائیداری کا مشورہ",
        "serving_header": "پیش کرنے کا طریقہ",
        "closing_header": "باورچی AI کہتا ہے",
        "price_label": "تخمینی قیمت (روپے)",
        "total_label": "کل",

        # Download
        "download_btn": "📥 ریسیپی ڈاؤن لوڈ کریں",
        "download_filename": "healthy_bawarchi_recipe.txt",

        # Footer
        "footer": (
            "صحت مند باورچی &nbsp;|&nbsp; پاکستان میں صحت مند، پائیدار کھانے کو فروغ دینا 🇵🇰<br>"
            "<em>\"صحت مند کھانا، خوشحال زندگی — یہی ہے Healthy Bawarchi!\"</em>"
        ),
    },
}


def get_lang() -> str:
    """Return current language from session state."""
    return st.session_state.get("lang", "en")


def t(key: str, **kwargs) -> str:
    """Translate a key to the current language, with optional format args."""
    lang = get_lang()
    text = T[lang].get(key, T["en"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text


def inject_rtl_css():
    """Inject RTL CSS for Urdu mode. Called only when lang == 'ur'."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');

        .main .block-container,
        .stMarkdown, .stMarkdown p,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown li, .stMarkdown ol, .stMarkdown ul,
        .element-container p,
        .stAlert p {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Noto Nastaliq Urdu', serif !important;
        }

        .stTextArea textarea {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Noto Nastaliq Urdu', serif !important;
        }

        .stRadio label {
            direction: rtl !important;
        }

        .hero-banner h1, .hero-banner p, .hero-tagline {
            direction: rtl !important;
            font-family: 'Noto Nastaliq Urdu', serif !important;
        }

        .section-title {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Noto Nastaliq Urdu', serif !important;
        }

        .recipe-output, .recipe-output p,
        .recipe-output h1, .recipe-output h2, .recipe-output h3,
        .recipe-output li {
            direction: rtl !important;
            text-align: right !important;
            font-family: 'Noto Nastaliq Urdu', serif !important;
        }
    </style>
    """, unsafe_allow_html=True)


def inject_ltr_css():
    """Inject LTR CSS for English mode (reset any RTL)."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        .main .block-container,
        .stMarkdown, .stMarkdown p,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown li {
            direction: ltr !important;
            text-align: left !important;
            font-family: 'Poppins', sans-serif !important;
        }

        .stTextArea textarea {
            direction: ltr !important;
            text-align: left !important;
            font-family: 'Poppins', sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)
