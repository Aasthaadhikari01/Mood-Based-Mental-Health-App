# app.py
import streamlit as st
st.set_page_config(layout="wide", page_title="Mood Adaptive UI")
from transformers import pipeline



# Load sentiment/emotion classifier
@st.cache_resource
def load_classifier():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

classifier = load_classifier()

# Mood to theme settings
mood_themes = {
    "joy": {"bg": "#FFF9C4", "font_color": "#333", "message": "You're glowing! Keep shining 🌞"},
    "sadness": {"bg": "#BBDEFB", "font_color": "#000", "message": "It's okay to feel down. Try journaling or take a deep breath 💙"},
    "anger": {"bg": "#FFCDD2", "font_color": "#000", "message": "Let’s cool off with a relaxing activity 🧘‍♂️"},
    "fear": {"bg": "#D1C4E9", "font_color": "#000", "message": "You're safe here. Maybe some calming music? 🎵"},
    "surprise": {"bg": "#F0F4C3", "font_color": "#000", "message": "Whoa! Let’s turn this surprise into excitement! 🎉"},
    "neutral": {"bg": "#ECEFF1", "font_color": "#000", "message": "Steady and balanced – a great place to be 🤍"},
}


st.title("🧠 Mood-Based Mental Health App")

st.markdown("Enter your current mood in words or describe your feelings:")

user_input = st.text_area("How are you feeling today?", placeholder="Write anything...")

if user_input:
        # Get all scores
    raw_scores = classifier(user_input, return_all_scores=True)[0]
    scores_dict = {item['label'].lower(): item['score'] for item in raw_scores}

    # Custom override logic
        # Check for override based on keywords
    lowered_input = user_input.lower()
    if any(phrase in lowered_input for phrase in ["not feeling good", "not okay", "feeling bad", "can't", "unable", "hopeless", "sad", "tired", "late", "down"]):
        mood = "sadness"
    elif scores_dict.get("sadness", 0) > 0.5:
        mood = "sadness"
    elif scores_dict.get("anger", 0) > 0.5:
        mood = "anger"
    elif scores_dict.get("fear", 0) > 0.5:
        mood = "fear"
    else:
        mood = max(scores_dict, key=scores_dict.get)

    
    st.write("🔍 Raw scores:", scores_dict)  # You can remove this after testing


    # Get theme details
    theme = mood_themes.get(mood, mood_themes["neutral"])

    # Apply background color and font dynamically
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {theme['bg']};
            color: {theme['font_color']};
        }}
        .content-box {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"<div class='content-box'><h3>🧘 Mood Detected: {mood.title()}</h3><p>{theme['message']}</p></div>", unsafe_allow_html=True)

    # Activity Suggestion
    st.markdown("### 🌟 Suggested Activity:")
    if mood in ["sadness", "anger", "fear"]:
        st.write("- Try a breathing exercise [Box Breathing (4-4-4-4)](https://youtu.be/FJJazKtH_9I)")
        st.write("- Journal your thoughts or listen to [calming music](https://www.youtube.com/watch?v=2OEL4P1Rz04)")
    elif mood == "joy":
        st.write("- Share your happiness with someone 😊")
    elif mood == "surprise":
        st.write("- Reflect: What amazed you today?")
    else:
        st.write("- Continue with your daily focus tasks 📋")

else:
    st.info("Write something above to detect mood and personalize your experience.")

