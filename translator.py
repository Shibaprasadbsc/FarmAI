"""
FarmAI Backend — translator.py
================================
Handles translation of disease names and treatment text
into Hindi and Odia using the deep-translator library.

Install:  pip install deep-translator
Docs:     https://github.com/nidhaloff/deep-translator
"""

# ── Language code map ──────────────────────────────────────────────────────────
# These are the language codes Google Translate understands
LANG_CODES = {
    "en": "english",
    "hi": "hindi",
    "od": "odia",
    "or": "odia",   # alternate code
}

# ── Simple offline fallback dictionary ────────────────────────────────────────
# If Google Translate is not available (no internet / quota exceeded),
# we use these pre-translated common phrases.
FALLBACK = {
    "hi": {
        "Tomato Early Blight":    "टमाटर का अगेती झुलसा रोग",
        "Tomato Late Blight":     "टमाटर का पछेती झुलसा रोग",
        "Tomato Leaf Mold":       "टमाटर का पत्ती फफूंद",
        "Tomato Yellow Leaf Curl":"टमाटर पीली पत्ती मरोड़ विषाणु",
        "Potato Early Blight":    "आलू का अगेती झुलसा रोग",
        "Potato Late Blight":     "आलू का पछेती झुलसा रोग",
        "Corn Common Rust":       "मक्का का सामान्य रतुआ",
        "Apple Scab":             "सेब का पपड़ी रोग",
        "Healthy":                "स्वस्थ फसल",
        "No treatment needed":    "उपचार की आवश्यकता नहीं",
        "Spray every 7 days":     "हर 7 दिन में स्प्रे करें",
    },
    "od": {
        "Tomato Early Blight":    "ଟମାଟୋ ଆଗୁ ନଷ୍ଟ ରୋଗ",
        "Tomato Late Blight":     "ଟମାଟୋ ପର ନଷ୍ଟ ରୋଗ",
        "Potato Early Blight":    "ଆଳୁ ଆଗୁ ନଷ୍ଟ ରୋଗ",
        "Potato Late Blight":     "ଆଳୁ ପର ନଷ୍ଟ ରୋଗ",
        "Corn Common Rust":       "ମକା ସାଧାରଣ ମରଚ",
        "Apple Scab":             "ଆପଲ ଖସ ରୋଗ",
        "Healthy":                "ସୁସ୍ଥ ଫସଲ",
        "No treatment needed":    "ଚିକିତ୍ସା ଆବଶ୍ୟକ ନାହିଁ",
    }
}


def translate_text(text: str, target_lang: str) -> str:
    """
    Translate `text` into `target_lang`.

    Steps:
    1. Try deep-translator (Google Translate wrapper) — needs internet.
    2. If that fails, check our offline fallback dictionary.
    3. If not in fallback, return the original English text with a note.

    Args:
        text        : English string to translate
        target_lang : Language code ("hi" / "od" / "en")

    Returns:
        Translated string (or original if translation fails)
    """
    # English — no translation needed
    if target_lang == "en":
        return text

    lang_name = LANG_CODES.get(target_lang, "hindi")

    # ── Try live translation ───────────────────────────────────────────────────
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source="english", target=lang_name)
        result = translator.translate(text)
        return result if result else text

    except ImportError:
        # deep-translator not installed — use fallback
        pass
    except Exception as e:
        # Network error, quota exceeded, etc. — use fallback
        print(f"[Translator] Live translation failed: {e}. Using fallback.")

    # ── Fallback dictionary ────────────────────────────────────────────────────
    lang_fallback = FALLBACK.get(target_lang, {})
    for key, value in lang_fallback.items():
        if key.lower() in text.lower():
            return value

    # ── Last resort: return original with language tag ─────────────────────────
    return f"[{target_lang.upper()}] {text}"


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("Tomato Early Blight", "hi"),
        ("Spray every 7 days", "hi"),
        ("Apple Scab", "od"),
        ("Hello world", "en"),
    ]
    print("Translation test:\n")
    for text, lang in tests:
        result = translate_text(text, lang)
        print(f"  [{lang}] {text!r:35} → {result!r}")
