# ============================================================
# Healthy Bawarchi — Main Streamlit App
# Bilingual (EN/UR) AI-powered recipe generator
# ============================================================

import streamlit as st
from PIL import Image

from recipe_engine import generate_recipe, generate_recipe_from_image, recipe_to_text
from usda_nutrition import calculate_recipe_nutrition, format_nutrition_source_note
from i18n import t, get_lang, inject_rtl_css, inject_ltr_css

# ─────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit call
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Healthy Bawarchi — Smart Recipe Generator",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"
if "recipe" not in st.session_state:
    st.session_state["recipe"] = None
if "nutrition" not in st.session_state:
    st.session_state["nutrition"] = None
if "detected_ingredients" not in st.session_state:
    st.session_state["detected_ingredients"] = None

lang = get_lang()

# ─────────────────────────────────────────────
# LANGUAGE-AWARE CSS
# ─────────────────────────────────────────────
if lang == "ur":
    inject_rtl_css()
else:
    inject_ltr_css()

# ─────────────────────────────────────────────
# GLOBAL CSS — Green theme, Healthy Bawarchi brand
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #F1F8E9 0%, #E8F5E9 100%);
    }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(27, 94, 32, 0.3);
    }
    .hero-banner h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 1px;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.92);
        font-size: 1.05rem;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    .hero-tagline {
        color: #CCFF90;
        font-size: 0.95rem;
        font-style: italic;
        margin-top: 0.3rem;
    }

    /* Section cards */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 4px solid #2E7D32;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1B5E20;
        margin-bottom: 0.8rem;
    }

    /* Generate button */
    .stButton > button {
        background: linear-gradient(135deg, #1B5E20, #2E7D32) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.4) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(27, 94, 32, 0.5) !important;
    }

    /* Recipe output card */
    .recipe-output {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-top: 5px solid #2E7D32;
        margin-top: 1.5rem;
    }

    /* Cuisine pill badge */
    .cuisine-pill {
        display: inline-block;
        background: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #2E7D32;
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.8rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #E8F5E9;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #2E7D32 !important;
        color: white !important;
    }

    /* Detected ingredients box */
    .detected-box {
        background: #E8F5E9;
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
        color: #1B5E20;
        margin: 0.5rem 0 1rem 0;
    }

    /* Nutrition card */
    .nutrition-card {
        background: #F9FBE7;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #C5E1A5;
    }

    /* USDA badge */
    .usda-badge {
        font-size: 0.75rem;
        color: #388E3C;
        font-weight: 600;
        margin-top: 0.5rem;
    }

        /* Language toggle button — override to be compact */
    div[data-testid="column"]:last-child .stButton > button {
        background: #E8F5E9 !important;
        color: #1B5E20 !important;
        border: 1px solid #2E7D32 !important;
        border-radius: 20px !important;
        padding: 0.3rem 0.8rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        width: auto !important;
        min-width: 90px !important;
        white-space: nowrap !important;
        box-shadow: none !important;
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }

    /* Hide Streamlit default branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LANGUAGE TOGGLE — top right
# ─────────────────────────────────────────────
col_title, col_toggle = st.columns([6, 1])
with col_toggle:
    if st.button(t("lang_toggle"), key="lang_btn"):
        st.session_state["lang"] = "ur" if lang == "en" else "en"
        # Clear recipe on language switch so output re-renders in new language
        st.session_state["recipe"] = None
        st.session_state["nutrition"] = None
        st.rerun()

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <h1>🥗 {t("title")}</h1>
    <p>{t("subtitle")}</p>
    <div class="hero-tagline">{t("tagline")}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — About & disclaimer
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🌿 {t('sidebar_settings')}")
    st.markdown("---")
    st.markdown(t("sidebar_about"))
    st.markdown("---")
    st.caption(t("sidebar_disclaimer"))

# ─────────────────────────────────────────────
# CUISINE SELECTOR
# ─────────────────────────────────────────────
st.markdown(
    f'<div class="section-card"><div class="section-title">🌍 {t("choose_cuisine")}</div>',
    unsafe_allow_html=True,
)
cuisine_options = {
    "🇵🇰 Pakistani": "Pakistani",
    "🇨🇳 Chinese":   "Chinese",
    "🇮🇹 Italian":   "Italian",
    "🇲🇽 Mexican":   "Mexican",
}
cuisine_display = st.radio(
    "Cuisine",
    options=list(cuisine_options.keys()),
    horizontal=True,
    label_visibility="collapsed",
)
cuisine = cuisine_options[cuisine_display]
st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAX INGREDIENTS SLIDER
# ─────────────────────────────────────────────
st.markdown(
    f'<div class="section-card"><div class="section-title">🔢 {t("max_ingredients_label")}</div>',
    unsafe_allow_html=True,
)
max_ingredients = st.slider(
    "Max ingredients",
    min_value=3,
    max_value=10,
    value=5,
    help="Fewer ingredients = more budget-friendly and less food waste",
    label_visibility="collapsed",
)
st.caption(t("max_ingredients_caption", n=max_ingredients))
st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INGREDIENT INPUT — Text or Image tabs
# ─────────────────────────────────────────────
st.markdown(
    f'<div class="section-card"><div class="section-title">🥦 {t("what_ingredients")}</div>',
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs([t("tab_type"), t("tab_photo")])

ingredients_text = ""
uploaded_image_bytes = None

with tab1:
    ingredients_text = st.text_area(
        "Ingredients",
        placeholder=t("type_placeholder"),
        height=120,
        label_visibility="collapsed",
    )
    st.caption(t("type_caption"))

with tab2:
    uploaded_file = st.file_uploader(
        "Upload a photo of your ingredients",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="", use_container_width=True)
        uploaded_image_bytes = uploaded_file.getvalue()
        st.caption(t("photo_caption"))

st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GENERATE BUTTON
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
generate_btn = st.button(t("generate_btn"), use_container_width=True)

# ─────────────────────────────────────────────
# GENERATION LOGIC
# ─────────────────────────────────────────────
if generate_btn:
    has_text  = bool(ingredients_text.strip())
    has_image = uploaded_image_bytes is not None

    if not has_text and not has_image:
        st.warning(t("error_no_input"))
        st.stop()

    with st.spinner(t("spinner")):
        try:
            if has_image:
                detected, recipe = generate_recipe_from_image(
                    uploaded_image_bytes, cuisine, max_ingredients
                )
                st.session_state["detected_ingredients"] = detected
            else:
                recipe = generate_recipe(ingredients_text, cuisine, max_ingredients)
                st.session_state["detected_ingredients"] = None

            # Fetch USDA nutrition
            usda_key = st.secrets.get("USDA_API_KEY", "")
            nutrition = calculate_recipe_nutrition(
                recipe.get("ingredients", []),
                recipe.get("servings", 2),
                usda_key,
            )

            st.session_state["recipe"]    = recipe
            st.session_state["nutrition"] = nutrition

        except Exception as e:
            err = str(e)
            if "api_key" in err.lower() or "authentication" in err.lower() or "401" in err:
                st.error(t("error_api_key"))
            elif "quota" in err.lower() or "429" in err:
                st.error(t("error_quota"))
            else:
                st.error(t("error_generic", msg=err))
            st.stop()

# ─────────────────────────────────────────────
# RECIPE OUTPUT RENDERING
# ─────────────────────────────────────────────
recipe    = st.session_state.get("recipe")
nutrition
