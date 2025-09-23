import streamlit as st
import random
import csv
import os
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="Body Count Detector 😂",
    page_icon="💕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'dark_theme' not in st.session_state:
    st.session_state.dark_theme = True
if 'calculation_progress' not in st.session_state:
    st.session_state.calculation_progress = 0
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'result_data' not in st.session_state:
    st.session_state.result_data = {}
if 'form_completion' not in st.session_state:
    st.session_state.form_completion = 0

def inject_advanced_css(dark_theme=True):
    """Inject advanced interactive CSS with animations and effects"""
    
    # Color scheme based on theme
    if dark_theme:
        bg_primary = "rgba(15, 15, 25, 0.95)"
        bg_secondary = "rgba(25, 25, 40, 0.8)"
        bg_tertiary = "rgba(35, 35, 55, 0.6)"
        text_primary = "#ffffff"
        text_secondary = "#e0e0e0"
        accent_color = "#ff6b9d"
        accent_secondary = "#667eea"
        gradient_bg = "linear-gradient(135deg, #0f0f19 0%, #1a1a2e 50%, #16213e 100%)"
        particle_color = "rgba(255, 107, 157, 0.6)"
    else:
        bg_primary = "rgba(255, 255, 255, 0.95)"
        bg_secondary = "rgba(240, 240, 250, 0.8)"
        bg_tertiary = "rgba(250, 250, 255, 0.6)"
        text_primary = "#2c2c2c"
        text_secondary = "#4a4a4a"
        accent_color = "#ff6b9d"
        accent_secondary = "#667eea"
        gradient_bg = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 50%, #e0c3fc 100%)"
        particle_color = "rgba(255, 107, 157, 0.4)"
    
    css = f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Orbitron:wght@400;700;900&display=swap');
    
    /* Global Styles */
    .stApp {{
        background: {gradient_bg};
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow-x: hidden;
        min-height: 100vh;
    }}
    
    /* Advanced floating background with multiple layers */
    .stApp::before {{
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 20%, {particle_color} 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(102, 126, 234, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(118, 75, 162, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 60% 10%, rgba(255, 107, 157, 0.1) 0%, transparent 40%);
        animation: advancedFloat 25s ease-in-out infinite;
        z-index: -3;
    }}
    
    /* Interactive particle system */
    .stApp::after {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 10% 20%, {accent_color}20 1px, transparent 1px),
            radial-gradient(circle at 80% 80%, {accent_secondary}15 1px, transparent 1px),
            radial-gradient(circle at 40% 40%, {particle_color} 0.5px, transparent 0.5px),
            radial-gradient(circle at 90% 10%, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 80px 80px, 120px 120px, 60px 60px, 100px 100px;
        animation: particleFloat 20s linear infinite;
        pointer-events: none;
        z-index: -2;
    }}
    
    @keyframes advancedFloat {{
        0%, 100% {{ transform: translate(0px, 0px) rotate(0deg) scale(1); }}
        25% {{ transform: translate(30px, -30px) rotate(90deg) scale(1.1); }}
        50% {{ transform: translate(-20px, 20px) rotate(180deg) scale(0.9); }}
        75% {{ transform: translate(40px, 10px) rotate(270deg) scale(1.05); }}
    }}
    
    @keyframes particleFloat {{
        0% {{ transform: translate(0, 0) rotate(0deg); opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
        100% {{ transform: translate(-100px, -100px) rotate(360deg); opacity: 0.3; }}
    }}
    
    /* Advanced Glassmorphism Cards */
    .glass-card {{
        background: {bg_secondary};
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 25px;
        padding: 35px;
        margin: 25px 0;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.1),
            0 5px 15px rgba(0, 0, 0, 0.05),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }}
    
    /* Interactive hover effects */
    .glass-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .glass-card:hover::before {{
        left: 100%;
    }}
    
    .glass-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.2),
            0 10px 25px rgba(0, 0, 0, 0.1),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 107, 157, 0.3);
    }}
    
    /* Progress indicator */
    .progress-container {{
        background: {bg_tertiary};
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .progress-bar {{
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, {accent_color}, {accent_secondary});
        border-radius: 10px;
        transition: width 0.5s ease;
        position: relative;
    }}
    
    .progress-fill::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: progressShine 2s ease-in-out infinite;
    }}
    
    @keyframes progressShine {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    
    /* Enhanced Result Card with 3D effects */
    .result-card {{
        background: {bg_secondary};
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 2px solid {accent_color};
        border-radius: 30px;
        padding: 50px;
        margin: 40px 0;
        box-shadow: 
            0 30px 80px rgba(255, 107, 157, 0.4),
            0 15px 40px rgba(255, 107, 157, 0.2),
            0 0 0 1px rgba(255, 107, 157, 0.3),
            inset 0 2px 0 rgba(255, 255, 255, 0.1),
            inset 0 -2px 0 rgba(0, 0, 0, 0.1);
        text-align: center;
        position: relative;
        animation: cinematicReveal 2s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
        transform-style: preserve-3d;
    }}
    
    @keyframes cinematicReveal {{
        0% {{
            transform: scale(0.5) rotateY(-30deg) rotateX(15deg);
            opacity: 0;
            filter: blur(20px);
        }}
        30% {{
            transform: scale(0.8) rotateY(-10deg) rotateX(5deg);
            opacity: 0.3;
            filter: blur(10px);
        }}
        60% {{
            transform: scale(1.1) rotateY(5deg) rotateX(-2deg);
            opacity: 0.8;
            filter: blur(2px);
        }}
        100% {{
            transform: scale(1) rotateY(0deg) rotateX(0deg);
            opacity: 1;
            filter: blur(0);
        }}
    }}
    
    /* Advanced particle system for result card */
    .result-card::before {{
        content: '';
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background-image: 
            radial-gradient(circle at 25% 25%, {accent_color}60 3px, transparent 3px),
            radial-gradient(circle at 75% 75%, rgba(255,255,255,0.2) 2px, transparent 2px),
            radial-gradient(circle at 50% 50%, {accent_color}40 1px, transparent 1px),
            radial-gradient(circle at 10% 90%, {accent_secondary}30 2px, transparent 2px);
        background-size: 60px 60px, 40px 40px, 80px 80px, 50px 50px;
        animation: advancedParticles 20s linear infinite;
        opacity: 0.4;
        z-index: 1;
    }}
    
    @keyframes advancedParticles {{
        0% {{ transform: translate(0, 0) rotate(0deg) scale(1); }}
        25% {{ transform: translate(-50px, -50px) rotate(90deg) scale(1.1); }}
        50% {{ transform: translate(-100px, -100px) rotate(180deg) scale(0.9); }}
        75% {{ transform: translate(-150px, -150px) rotate(270deg) scale(1.05); }}
        100% {{ transform: translate(-200px, -200px) rotate(360deg) scale(1); }}
    }}
    
    /* Enhanced result text with 3D effect */
    .result-text {{
        font-size: 3rem;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
        background: linear-gradient(45deg, {accent_color}, #764ba2, {accent_secondary}, {accent_color});
        background-size: 300% 300%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: 
            textGlow 3s ease-in-out infinite alternate,
            textShine 4s ease-in-out infinite,
            textPulse 2s ease-in-out infinite;
        text-shadow: 
            0 0 30px rgba(255, 107, 157, 0.8),
            0 0 60px rgba(255, 107, 157, 0.4),
            0 0 90px rgba(255, 107, 157, 0.2);
        position: relative;
        z-index: 2;
        transform-style: preserve-3d;
    }}
    
    @keyframes textGlow {{
        from {{
            filter: drop-shadow(0 0 20px {accent_color}80) drop-shadow(0 0 40px {accent_color}40);
            transform: scale(1) rotateX(0deg);
        }}
        to {{
            filter: drop-shadow(0 0 40px {accent_color}ff) drop-shadow(0 0 80px {accent_color}80);
            transform: scale(1.05) rotateX(2deg);
        }}
    }}
    
    @keyframes textShine {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes textPulse {{
        0%, 100% {{ transform: scale(1) translateZ(0); }}
        50% {{ transform: scale(1.02) translateZ(10px); }}
    }}
    
    /* Interactive main title */
    .main-title {{
        font-size: 4rem;
        font-weight: 900;
        font-family: 'Orbitron', monospace;
        text-align: center;
        background: linear-gradient(45deg, {accent_color}, #667eea, #764ba2, {accent_color});
        background-size: 300% 300%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleShine 5s ease-in-out infinite, titleFloat 6s ease-in-out infinite;
        margin-bottom: 15px;
        text-shadow: 0 0 50px rgba(255, 107, 157, 0.5);
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .main-title:hover {{
        transform: scale(1.05) rotateY(5deg);
        filter: drop-shadow(0 0 30px {accent_color}80);
    }}
    
    @keyframes titleShine {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes titleFloat {{
        0%, 100% {{ transform: translateY(0px) rotateX(0deg); }}
        50% {{ transform: translateY(-10px) rotateX(2deg); }}
    }}
    
    /* Interactive subtitle */
    .subtitle {{
        font-size: 1.4rem;
        color: {text_secondary};
        text-align: center;
        margin-bottom: 50px;
        font-weight: 400;
        animation: subtitleGlow 4s ease-in-out infinite alternate;
        transition: all 0.3s ease;
    }}
    
    .subtitle:hover {{
        color: {accent_color};
        transform: scale(1.02);
    }}
    
    @keyframes subtitleGlow {{
        from {{ opacity: 0.8; }}
        to {{ opacity: 1; text-shadow: 0 0 20px rgba(255, 107, 157, 0.3); }}
    }}
    
    /* Enhanced theme toggle */
    .theme-toggle {{
        position: fixed;
        top: 25px;
        right: 25px;
        z-index: 1000;
        background: {bg_secondary};
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50px;
        padding: 12px 20px;
        color: {text_primary};
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }}
    
    .theme-toggle:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        border-color: {accent_color};
    }}
    
    /* Enhanced form inputs */
    .stSelectbox > div > div {{
        background: {bg_tertiary} !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stSelectbox > div > div:hover {{
        border-color: {accent_color} !important;
        box-shadow: 0 5px 15px rgba(255, 107, 157, 0.2) !important;
    }}
    
    .stTextInput > div > div > input {{
        background: {bg_tertiary} !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        color: {text_primary} !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        padding: 12px 16px !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {accent_color} !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2) !important;
    }}
    
    .stSlider > div > div > div > div {{
        background: linear-gradient(90deg, {accent_color}, {accent_secondary}) !important;
    }}
    
    .stNumberInput > div > div > input {{
        background: {bg_tertiary} !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        color: {text_primary} !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    /* Enhanced button with 3D effect */
    .stButton > button {{
        background: linear-gradient(45deg, {accent_color}, #764ba2, {accent_secondary}) !important;
        background-size: 200% 200% !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 18px 40px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 15px 30px rgba(255, 107, 157, 0.4),
            0 5px 15px rgba(255, 107, 157, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        position: relative !important;
        overflow: hidden !important;
        transform-style: preserve-3d !important;
    }}
    
    .stButton > button::before {{
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.5s !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-5px) scale(1.05) rotateX(5deg) !important;
        box-shadow: 
            0 25px 50px rgba(255, 107, 157, 0.6),
            0 10px 25px rgba(255, 107, 157, 0.4) !important;
        background-position: 100% 0 !important;
    }}
    
    .stButton > button:hover::before {{
        left: 100% !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(-2px) scale(1.02) !important;
    }}
    
    /* Enhanced roast message */
    .roast-message {{
        font-size: 1.4rem;
        color: {text_primary};
        margin: 25px 0;
        padding: 25px;
        background: linear-gradient(135deg, rgba(255, 107, 157, 0.15), rgba(102, 126, 234, 0.15));
        border-radius: 20px;
        border-left: 5px solid {accent_color};
        font-weight: 600;
        position: relative;
        z-index: 2;
        backdrop-filter: blur(10px);
        animation: roastReveal 1s ease-out;
        box-shadow: 0 10px 25px rgba(255, 107, 157, 0.2);
    }}
    
    @keyframes roastReveal {{
        0% {{
            transform: translateX(-50px);
            opacity: 0;
        }}
        100% {{
            transform: translateX(0);
            opacity: 1;
        }}
    }}
    
    /* Loading animation */
    .loading-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 40px;
    }}
    
    .loading-spinner {{
        width: 60px;
        height: 60px;
        border: 4px solid rgba(255, 107, 157, 0.2);
        border-top: 4px solid {accent_color};
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Sound effect simulation */
    .sound-effect {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 4rem;
        animation: soundPulse 0.5s ease-out;
        pointer-events: none;
        z-index: 9999;
    }}
    
    @keyframes soundPulse {{
        0% {{ transform: translate(-50%, -50%) scale(0); opacity: 1; }}
        100% {{ transform: translate(-50%, -50%) scale(2); opacity: 0; }}
    }}
    
    /* Interactive form sections */
    .form-section {{
        margin: 30px 0;
        padding: 25px;
        background: {bg_tertiary};
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    }}
    
    .form-section:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(255, 107, 157, 0.1);
        border-color: rgba(255, 107, 157, 0.3);
    }}
    
    .section-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {accent_color};
        margin-bottom: 20px;
        text-align: center;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main-title {{ font-size: 2.5rem; }}
        .result-text {{ font-size: 2rem; }}
        .glass-card {{ padding: 20px; margin: 15px 0; }}
        .result-card {{ padding: 30px; }}
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def calculate_form_completion(name, age, location, selected_locality, relationship_status, 
                            dated_count, clubbing_freq, drink_choice, gender, job, favorite_food):
    """Calculate form completion percentage"""
    fields = [name, location or selected_locality, relationship_status, 
              clubbing_freq, drink_choice, gender, job, favorite_food]
    filled_fields = sum(1 for field in fields if field and field.strip())
    return min(100, (filled_fields / len(fields)) * 100)

def calculate_body_count(name, age, location, selected_locality, relationship_status, 
                        dated_count, clubbing_freq, drink_choice):
    """Calculate body count using the specified humorous algorithm"""
    
    # Seed randomness for determinism
    seed_value = sum(ord(c) for c in name.lower()) + age + len(location.strip())
    random.seed(seed_value)
    
    # Start with random base (0-5)
    score = random.randint(0, 5)
    
    # Name-based rules
    if len(name) % 2 == 0:
        score += 5
    
    if name.lower().startswith(('a', 's', 'p')):
        score += 10
    
    if any(char in name.lower() for char in ['x', 'z']):
        score += 7
    
    # Unicode codepoint micro-randomness
    score += (sum(ord(c) for c in name)) % 5
    
    # Location-based rules
    locality_boosts = {
        'Park Street': 20,
        'Ballygunge': 15,
        'Salt Lake': 10,
        'New Town': 10,
        'Rajarhat': 10,
        'Howrah': 5,
        'Esplanade': 8,
        'Garia': 3,
        'Behala': 3,
        'Dum Dum': 3,
        'Jadavpur': 3,
        'Tollygunge': 3,
        'Shyambazar': 3
    }
    
    if selected_locality and selected_locality != "None":
        score += locality_boosts.get(selected_locality, 0)
    else:
        score += len(location.strip()) % 10
        if any(city in location.lower() for city in ['kolkata', 'calcutta']):
            score += 8
    
    # Age rules
    if age < 20:
        score += 2
    elif 20 <= age <= 30:
        score += 10
    elif 31 <= age <= 40:
        score += 5
    else:
        score += 3
    
    # Relationship status rules
    relationship_boosts = {
        'Single': 5,
        'In a Relationship': 10,
        'Complicated': 15,
        'Married': 2
    }
    score += relationship_boosts.get(relationship_status, 0)
    
    # Clubbing frequency rules
    clubbing_boosts = {
        'Sometimes': 5,
        'Every weekend': 15,
        'I live in the club!': 25
    }
    score += clubbing_boosts.get(clubbing_freq, 0)
    
    # Drink choice rules
    drink_boosts = {
        'Tequila': 10,
        'Vodka': 7,
        'Whiskey': 5
    }
    score += drink_boosts.get(drink_choice, 0)
    
    # Dating count rules
    if dated_count > 5:
        score += min(20, dated_count * 2)
    
    # Cap between 0 and 100
    return max(0, min(100, score))

def get_roast_message(score):
    """Generate roast message based on score"""
    if score <= 10:
        return "Innocent soul 😇 — purity preserved."
    elif score <= 30:
        return "Lowkey romantic 😏 — careful with the heart."
    elif score <= 60:
        return "Certified Lover❤️🔥 — you know how to mingle."
    else:
        return "Kolkata's Casanova 💃🕺 — legend status unlocked."

def get_locality_roast(locality):
    """Get locality-specific roast message"""
    locality_roasts = {
        'Park Street': "Certified Party Animal 🎉",
        'Ballygunge': "High-class heartbreaker 💃",
        'Salt Lake': "Techie by day, lover by night 🤓🔥",
        'New Town': "Modern romance vibes ✨",
        'Rajarhat': "IT corridor charmer 💻❤️",
        'Howrah': "Desi Swag overload 💪",
        'Behala': "Lowkey but dangerous 😏",
        'Esplanade': "Classic Kolkata charm 🎭",
        'Garia': "Suburban secret weapon 🚇",
        'Dum Dum': "Airport area adventurer ✈️",
        'Jadavpur': "Intellectual seducer 📚🔥",
        'Tollygunge': "Bollywood dreams come true 🎬",
        'Shyambazar': "Traditional with a twist 🏛️💕"
    }
    return locality_roasts.get(locality, "")

def save_result_to_csv(name, location, selected_locality, score):
    """Save result to CSV file"""
    filename = "body_count_results.csv"
    file_exists = os.path.isfile(filename)
    
    display_location = selected_locality if selected_locality and selected_locality != "None" else location
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Location', 'Score', 'Timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Name': name,
            'Location': display_location,
            'Score': score,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return filename

def show_loading_animation():
    """Show loading animation with progress"""
    loading_container = st.empty()
    progress_bar = st.progress(0)
    
    for i in range(101):
        progress_bar.progress(i)
        if i % 20 == 0:
            loading_container.markdown(f"""
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
            <div style="text-align: center; margin-top: 10px;">
                🔮 Analyzing your romantic energy... {i}%
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.02)
    
    loading_container.empty()
    progress_bar.empty()

def main():
    """Main Streamlit app with enhanced interactivity"""
    
    # Theme toggle in sidebar
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        theme_toggle = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_theme)
        if theme_toggle != st.session_state.dark_theme:
            st.session_state.dark_theme = theme_toggle
            st.experimental_rerun()
        
        st.markdown("### 📊 Stats")
        if st.session_state.show_result and st.session_state.result_data:
            st.metric("Your Score", st.session_state.result_data.get('score', 0))
            st.metric("Form Completion", f"{st.session_state.form_completion:.0f}%")
    
    # Inject advanced CSS
    inject_advanced_css(st.session_state.dark_theme)
    
    # Interactive main title with click effect
    st.markdown('''
    <div class="main-title" onclick="this.style.transform='scale(1.1) rotateY(10deg)'; setTimeout(() => this.style.transform='scale(1) rotateY(0deg)', 200)">
        💕 Body Count Detector 💕
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="subtitle">Discover your romantic mysteries with AI-powered humor! 😂✨</div>', 
                unsafe_allow_html=True)
    
    # Input form in enhanced glassmorphism card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Personal Information Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("✨ Your Name", placeholder="Enter your magical name...")
        age = st.slider("🎂 Age", min_value=16, max_value=70, value=25)
        gender = st.selectbox("⚥ Gender", ["Male", "Female", "Other", "Prefer not to say"])
        
    with col2:
        job = st.text_input("💼 Job/Occupation", placeholder="What's your superpower?")
        relationship_status = st.selectbox("💕 Relationship Status", 
                                         ["Single", "In a Relationship", "Married", "Complicated"])
        dated_count = st.number_input("💏 How many people have you dated?", min_value=0, value=2)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Location Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📍 Location Details</div>', unsafe_allow_html=True)
    
    location_col1, location_col2 = st.columns(2)
    
    with location_col1:
        location = st.text_input("🗺️ Your Location", placeholder="Where do you spread your charm?")
    
    with location_col2:
        kolkata_localities = ["None", "Salt Lake", "Park Street", "New Town", "Garia", "Behala", 
                            "Dum Dum", "Ballygunge", "Howrah", "Shyambazar", "Esplanade", 
                            "Rajarhat", "Tollygunge", "Jadavpur"]
        selected_locality = st.selectbox("🏙️ Kolkata Locality (if applicable)", kolkata_localities)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Lifestyle Section
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎉 Lifestyle & Preferences</div>', unsafe_allow_html=True)
    
    lifestyle_col1, lifestyle_col2 = st.columns(2)
    
    with lifestyle_col1:
        clubbing_freq = st.radio("🕺 How often do you go clubbing?", 
                               ["Never", "Sometimes", "Every weekend", "I live in the club!"])
        favorite_food = st.text_input("🍕 Favorite Food", placeholder="Pizza, Biriyani, etc.")
        
    with lifestyle_col2:
        favorite_drink = st.selectbox("🍺 Favorite Drink", 
                                    ["Coke", "Beer", "Whiskey", "Vodka", "Tequila", "Other"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate and show form completion
    completion = calculate_form_completion(name, age, location, selected_locality, 
                                         relationship_status, dated_count, clubbing_freq, 
                                         favorite_drink, gender, job, favorite_food)
    st.session_state.form_completion = completion
    
    # Progress indicator
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; margin-bottom: 10px;">Form Completion: {completion:.0f}%</div>', 
                unsafe_allow_html=True)
    st.markdown(f'''
    <div class="progress-bar">
        <div class="progress-fill" style="width: {completion}%"></div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced reveal button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 REVEAL MY BODY COUNT! 🔮", use_container_width=True):
        
        # Validation with enhanced messages
        if not name.strip():
            st.markdown("""
            <div class="roast-message" style="border-left-color: #ff6b6b;">
                🤔 Hold up! We need your name to work our magic! ✨
            </div>
            """, unsafe_allow_html=True)
            return
        
        if not location.strip() and (not selected_locality or selected_locality == "None"):
            st.markdown("""
            <div class="roast-message" style="border-left-color: #ff6b6b;">
                📍 Where are you from? We need to know your hunting grounds! 😏
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Show loading animation
        show_loading_animation()
        
        # Sound effect simulation
        st.markdown('<div class="sound-effect">🎉</div>', unsafe_allow_html=True)
        
        # Calculate score
        score = calculate_body_count(name, age, location, selected_locality, 
                                   relationship_status, dated_count, clubbing_freq, favorite_drink)
        
        # Store result data
        st.session_state.result_data = {
            'name': name,
            'location': selected_locality if selected_locality and selected_locality != "None" else location,
            'score': score
        }
        st.session_state.show_result = True
        
        # Display location for result
        display_location = selected_locality if selected_locality and selected_locality != "None" else location
        
        # Result display with enhanced cinematic animation
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # Main result with enhanced styling
        st.markdown(f'''
        <div class="result-text">
            😂 {name}, living in {display_location}, your estimated body count is: {score}! 😂
        </div>
        ''', unsafe_allow_html=True)
        
        # Enhanced roast messages
        roast_message = get_roast_message(score)
        st.markdown(f'<div class="roast-message">{roast_message}</div>', unsafe_allow_html=True)
        
        # Locality-specific roast
        if selected_locality and selected_locality != "None":
            locality_roast = get_locality_roast(selected_locality)
            if locality_roast:
                st.markdown(f'<div class="roast-message">{locality_roast}</div>', unsafe_allow_html=True)
        
        # Score interpretation with visual elements
        if score >= 80:
            st.markdown('<div class="roast-message">🔥 You\'re practically a legend! The streets know your name! 🔥</div>', 
                       unsafe_allow_html=True)
        elif score >= 60:
            st.markdown('<div class="roast-message">💫 Smooth operator detected! You\'ve got game! 💫</div>', 
                       unsafe_allow_html=True)
        elif score >= 40:
            st.markdown('<div class="roast-message">😎 Not bad, not bad! You know how to charm! 😎</div>', 
                       unsafe_allow_html=True)
        elif score >= 20:
            st.markdown('<div class="roast-message">🌟 Sweet and selective! Quality over quantity! 🌟</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="roast-message">👼 Pure soul alert! Your innocence is precious! 👼</div>', 
                       unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced celebration effects
        st.balloons()
        time.sleep(0.5)
        st.snow()
        
        # Interactive save result section
        st.markdown("<br>", unsafe_allow_html=True)
        save_col1, save_col2, save_col3 = st.columns([1, 2, 1])
        
        with save_col2:
            if st.button("💾 Save My Epic Result", use_container_width=True):
                try:
                    filename = save_result_to_csv(name, location, selected_locality, score)
                    st.markdown(f"""
                    <div class="roast-message" style="border-left-color: #4CAF50;">
                        ✅ Your legendary result has been saved to {filename}! 
                        <br>📁 Check the app directory for your data!
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.markdown(f"""
                    <div class="roast-message" style="border-left-color: #ff6b6b;">
                        ❌ Oops! Couldn't save your result: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Enhanced footer with interactive elements
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; opacity: 0.8; font-size: 1rem; padding: 20px;">
        <div style="margin-bottom: 15px;">
            🚫 <strong>Disclaimer:</strong> This is purely for entertainment purposes! Results are completely fictional and humorous. 😄
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7;">
            Made with ❤️ using Streamlit | © 2025 Body Count Detector<br>
            🎭 For entertainment only • 🔮 Results may vary • 😂 Humor guaranteed
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()