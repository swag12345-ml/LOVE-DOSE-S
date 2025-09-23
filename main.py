import streamlit as st
import random
import csv
import os
from datetime import datetime
import time
import base64
from io import BytesIO
from xhtml2pdf import pisa
from PIL import Image

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
if 'profile_image' not in st.session_state:
    st.session_state.profile_image = None

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
    
    /* Aura Tips Card */
    .aura-card {{
        background: {bg_secondary};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 25px;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 
            0 20px 40px rgba(102, 126, 234, 0.2),
            0 8px 20px rgba(102, 126, 234, 0.1);
        animation: auraReveal 1.5s ease-out;
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
    
    @keyframes auraReveal {{
        0% {{
            transform: translateY(30px);
            opacity: 0;
        }}
        100% {{
            transform: translateY(0);
            opacity: 1;
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
    
    /* Aura tips styling */
    .aura-tip {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        font-size: 1.2rem;
        color: {text_primary};
        text-align: center;
        font-weight: 500;
        animation: tipGlow 3s ease-in-out infinite alternate;
    }}
    
    @keyframes tipGlow {{
        from {{ box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2); }}
        to {{ box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4); }}
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
                            dated_count, clubbing_freq, drink_choice, gender, job, favorite_food,
                            pet_preference, favorite_emoji, dance_skills, social_followers,
                            favorite_hobby, coffee_addiction, height, weight, zodiac_sign,
                            movie_genre, time_preference):
    """Calculate form completion percentage - enhanced with new fields"""
    fields = [name, location or selected_locality, relationship_status, 
              clubbing_freq, drink_choice, gender, job, favorite_food,
              pet_preference, favorite_emoji, favorite_hobby, zodiac_sign, movie_genre, time_preference]
    filled_fields = sum(1 for field in fields if field and str(field).strip())
    # Add numeric fields
    numeric_fields = [dance_skills, social_followers, coffee_addiction, height, weight]
    filled_fields += sum(1 for field in numeric_fields if field is not None and field > 0)
    
    total_fields = len(fields) + len(numeric_fields)
    return min(100, (filled_fields / total_fields) * 100)

def calculate_enhanced_body_count(name, age, location, selected_locality, relationship_status, 
                               dated_count, clubbing_freq, drink_choice, pet_preference, 
                               favorite_emoji, dance_skills, social_followers, favorite_hobby,
                               coffee_addiction, height, weight, zodiac_sign, movie_genre, time_preference):
    """Enhanced body count calculation with new funny parameters"""
    
    # Seed randomness for determinism based on user input
    seed_value = sum(ord(c) for c in name.lower()) + age + len(location.strip())
    random.seed(seed_value)
    
    # Start with random base (0-5) to avoid everyone getting the same score
    score = random.randint(0, 5)
    
    # Original name-based rules - longer names = more mysterious = higher score
    if len(name) % 2 == 0:
        score += 5
    
    # Names starting with certain letters get charm bonus
    if name.lower().startswith(('a', 's', 'p')):
        score += 10
    
    # Rare letters make you unique and attractive
    if any(char in name.lower() for char in ['x', 'z']):
        score += 7
    
    # Unicode codepoint micro-randomness for fair distribution
    score += (sum(ord(c) for c in name)) % 5
    
    # Location-based boosts - some areas are hotspots for romance
    locality_boosts = {
        'Park Street': 20,    # Party central
        'Ballygunge': 15,     # Posh area
        'Salt Lake': 10,      # Tech hub
        'New Town': 10,       # Modern area
        'Rajarhat': 10,       # IT corridor
        'Howrah': 5,          # Traditional
        'Esplanade': 8,       # Business district
        'Garia': 3,           # Residential
        'Behala': 3,          # Quiet area
        'Dum Dum': 3,         # Airport area
        'Jadavpur': 3,        # Student area
        'Tollygunge': 3,      # Film industry
        'Shyambazar': 3       # North Kolkata
    }
    
    if selected_locality and selected_locality != "None":
        score += locality_boosts.get(selected_locality, 0)
    else:
        # General location length boost
        score += len(location.strip()) % 10
        if any(city in location.lower() for city in ['kolkata', 'calcutta']):
            score += 8
    
    # Age-based scoring - prime dating years get higher scores
    if age < 20:
        score += 2      # Young and inexperienced
    elif 20 <= age <= 30:
        score += 10     # Prime dating years
    elif 31 <= age <= 40:
        score += 5      # Experienced but settling down
    else:
        score += 3      # Mature relationships
    
    # Relationship status affects opportunities
    relationship_boosts = {
        'Single': 5,           # Ready to mingle
        'In a Relationship': 10,  # Someone found you attractive
        'Complicated': 15,     # Drama = more stories
        'Married': 2           # Settled down
    }
    score += relationship_boosts.get(relationship_status, 0)
    
    # Clubbing frequency - party people meet more people
    clubbing_boosts = {
        'Sometimes': 5,        # Social but selective
        'Every weekend': 15,   # Party animal
        'I live in the club!': 25  # Club legend
    }
    score += clubbing_boosts.get(clubbing_freq, 0)
    
    # Drink choice reveals personality
    drink_boosts = {
        'Tequila': 10,    # Wild and adventurous
        'Vodka': 7,       # Classic party choice
        'Whiskey': 5      # Sophisticated taste
    }
    score += drink_boosts.get(drink_choice, 0)
    
    # Dating history directly correlates
    if dated_count > 5:
        score += min(20, dated_count * 2)  # Cap to keep realistic
    
    # 🎉 NEW FUNNY PARAMETER BOOSTS - The fun additions!
    
    # Pet preference - pets are conversation starters and show caring nature
    pet_boosts = {
        'Dogs': 8,      # Dog lovers are social and loyal
        'Cats': 5,      # Cat lovers are independent and mysterious  
        'Both': 12,     # Animal lovers are caring and attractive
        'Birds': 3,     # Unique pet choice
        'Fish': 1,      # Low maintenance = low effort in relationships?
        'None': 0       # Missing out on pet charm
    }
    score += pet_boosts.get(pet_preference, 0)
    
    # Favorite emoji reveals flirtiness level
    flirty_emojis = ['😏', '😘', '😉', '🔥', '💕', '😍', '🥰', '💋', '😈']
    if favorite_emoji in flirty_emojis:
        score += 8      # Master of digital flirting
    elif favorite_emoji in ['😂', '🤣', '😁']:
        score += 5      # Funny people are magnet for others
    elif favorite_emoji in ['🤓', '🤔', '😐']:
        score += 2      # Serious types have their appeal too
    
    # Dance skills - smooth moves on dance floor = smooth operator
    if dance_skills >= 8:
        score += 15     # Dance floor legend - everyone wants to dance with you
    elif dance_skills >= 6:
        score += 10     # Pretty good moves - you're fun at parties
    elif dance_skills >= 4:
        score += 5      # Average dancer - at least you try
    elif dance_skills >= 2:
        score += 2      # Beginner but enthusiastic
    # 0-1 dance skills get no boost - sorry, no rhythm no romance
    
    # Social media followers - popularity indicator (sad but true in digital age)
    if social_followers >= 10000:
        score += 20     # Influencer status - people want to be seen with you
    elif social_followers >= 5000:
        score += 15     # Popular person - good social proof
    elif social_followers >= 1000:
        score += 10     # Decent following - you're interesting
    elif social_followers >= 500:
        score += 5      # Some friends - not antisocial
    elif social_followers >= 100:
        score += 2      # Basic social presence
    # Below 100 - either very private or new to social media
    
    # Hobby-based attraction - interesting hobbies make you more attractive
    hobby_boosts = {
        'travelling': 12, 'travel': 12, 'traveling': 12,  # Worldly and adventurous
        'photography': 8,    # Artistic eye and patience
        'music': 10, 'singing': 10,     # Musical talent is attractive
        'dancing': 12,       # Rhythm and body confidence
        'cooking': 9,        # Nurturing and practical skill
        'reading': 6,        # Intellectual but might be introverted
        'gaming': 4,         # Fun but might spend too much time indoors
        'sports': 8,         # Physical fitness and competitive spirit
        'fitness': 10, 'gym': 10,  # Health-conscious and disciplined
        'yoga': 7,           # Flexibility and mindfulness
        'art': 7, 'painting': 7,     # Creative and sensitive
        'writing': 6,        # Articulate but might be introspective
        'movies': 5,         # Common interest, good for dates
        'netflix': 3,        # Couch potato alert
        'sleeping': 1        # Lazy or just honest?
    }
    
    hobby_lower = favorite_hobby.lower() if favorite_hobby else ''
    for hobby, boost in hobby_boosts.items():
        if hobby in hobby_lower:
            score += boost
            break
    
    # Coffee addiction - passionate about coffee = passionate in general
    if coffee_addiction >= 5:
        score += 10     # Coffee addict - you're passionate and probably interesting to talk to
    elif coffee_addiction >= 3:
        score += 5      # Regular coffee drinker - you know what you like
    elif coffee_addiction >= 1:
        score += 2      # Occasional coffee - pretty normal
    # No coffee - either very healthy or missing out on cafe culture
    
    # Height preference - society has standards (unfortunately)
    if height >= 180:  # 6 feet or taller
        score += 8      # Tall and commanding presence
    elif height >= 170:  # 5'7" - decent height
        score += 5      # Good height for most people
    elif height >= 160:  # Average height
        score += 3      # Height isn't everything but...
    # Shorter heights get no boost but personality matters more!
    
    # BMI consideration - fitness level affects attractiveness for many
    if height > 0 and weight > 0:
        bmi = weight / ((height/100) ** 2)
        if 18.5 <= bmi <= 24.9:    # Normal BMI range
            score += 5      # Healthy weight range
        elif 25 <= bmi <= 29.9:    # Slightly overweight
            score += 3      # Still attractive, just a bit more to love
        # Very underweight or overweight get no boost, but beauty is subjective!
    
    # Zodiac sign stereotypes - some signs are considered more attractive
    fire_signs = ['Aries', 'Leo', 'Sagittarius']        # Passionate and energetic
    air_signs = ['Gemini', 'Libra', 'Aquarius']         # Charming and intellectual
    water_signs = ['Cancer', 'Scorpio', 'Pisces']       # Emotional and deep
    earth_signs = ['Taurus', 'Virgo', 'Capricorn']      # Reliable and practical
    
    if zodiac_sign in fire_signs:
        score += 8      # Fire signs are passionate and exciting
    elif zodiac_sign in air_signs:
        score += 6      # Air signs are charming conversationalists
    elif zodiac_sign in water_signs:
        score += 7      # Water signs are emotionally deep and mysterious
    elif zodiac_sign in earth_signs:
        score += 5      # Earth signs are reliable and grounded
    
    # Movie genre preference reveals personality
    genre_boosts = {
        'Romance': 8,        # Hopeless romantic - believes in love
        'Action': 6,         # Adventurous and thrilling personality
        'Comedy': 7,         # Fun personality - loves to laugh
        'Horror': 5,         # Thrill seeker - not easily scared
        'Drama': 4,          # Emotional depth and empathy
        'Sci-Fi': 3,         # Intellectual and imaginative
        'Documentary': 2     # Intellectual but might be boring on dates
    }
    score += genre_boosts.get(movie_genre, 0)
    
    # Time preference affects social opportunities
    if time_preference == 'Night Owl':
        score += 8      # Night people are mysterious and often more fun
    elif time_preference == 'Morning Person':
        score += 5      # Healthy lifestyle and discipline
    elif time_preference == 'Both':
        score += 6      # Flexible and adaptable - can match anyone's schedule
    elif time_preference == 'Neither':
        score += 3      # Honest but might be difficult to plan dates with
    
    # Keep the score realistic - cap between 0 and 100
    # Most people should fall in 10-60 range with occasional higher scores
    final_score = max(0, min(100, score))
    
    return final_score

def get_roast_message(score):
    """Generate humorous roast message based on score"""
    if score <= 10:
        return "Innocent soul 😇 — purity preserved, Netflix and chill means actually watching Netflix!"
    elif score <= 25:
        return "Lowkey romantic 😏 — you've got some game, but you're still figuring it out!"
    elif score <= 45:
        return "Certified Lover ❤️🔥 — you know how to charm, probably have smooth pickup lines!"
    elif score <= 70:
        return "Kolkata's Heartthrob 💃🕺 — you're dangerous, people fall for your charm easily!"
    elif score <= 85:
        return "Legendary Status Unlocked 👑 — you're a walking temptation, the streets know your name!"
    else:
        return "Ultimate Romance God/Goddess 🔥👑 — you're mythical, people write songs about you!"

def get_aura_improvement_tips():
    """Generate 3 random funny aura improvement tips"""
    tips_pool = [
        "✨ Dress like a legend – sparkly shoes = instant charm boost of +50 aura points!",
        "😏 Master the mysterious smile – practice in the mirror daily, but not creepily!",
        "💃🕺 Walk like the floor is your personal runway stage – confidence is magnetic!",
        "📱 Use flirty emojis strategically – they increase your digital aura by 200%!",
        "🍫🍟 Always carry a secret snack – sharing food = sharing hearts (proven science)!",
        "☕ Perfect your coffee order – confidence at cafes attracts fellow caffeine addicts!",
        "🎵 Create a killer playlist – good music taste is more attractive than six-pack abs!",
        "📸 Master the art of selfie angles – your Instagram game directly affects your aura!",
        "🌟 Learn 3 random interesting facts – smart conversations are the new foreplay!",
        "💋 Perfect your voice message game – tone matters more than the actual words!",
        "🕺 Practice your signature dance move – be the person everyone remembers!",
        "😎 Invest in good sunglasses – mystery eyes create intrigue and questions!",
        "🍕 Know the best food spots in your city – foodie knowledge opens hearts and stomachs!",
        "🎭 Develop your storytelling skills – good stories make you unforgettable company!",
        "💫 Learn to give genuine compliments – make people feel special, not just pretty!",
        "🌹 Master the art of timing – know when to text back for maximum impact!",
        "🔥 Confidence is your best accessory – wear it everywhere, even to buy groceries!",
        "🎨 Develop a unique hobby – interesting people attract other interesting people!",
        "💄 Take care of yourself first – self-love literally radiates attractive energy!",
        "🌈 Be authentically weird – your quirks are what make you irreplaceably attractive!",
        "🚀 Learn a new skill every month – growth mindset is incredibly sexy!",
        "🎪 Have at least one party trick – being memorable beats being perfect!",
        "🧠 Read something other than social media – intellectual depth is underrated!",
        "🌺 Smell amazing always – good fragrance lingers in memory longer than looks!"
    ]
    
    # Return 3 random tips to keep it fresh each time
    return random.sample(tips_pool, 3)

def create_profile_pdf(user_data, image_data=None):
    """Create a professional PDF profile report using xhtml2pdf"""
    try:
        # Prepare image data for embedding in PDF if provided
        image_html = ""
        if image_data:
            try:
                # Convert PIL image to base64 for HTML embedding
                buffered = BytesIO()
                # Ensure image is in RGB mode for consistent PDF rendering
                if image_data.mode != 'RGB':
                    image_data = image_data.convert('RGB')
                image_data.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                image_html = f'''
                <div style="text-align: center; margin: 20px 0;">
                    <img src="data:image/png;base64,{img_str}" 
                         style="width: 150px; height: 150px; border-radius: 50%; 
                                object-fit: cover; border: 4px solid #ff6b9d;">
                </div>
                '''
            except Exception as e:
                # If image processing fails, continue without image
                image_html = '<div style="text-align: center; margin: 20px 0;"><p>📷 Image could not be processed</p></div>'
        
        # Create comprehensive HTML content for the PDF report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    margin: 2cm;
                    size: A4;
                }}
                body {{
                    font-family: 'Arial', sans-serif;
                    background: white;
                    color: #333;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    background: linear-gradient(135deg, #ff6b9d, #667eea);
                    color: white;
                    padding: 30px;
                    border-radius: 15px;
                }}
                .header h1 {{
                    font-size: 32px;
                    margin: 0;
                    font-weight: bold;
                }}
                .score-highlight {{
                    background: linear-gradient(45deg, #ff6b9d, #667eea);
                    color: white;
                    padding: 25px;
                    text-align: center;
                    border-radius: 15px;
                    font-size: 28px;
                    font-weight: bold;
                    margin: 30px 0;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                }}
                .section {{
                    margin: 25px 0;
                    padding: 20px;
                    background: #f9f9f9;
                    border-radius: 12px;
                    border-left: 6px solid #ff6b9d;
                }}
                .section h2 {{
                    color: #667eea;
                    margin-top: 0;
                    font-size: 22px;
                    border-bottom: 2px solid #ff6b9d;
                    padding-bottom: 8px;
                }}
                .info-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                }}
                .info-item {{
                    background: white;
                    padding: 12px;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                }}
                .info-item strong {{
                    color: #ff6b9d;
                    display: block;
                    margin-bottom: 5px;
                }}
                .aura-tips {{
                    background: linear-gradient(135deg, rgba(255,107,157,0.1), rgba(102,126,234,0.1));
                    padding: 25px;
                    border-radius: 12px;
                    margin: 25px 0;
                    border: 2px solid #667eea;
                }}
                .tip-item {{
                    margin: 15px 0;
                    padding: 15px;
                    background: white;
                    border-radius: 8px;
                    border-left: 4px solid #ff6b9d;
                    font-size: 14px;
                }}
                .roast-section {{
                    background: linear-gradient(135deg, rgba(255,107,157,0.15), rgba(102,126,234,0.15));
                    padding: 25px;
                    border-radius: 12px;
                    margin: 25px 0;
                    text-align: center;
                    border: 2px dashed #ff6b9d;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    font-size: 12px;
                    color: #666;
                    padding: 20px;
                    background: #f5f5f5;
                    border-radius: 10px;
                }}
                .stats-box {{
                    display: inline-block;
                    background: #667eea;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 20px;
                    margin: 5px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>💕 Body Count Detector - Profile Report 💕</h1>
                <p>Your complete romantic personality analysis</p>
            </div>
            
            {image_html}
            
            <div class="score-highlight">
                🔥 Body Count Score: {user_data['score']} 🔥
            </div>
            
            <div class="section">
                <h2>👤 Personal Information</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Name:</strong> {user_data['name']}
                    </div>
                    <div class="info-item">
                        <strong>Age:</strong> {user_data['age']} years old
                    </div>
                    <div class="info-item">
                        <strong>Gender:</strong> {user_data['gender']}
                    </div>
                    <div class="info-item">
                        <strong>Occupation:</strong> {user_data['job']}
                    </div>
                    <div class="info-item">
                        <strong>Location:</strong> {user_data['location']}
                    </div>
                    <div class="info-item">
                        <strong>Relationship Status:</strong> {user_data['relationship_status']}
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>💕 Relationship & Dating History</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>People Dated:</strong> {user_data['dated_count']} people
                    </div>
                    <div class="info-item">
                        <strong>Clubbing Frequency:</strong> {user_data['clubbing_freq']}
                    </div>
                    <div class="info-item">
                        <strong>Favorite Drink:</strong> {user_data['favorite_drink']}
                    </div>
                    <div class="info-item">
                        <strong>Current Status:</strong> {user_data['relationship_status']}
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎉 Personality & Lifestyle Factors</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Pet Preference:</strong> {user_data['pet_preference']}
                    </div>
                    <div class="info-item">
                        <strong>Favorite Emoji:</strong> {user_data['favorite_emoji']}
                    </div>
                    <div class="info-item">
                        <strong>Dance Skills:</strong> {user_data['dance_skills']}/10
                    </div>
                    <div class="info-item">
                        <strong>Social Media Followers:</strong> {user_data['social_followers']}
                    </div>
                    <div class="info-item">
                        <strong>Favorite Hobby:</strong> {user_data['favorite_hobby']}
                    </div>
                    <div class="info-item">
                        <strong>Coffee Addiction:</strong> {user_data['coffee_addiction']}/10
                    </div>
                    <div class="info-item">
                        <strong>Height:</strong> {user_data['height']} cm
                    </div>
                    <div class="info-item">
                        <strong>Weight:</strong> {user_data['weight']} kg
                    </div>
                    <div class="info-item">
                        <strong>Zodiac Sign:</strong> {user_data['zodiac_sign']}
                    </div>
                    <div class="info-item">
                        <strong>Movie Genre:</strong> {user_data['movie_genre']}
                    </div>
                    <div class="info-item">
                        <strong>Time Preference:</strong> {user_data['time_preference']}
                    </div>
                </div>
            </div>
            
            <div class="roast-section">
                <h2>🔥 The Hilarious Verdict</h2>
                <p style="font-size: 18px; font-weight: bold; color: #333;">
                    {user_data['roast_message']}
                </p>
            </div>
            
            <div class="aura-tips">
                <h2>✨ Your Personalized Aura Improvement Tips</h2>
                <p style="text-align: center; margin-bottom: 20px; font-style: italic;">
                    Follow these scientifically-questionable tips to boost your romantic appeal!
                </p>
        """
        
        # Add each aura tip as a separate item
        for i, tip in enumerate(user_data['aura_tips'], 1):
            html_content += f'<div class="tip-item"><strong>Tip #{i}:</strong> {tip}</div>'
        
        # Complete the HTML
        html_content += f"""
            </div>
            
            <div class="section">
                <h2>📊 Score Breakdown</h2>
                <div style="text-align: center;">
                    <div class="stats-box">Overall Score: {user_data['score']}/100</div>
                    <div class="stats-box">Charm Level: {'🔥' * min(5, user_data['score'] // 20)}</div>
                    <div class="stats-box">Aura Status: {'Legendary' if user_data['score'] > 80 else 'Strong' if user_data['score'] > 60 else 'Growing' if user_data['score'] > 40 else 'Developing'}</div>
                </div>
                <p style="text-align: center; margin-top: 20px; font-style: italic;">
                    Remember: This score is based on completely scientific* algorithms (*not actually scientific)
                </p>
            </div>
            
            <div class="footer">
                <h3>💕 Body Count Detector Report 💕</h3>
                <p><strong>Generated on:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p><strong>Disclaimer:</strong> This report is for entertainment purposes only. Results are completely fictional and humorous.</p>
                <p><strong>Remember:</strong> Your worth isn't determined by any number - you're amazing just as you are! 💖</p>
                <p style="margin-top: 15px; font-size: 10px;">
                    This report contains {len(user_data)} data points analyzed through our proprietary "Romance Algorithm"™<br>
                    No hearts were broken in the making of this report (probably)
                </p>
            </div>
        </body>
        </html>
        """
        
        # Generate PDF using xhtml2pdf
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), result)
        
        if not pdf.err:
            return result.getvalue()
        else:
            st.error(f"PDF generation error: {pdf.err}")
            return None
            
    except Exception as e:
        st.error(f"Error creating PDF: {str(e)}")
        return None

def show_loading_animation():
    """Display an entertaining loading animation with progress"""
    loading_container = st.empty()
    progress_bar = st.progress(0)
    
    # Funny loading messages that change during the process
    loading_messages = [
        "🔮 Analyzing your romantic energy...",
        "💕 Calculating charm coefficients...", 
        "😏 Evaluating flirtation potential...",
        "🕺 Measuring dance floor magnetism...",
        "📱 Processing social media aura...",
        "☕ Computing coffee-powered attraction...",
        "🎭 Finalizing personality profile...",
        "🔥 Generating your legendary score..."
    ]
    
    for i in range(101):
        progress_bar.progress(i)
        
        # Update message based on progress
        message_index = min(len(loading_messages) - 1, i // 13)
        current_message = loading_messages[message_index]
        
        if i % 10 == 0:  # Update every 10%
            loading_container.markdown(f"""
            <div class="loading-container">
                <div class="loading-spinner"></div>
            </div>
            <div style="text-align: center; margin-top: 15px; font-size: 18px; color: #ff6b9d;">
                {current_message} {i}%
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(0.03)  # Slightly slower for dramatic effect
    
    # Clear loading elements
    loading_container.empty()
    progress_bar.empty()

def main():
    """Main Streamlit app with all enhanced features"""
    
    # Sidebar for theme and stats
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        theme_toggle = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_theme)
        if theme_toggle != st.session_state.dark_theme:
            st.session_state.dark_theme = theme_toggle
            st.rerun()
        
        st.markdown("### 📊 Your Stats")
        if st.session_state.show_result and st.session_state.result_data:
            st.metric("Your Score", st.session_state.result_data.get('score', 0))
            st.metric("Form Completion", f"{st.session_state.form_completion:.0f}%")
            
            # Fun score interpretation
            score = st.session_state.result_data.get('score', 0)
            if score >= 80:
                st.success("🔥 Legendary Status!")
            elif score >= 60:
                st.info("💫 High Charm Level!")
            elif score >= 40:
                st.warning("✨ Good Potential!")
            else:
                st.error("😇 Pure Innocence!")
    
    # Inject the advanced CSS styling
    inject_advanced_css(st.session_state.dark_theme)
    
    # Interactive animated main title
    st.markdown('''
    <div class="main-title" onclick="this.style.transform='scale(1.1) rotateY(10deg)'; setTimeout(() => this.style.transform='scale(1) rotateY(0deg)', 200)">
        💕 Body Count Detector 💕
    </div>
    ''', unsafe_allow_html=True)
    
    # Subtitle with hover effects
    st.markdown('<div class="subtitle">Discover your romantic mysteries with AI-powered humor! 😂✨</div>', 
                unsafe_allow_html=True)
    
    # Main input form in glassmorphism container
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # 📸 PROFILE IMAGE UPLOAD SECTION
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📸 Profile Picture (Optional)</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload your photo for the PDF report", 
        type=['png', 'jpg', 'jpeg'], 
        help="This will be included in your personalized PDF profile report. Make it a good one! 😉"
    )
    
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.session_state.profile_image = image
            # Display a small preview centered
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(image, width=150, caption="Profile Preview ✨")
                st.success("📸 Photo uploaded successfully!")
        except Exception as e:
            st.error("❌ Error loading image. Please try a different file format!")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 👤 PERSONAL INFORMATION SECTION
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
        dated_count = st.number_input("💏 How many people have you dated?", min_value=0, value=2, 
                                    help="Be honest! This affects your score calculation.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 📍 LOCATION DETAILS SECTION
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📍 Location Details</div>', unsafe_allow_html=True)
    
    location_col1, location_col2 = st.columns(2)
    
    with location_col1:
        location = st.text_input("🗺️ Your Location", placeholder="Where do you spread your charm?")
    
    with location_col2:
        kolkata_localities = ["None", "Salt Lake", "Park Street", "New Town", "Garia", "Behala", 
                            "Dum Dum", "Ballygunge", "Howrah", "Shyambazar", "Esplanade", 
                            "Rajarhat", "Tollygunge", "Jadavpur"]
        selected_locality = st.selectbox("🏙️ Kolkata Locality (if applicable)", kolkata_localities,
                                       help="Kolkata locals get location-specific bonuses!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 🎉 LIFESTYLE & PREFERENCES SECTION
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
    
    # 😄 ENHANCED FUNNY PARAMETERS SECTION - The main new addition!
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">😄 Extra Fun Facts (New!)</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-style: italic; opacity: 0.8;">These quirky details will spice up your body count calculation! 🌶️</p>', unsafe_allow_html=True)
    
    fun_col1, fun_col2 = st.columns(2)
    
    with fun_col1:
        pet_preference = st.selectbox("🐾 Pet Preference", 
                                    ["Dogs", "Cats", "Both", "Birds", "Fish", "None"],
                                    help="Pet lovers get charm bonuses!")
        
        favorite_emoji = st.selectbox("😄 Your Go-To Emoji", 
                                    ["😂", "😏", "😘", "😉", "🔥", "💕", "😍", "🥰", "💋", "😈", "🤓", "🤔", "😐"],
                                    help="Flirty emojis = higher scores!")
        
        dance_skills = st.slider("💃 Dance Skills (0-10)", min_value=0, max_value=10, value=5,
                               help="Smooth moves on the dance floor = smooth operator in life!")
        
        social_followers = st.number_input("📱 Social Media Followers", min_value=0, value=500,
                                         help="Digital popularity affects your modern dating game!")
        
        favorite_hobby = st.text_input("🎨 Favorite Hobby", placeholder="What makes you interesting?",
                                     help="Interesting hobbies make you more attractive!")
        
    with fun_col2:
        coffee_addiction = st.slider("☕ Coffee Addiction Level (0-10)", min_value=0, max_value=10, value=5,
                                   help="Coffee addicts are passionate people!")
        
        height = st.number_input("📏 Height (cm)", min_value=140, max_value=220, value=170,
                               help="Height matters (unfortunately) in the dating world!")
        
        weight = st.number_input("⚖️ Weight (kg)", min_value=40, max_value=150, value=70,
                               help="Used for BMI calculation - fitness affects attractiveness!")
        
        zodiac_sign = st.selectbox("♈ Zodiac Sign", 
                                 ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"],
                                 help="Some zodiac signs are considered more attractive!")
        
        movie_genre = st.selectbox("🎬 Favorite Movie Genre", 
                                 ["Romance", "Action", "Comedy", "Horror", "Drama", "Sci-Fi", "Documentary"],
                                 help="Your taste in movies reveals your personality!")
    
    time_preference = st.radio("🌅🌙 Are you a...", 
                             ["Morning Person", "Night Owl", "Both", "Neither"],
                             help="Night owls are mysterious, morning people are disciplined!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FORM COMPLETION TRACKING - Enhanced with new parameters
    completion = calculate_form_completion(name, age, location, selected_locality, 
                                         relationship_status, dated_count, clubbing_freq, 
                                         favorite_drink, gender, job, favorite_food,
                                         pet_preference, favorite_emoji, dance_skills, 
                                         social_followers, favorite_hobby, coffee_addiction, 
                                         height, weight, zodiac_sign, movie_genre, time_preference)
    st.session_state.form_completion = completion
    
    # Enhanced progress indicator with animations
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; margin-bottom: 10px; font-size: 18px;">Form Completion: {completion:.0f}%</div>', 
                unsafe_allow_html=True)
    st.markdown(f'''
    <div class="progress-bar">
        <div class="progress-fill" style="width: {completion}%"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Completion encouragement messages
    if completion < 50:
        st.markdown('<p style="text-align: center; color: #ff6b9d;">💡 Fill out more fields for a more accurate (and hilarious) result!</p>', unsafe_allow_html=True)
    elif completion < 80:
        st.markdown('<p style="text-align: center; color: #667eea;">🎯 Almost there! A few more details will make your score epic!</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="text-align: center; color: #4CAF50;">✨ Perfect! You\'re ready for the ultimate revelation!</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main glass card
    
    # 🔮 ENHANCED REVEAL BUTTON WITH 3D EFFECTS
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 REVEAL MY BODY COUNT! 🔮", use_container_width=True):
        
        # Enhanced input validation with playful messages
        if not name.strip():
            st.markdown("""
            <div class="roast-message" style="border-left-color: #ff6b6b;">
                🤔 Hold up! We need your name to work our romance magic! Without it, our algorithms get confused! ✨
            </div>
            """, unsafe_allow_html=True)
            return
        
        if not location.strip() and (not selected_locality or selected_locality == "None"):
            st.markdown("""
            <div class="roast-message" style="border-left-color: #ff6b6b;">
                📍 Where are you from? We need to know your hunting grounds to calculate your territorial charm bonus! 😏
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Show entertaining loading animation
        show_loading_animation()
        
        # Sound effect simulation with visual feedback
        st.markdown('<div class="sound-effect">🎉</div>', unsafe_allow_html=True)
        
        # ENHANCED BODY COUNT CALCULATION with all new parameters
        score = calculate_enhanced_body_count(name, age, location, selected_locality, 
                                           relationship_status, dated_count, clubbing_freq, 
                                           favorite_drink, pet_preference, favorite_emoji, 
                                           dance_skills, social_followers, favorite_hobby,
                                           coffee_addiction, height, weight, zodiac_sign, 
                                           movie_genre, time_preference)
        
        # Generate personalized aura improvement tips
        aura_tips = get_aura_improvement_tips()
        
        # Store comprehensive result data for PDF generation
        st.session_state.result_data = {
            'name': name,
            'age': age,
            'gender': gender,
            'job': job,
            'location': selected_locality if selected_locality and selected_locality != "None" else location,
            'relationship_status': relationship_status,
            'dated_count': dated_count,
            'clubbing_freq': clubbing_freq,
            'favorite_drink': favorite_drink,
            'pet_preference': pet_preference,
            'favorite_emoji': favorite_emoji,
            'dance_skills': dance_skills,
            'social_followers': social_followers,
            'favorite_hobby': favorite_hobby,
            'coffee_addiction': coffee_addiction,
            'height': height,
            'weight': weight,
            'zodiac_sign': zodiac_sign,
            'movie_genre': movie_genre,
            'time_preference': time_preference,
            'score': score,
            'roast_message': get_roast_message(score),
            'aura_tips': aura_tips
        }
        st.session_state.show_result = True
        
        # 🎭 CINEMATIC RESULT DISPLAY WITH ADVANCED ANIMATIONS
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # Main result with enhanced 3D styling and animations
        st.markdown(f'''
        <div class="result-text">
            😂 {name}, your estimated body count is: {score}! 😂
        </div>
        ''', unsafe_allow_html=True)
        
        # Enhanced roast messages with better styling
        roast_message = get_roast_message(score)
        st.markdown(f'<div class="roast-message">{roast_message}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ✨ AURA IMPROVEMENT TIPS SECTION - Major new feature!
        st.markdown('<div class="aura-card">', unsafe_allow_html=True)
        st.markdown(f'''
        <div style="text-align: center; font-size: 2rem; font-weight: bold; 
                    color: #667eea; margin-bottom: 20px;">
            ✨ Your Personalized Aura Improvement Tips ✨
        </div>
        <div style="text-align: center; margin-bottom: 25px; font-style: italic; opacity: 0.9;">
            Follow these scientifically-questionable but hilariously effective tips to boost your romantic appeal! 💫
        </div>
        ''', unsafe_allow_html=True)
        
        # Display each aura tip with individual animations
        for i, tip in enumerate(aura_tips, 1):
            st.markdown(f'<div class="aura-tip">💡 <strong>Tip #{i}:</strong> {tip}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced celebration effects
        st.balloons()  # First celebration
        time.sleep(0.5)
        st.snow()      # Second celebration for extra drama
        
        # 📄 PDF GENERATION & CSV SAVING SECTION - Enhanced functionality
        st.markdown("<br>", unsafe_allow_html=True)
        pdf_col1, pdf_col2 = st.columns(2)
        
        with pdf_col1:
            if st.button("💾 Save CSV Result", use_container_width=True):
                try:
                    filename = "body_count_results.csv"
                    file_exists = os.path.isfile(filename)
                    
                    # Save comprehensive data to CSV
                    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                        fieldnames = ['Name', 'Age', 'Location', 'Score', 'Relationship_Status', 'Timestamp']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        
                        if not file_exists:
                            writer.writeheader()
                        
                        writer.writerow({
                            'Name': name,
                            'Age': age,
                            'Location': st.session_state.result_data['location'],
                            'Score': score,
                            'Relationship_Status': relationship_status,
                            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                    
                    st.markdown(f"""
                    <div class="roast-message" style="border-left-color: #4CAF50;">
                        ✅ Your epic result has been saved to {filename}! Now you have permanent proof of your romantic prowess! 📁✨
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.markdown(f"""
                    <div class="roast-message" style="border-left-color: #ff6b6b;">
                        ❌ Oops! Error saving your legendary status: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
        
        with pdf_col2:
            if st.button("📄 Download Profile PDF", use_container_width=True):
                try:
                    with st.spinner("🎨 Creating your beautiful PDF profile..."):
                        pdf_data = create_profile_pdf(st.session_state.result_data, 
                                                    st.session_state.profile_image)
                    
                    if pdf_data:
                        st.download_button(
                            label="⬇️ Download Your Epic Profile PDF",
                            data=pdf_data,
                            file_name=f"{name.replace(' ', '_')}_body_count_profile.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            help="Get a comprehensive PDF report with all your data and tips!"
                        )
                        st.markdown("""
                        <div class="roast-message" style="border-left-color: #4CAF50;">
                            🎉 Your personalized PDF profile is ready for download! Share it with friends (or don't... that's probably smarter)! 📄✨
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="roast-message" style="border-left-color: #ff6b6b;">
                            ❌ PDF creation failed. Even our algorithms are shocked by your results! Please try again!
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="roast-message" style="border-left-color: #ff6b6b;">
                        ❌ PDF Error: {str(e)} - Our PDF generator couldn't handle your awesomeness!
                    </div>
                    """, unsafe_allow_html=True)
    
    # ENHANCED FOOTER with additional information
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; opacity: 0.8; font-size: 1rem; padding: 20px;">
        <div style="margin-bottom: 20px; font-size: 1.1rem;">
            🚫 <strong>Important Disclaimer:</strong> This is purely for entertainment! Results are completely fictional and humorous. 😄<br>
            Your actual worth as a person is immeasurable and not determined by any algorithm! 💖
        </div>
        <div style="font-size: 0.9rem; opacity: 0.7; line-height: 1.6;">
            Made with ❤️ using Streamlit & Python | © 2025 Body Count Detector<br>
            🎭 For entertainment only • 🔮 Results may vary • 😂 Humor guaranteed • 💕 Love yourself first<br>
            <br>
            <strong>Features:</strong> Advanced PDF Reports • Aura Improvement Tips • 15+ Fun Parameters • CSV Export<br>
            <strong>New in this version:</strong> Enhanced UI/UX • Profile Pictures • Personalized Tips • Better Calculations
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the enhanced app
if __name__ == "__main__":
    main()
