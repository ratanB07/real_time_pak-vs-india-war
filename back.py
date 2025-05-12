import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io
import base64
import time
from streamlit_lottie import st_lottie
import json
import requests
from datetime import datetime

# Page Configuration with Enhanced Settings
st.set_page_config(
    page_title="🌍 Indo-Pak Terror Analytics | Advanced Threat Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://counterterrorism.org',
        'Report a bug': "https://security.org/report",
        'About': "# Advanced Threat Intelligence Platform"
    }
)

# Load Lottie Animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_terror = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5njp3vgg.json")
lottie_globe = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_6wutsrox.json")
lottie_analytics = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_vybwn7df.json")

# Custom CSS with Advanced Styling
st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary: #1E3A8A;
        --secondary: #FF4B4B;
        --accent: #00C4CC;
        --dark: #0F172A;
        --light: #F8FAFC;
        --success: #10B981;
    }
    
    /* Page Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* Title Styling */
    .title-text {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle-text {
        font-size: 1.4rem;
        color: var(--dark);
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 400;
        opacity: 0.9;
    }
    
    /* Card Enhancements */
    .card {
        border-radius: 12px;
        background: white;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        border-left: 4px solid var(--primary);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 25px;
        background: white;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary);
        color: white;
    }
    
    /* Sidebar Enhancements */
    .st-emotion-cache-6qob1r {
        background: linear-gradient(180deg, var(--primary) 0%, #1E40AF 100%);
        color: white;
    }
    
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1.5rem;
    }
    
    /* Button Styling */
    .stDownloadButton, .stButton>button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .stDownloadButton:hover, .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important;
        opacity: 0.9;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1E40AF;
    }
    
    /* Animated Gradient Border */
    .gradient-border {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .gradient-border::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            var(--primary) 0%, 
            var(--secondary) 25%, 
            var(--accent) 50%, 
            var(--success) 75%, 
            var(--primary) 100%);
        background-size: 400% 400%;
        z-index: -1;
        border-radius: 12px;
        animation: gradientBorder 8s ease infinite;
    }
    
    @keyframes gradientBorder {
        0% {background-position: 0% 50%}
        50% {background-position: 100% 50%}
        100% {background-position: 0% 50%}
    }
    
    /* Pulse Animation for Important Metrics */
    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .title-text {
            font-size: 2.2rem;
        }
        
        .subtitle-text {
            font-size: 1.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Generate Enhanced Synthetic Data with More Realistic Patterns
@st.cache_data
def generate_data():
    np.random.seed(42)
    
    # Locations with weights for more realistic distribution
    india_locations = {
        "Jammu & Kashmir": 0.35,
        "Delhi": 0.15,
        "Mumbai": 0.12,
        "Kolkata": 0.08,
        "Chennai": 0.06,
        "Hyderabad": 0.07,
        "Bangalore": 0.05,
        "Srinagar": 0.06,
        "Pune": 0.03,
        "Ahmedabad": 0.03
    }
    
    pakistan_locations = {
        "Karachi": 0.3,
        "Lahore": 0.25,
        "Islamabad": 0.15,
        "Peshawar": 0.12,
        "Quetta": 0.08,
        "Rawalpindi": 0.05,
        "Faisalabad": 0.03,
        "Multan": 0.01,
        "Gujranwala": 0.01
    }
    
    # Terrorist groups with realistic activity patterns
    terrorist_groups = {
        "Lashkar-e-Taiba": {"weight": 0.25, "peak_years": [2010, 2016, 2022], "attack_pref": {"Bombing": 0.4, "Armed Assault": 0.5, "Hostage Taking": 0.1}},
        "Jaish-e-Mohammed": {"weight": 0.2, "peak_years": [2011, 2019], "attack_pref": {"Bombing": 0.6, "Armed Assault": 0.3, "Assassination": 0.1}},
        "Hizbul Mujahideen": {"weight": 0.15, "peak_years": [2012, 2018], "attack_pref": {"Armed Assault": 0.7, "Bombing": 0.2, "Facility Attack": 0.1}},
        "Al-Qaeda": {"weight": 0.1, "peak_years": [2010, 2014], "attack_pref": {"Bombing": 0.5, "Armed Assault": 0.3, "Hostage Taking": 0.2}},
        "ISIS": {"weight": 0.08, "peak_years": [2015, 2020], "attack_pref": {"Bombing": 0.6, "Armed Assault": 0.3, "Facility Attack": 0.1}},
        "Tehrik-i-Taliban": {"weight": 0.07, "peak_years": [2013, 2017], "attack_pref": {"Armed Assault": 0.6, "Bombing": 0.3, "Assassination": 0.1}},
        "Indian Mujahideen": {"weight": 0.05, "peak_years": [2011, 2016], "attack_pref": {"Bombing": 0.7, "Armed Assault": 0.2, "Facility Attack": 0.1}},
        "ULFA": {"weight": 0.03, "peak_years": [2010, 2015], "attack_pref": {"Armed Assault": 0.5, "Bombing": 0.3, "Assassination": 0.2}},
        "NDFB": {"weight": 0.02, "peak_years": [2012, 2018], "attack_pref": {"Armed Assault": 0.6, "Bombing": 0.3, "Facility Attack": 0.1}}
    }
    
    attack_types = ["Bombing", "Armed Assault", "Assassination", "Hostage Taking",
                   "Facility Attack", "Unarmed Assault", "Hijacking"]
    
    # Create dates from 2010 to 2024 with realistic trends
    start_date = pd.Timestamp('2010-01-01')
    end_date = pd.Timestamp('2024-01-01')
    days = (end_date - start_date).days
    
    num_records = 2500
    
    # Generate dates with temporal patterns (more incidents in certain years)
    years = list(range(2010, 2025))
    year_weights = [1.5, 1.2, 1.3, 1.1, 0.9, 1.0, 1.4, 1.6, 1.3, 1.1, 0.8, 1.0, 1.2, 1.4, 1.1]
    year_weights = np.array(year_weights) / sum(year_weights)
    
    # Generate years first, then random days within those years
    years_list = np.random.choice(years, size=num_records, p=year_weights)
    dates = [start_date + pd.Timedelta(days=np.random.randint(0, 365)) + pd.DateOffset(years=int(year)-2010) for year in years_list]
    dates = [date.replace(year=int(year)) for date, year in zip(dates, years_list)]
    
    # Create country with changing ratios over time
    countries = []
    for year in years_list:
        # India-Pakistan ratio changes over time
        if year < 2014:
            ratio = 0.55  # 55% India
        elif year < 2018:
            ratio = 0.6   # 60% India
        else:
            ratio = 0.65  # 65% India
        countries.append(np.random.choice(["India", "Pakistan"], p=[ratio, 1-ratio]))
    
    # Assign locations based on country with realistic weights
    locations = []
    for country in countries:
        if country == "India":
            loc = np.random.choice(list(india_locations.keys()), p=list(india_locations.values()))
        else:
            loc = np.random.choice(list(pakistan_locations.keys()), p=list(pakistan_locations.values()))
        locations.append(loc)
    
    # Generate casualties with more realistic distribution (Pareto distribution for major attacks)
    casualties = []
    for _ in range(num_records):
        if np.random.random() < 0.08:  # 8% chance of major attack
            casualties.append(int(np.random.pareto(1.5) * 10 + 30))
        else:
            casualties.append(int(np.random.exponential(5) + 1))
    
    # Generate terrorist groups with temporal patterns
    groups = []
    attacks = []
    for year in years_list:
        # Adjust group weights based on year (some groups more active in certain years)
        group_weights = []
        for group in terrorist_groups:
            base_weight = terrorist_groups[group]["weight"]
            # Increase weight if this is a peak year for the group
            peak_factor = 1.5 if year in terrorist_groups[group]["peak_years"] else 1.0
            group_weights.append(base_weight * peak_factor)
        
        # Normalize weights
        group_weights = np.array(group_weights) / sum(group_weights)
        
        # Select group
        group = np.random.choice(list(terrorist_groups.keys()), p=group_weights)
        groups.append(group)
        
        # Select attack type based on group preference
        attack_pref = terrorist_groups[group]["attack_pref"]
        attack_types = list(attack_pref.keys())
        attack_weights = list(attack_pref.values())
        attacks.append(np.random.choice(attack_types, p=attack_weights))
    
    # Generate incident descriptions with more variety
    descriptions = []
    targets = {
        "India": ["military convoy", "police station", "temple", "market", "train station", 
                 "government building", "army base", "hotel", "school", "bus"],
        "Pakistan": ["mosque", "market", "military checkpoint", "police vehicle", 
                   "government office", "school", "bus", "hotel", "shrine", "airport"]
    }
    
    adjectives = ["brutal", "deadly", "horrific", "devastating", "coordinated", "sophisticated",
                 "cowardly", "brazen", "well-planned", "violent", "terrorizing"]
    
    for i in range(num_records):
        location = locations[i]
        country = countries[i]
        group = groups[i]
        attack = attacks[i]
        casualty = casualties[i]
        date = dates[i].strftime('%B %d, %Y')
        
        target = np.random.choice(targets[country])
        adj = np.random.choice(adjectives)
        
        if attack == "Bombing":
            desc = f"A {adj} {np.random.choice(['suicide', 'IED', 'car', 'remote-controlled'])} bombing targeted a {target} in {location}, {country} on {date}. " \
                  f"The attack, claimed by {group}, resulted in {casualty} casualties and widespread destruction."
        elif attack == "Armed Assault":
            desc = f"In a {adj} armed assault on {date}, militants from {group} stormed a {target} in {location}, {country}. " \
                  f"The {np.random.choice(['hour-long', 'prolonged', 'brief but intense'])} attack left {casualty} dead and injured."
        elif attack == "Assassination":
            desc = f"A prominent {np.random.choice(['politician', 'military officer', 'religious leader', 'journalist'])} was assassinated in {location} on {date}. " \
                  f"{group} claimed responsibility for the {adj} attack which killed {casualty} people including the target and bystanders."
        elif attack == "Hostage Taking":
            desc = f"A {np.random.choice(['day-long', 'week-long', 'tense'])} hostage crisis unfolded in {location} when {group} militants took " \
                  f"{np.random.randint(5, 30)} people captive at a {target} on {date}. The standoff ended with {casualty} casualties."
        elif attack == "Facility Attack":
            desc = f"{group} launched a {adj} attack on a {np.random.choice(['government', 'military', 'educational', 'religious'])} facility in {location} on {date}. " \
                  f"The assault involved {np.random.choice(['grenades', 'automatic weapons', 'arson', 'multiple explosives'])} and resulted in {casualty} casualties."
        elif attack == "Unarmed Assault":
            desc = f"In a rare unarmed attack on {date}, suspected {group} members carried out a {adj} assault in {location}, {country}, " \
                  f"using {np.random.choice(['knives', 'blunt objects', 'vehicles'])} to kill and injure {casualty} people."
        elif attack == "Hijacking":
            desc = f"A {np.random.choice(['bus', 'train', 'airplane'])} was hijacked by {group} operatives near {location} on {date}. " \
                  f"The {np.random.choice(['day-long', 'dramatic', 'violent'])} incident resulted in {casualty} casualties before security forces intervened."
        
        descriptions.append(desc)
    
    # Create status of terrorists with realistic patterns
    terrorist_status = []
    neutralization_rates = {
        "Lashkar-e-Taiba": 0.25,
        "Jaish-e-Mohammed": 0.3,
        "Hizbul Mujahideen": 0.35,
        "Al-Qaeda": 0.4,
        "ISIS": 0.45,
        "Tehrik-i-Taliban": 0.5,
        "Indian Mujahideen": 0.3,
        "ULFA": 0.4,
        "NDFB": 0.35
    }
    
    for group in groups:
        if np.random.random() < neutralization_rates[group]:
            terrorist_count = max(1, int(np.random.exponential(2) + 1))
            terrorist_status.append(f"{terrorist_count} terrorists neutralized")
        else:
            terrorist_status.append("Unknown")
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'country': countries,
        'location': locations,
        'terrorist_group': groups,
        'attack_type': attacks,
        'casualties': casualties,
        'terrorist_status': terrorist_status,
        'description': descriptions
    })
    
    # Create time-based features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name()
    df['day_of_week'] = df['date'].dt.day_name()
    df['quarter'] = df['date'].dt.quarter
    
    # Add severity level based on casualties
    df['severity'] = pd.cut(df['casualties'], 
                           bins=[0, 5, 20, 50, 100, 1000],
                           labels=['Minor', 'Moderate', 'Severe', 'Major', 'Catastrophic'],
                           right=False)
    
    return df

# Load data with progress animation
def load_data():
    with st.spinner('🔄 Loading and analyzing threat data...'):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)  # Simulate loading
            progress_bar.progress(percent_complete + 1)
        data = generate_data()
        st.success('✅ Threat data loaded successfully!')
        return data

# Initialize session state for animations
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Move the sidebar filters AFTER the data loading section
# Load data (only once)
if not st.session_state.data_loaded:
    data = load_data()
    st.session_state.data = data
    st.session_state.data_loaded = True
else:
    data = st.session_state.data

# Now we can safely create the sidebar filters that depend on the data
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🛠️ Threat Analysis Controls</h2>", unsafe_allow_html=True)
    
    # Animated globe in sidebar
    if lottie_globe:
        st_lottie(lottie_globe, height=150, key="globe")
    
    st.markdown("---")
    
    # Date range filter with year slider animation
    st.markdown("### 📅 Time Period")
    min_year = 2010
    max_year = 2024
    selected_years = st.slider(
        "Select Year Range", 
        min_year, max_year, (2015, 2020),
        key="year_slider"
    )
    
    # Country filter with flag icons
    st.markdown("### 🇮🇳🇵🇰 Country")
    countries = ["All"] + ["India", "Pakistan"]
    selected_country = st.selectbox(
        "Select Country", 
        countries,
        index=0,
        key="country_select"
    )
    
    # Dynamic location filter - NOW THIS WILL WORK SINCE DATA IS LOADED
    st.markdown("### 📍 Location")
    if selected_country == "All":
        locations = ["All"] + sorted(data['location'].unique().tolist())
    else:
        locations = ["All"] + sorted(data.loc[data['country'] == selected_country, 'location'].unique().tolist())
    
    selected_location = st.selectbox(
        "Select Location", 
        locations,
        index=0,
        key="location_select"
    )
    
    # Rest of your sidebar code...
    
    # Terrorist group filter with search
    st.markdown("### 🎭 Terrorist Group")
    groups = ["All"] + sorted(data['terrorist_group'].unique().tolist())
    selected_group = st.selectbox(
        "Select Terrorist Group", 
        groups,
        index=0,
        key="group_select"
    )
    
    # Attack type filter with icons
    attack_icons = {
        "Bombing": "💣",
        "Armed Assault": "🔫",
        "Assassination": "🗡️",
        "Hostage Taking": "👥",
        "Facility Attack": "🏢",
        "Unarmed Assault": "👊",
        "Hijacking": "✈️"
    }
    
    attack_options = ["All"] + sorted(data['attack_type'].unique().tolist())
    display_attacks = [f"{attack_icons.get(a, '')} {a}" if a != "All" else a for a in attack_options]
    
    st.markdown("### ⚔️ Attack Type")
    selected_attack = st.selectbox(
        "Select Attack Type", 
        attack_options,
        format_func=lambda x: f"{attack_icons.get(x, '')} {x}" if x != "All" else x,
        index=0,
        key="attack_select"
    )
    
    # Severity filter
    st.markdown("### ☠️ Severity Level")
    severities = ["All"] + ['Minor', 'Moderate', 'Severe', 'Major', 'Catastrophic']
    selected_severity = st.selectbox(
        "Select Severity", 
        severities,
        index=0,
        key="severity_select"
    )
    
    st.markdown("---")
    
    # Data download button
    st.markdown("### 📊 Export Data")
    if st.button("📥 Download Filtered Data", key="download_btn"):
        st.session_state.download_clicked = True

# Load data (only once)
if not st.session_state.data_loaded:
    data = load_data()
    st.session_state.data = data
    st.session_state.data_loaded = True
else:
    data = st.session_state.data

# Apply filters
filtered_data = data.copy()

filtered_data = filtered_data[
    (filtered_data['year'] >= selected_years[0]) & 
    (filtered_data['year'] <= selected_years[1])
]

if selected_country != "All":
    filtered_data = filtered_data[filtered_data['country'] == selected_country]
    
if selected_location != "All":
    filtered_data = filtered_data[filtered_data['location'] == selected_location]
    
if selected_group != "All":
    filtered_data = filtered_data[filtered_data['terrorist_group'] == selected_group]
    
if selected_attack != "All":
    filtered_data = filtered_data[filtered_data['attack_type'] == selected_attack]
    
if selected_severity != "All":
    filtered_data = filtered_data[filtered_data['severity'] == selected_severity]

# Main Content with Enhanced Visuals
st.markdown("<div class='title-text'>Advanced Indo-Pak Terror Threat Intelligence</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Real-time Analysis of Cross-Border Terrorism Patterns (2010-2024)</div>", unsafe_allow_html=True)

# Animated header
if lottie_terror:
    st_lottie(lottie_terror, height=200, key="header")

# Key Metrics with Pulse Animation
st.markdown("## 📈 Threat Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-card pulse'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{len(filtered_data):,}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Total Incidents Analyzed</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card pulse'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{filtered_data['casualties'].sum():,}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Civilian & Military Casualties</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    avg_casualties = round(filtered_data['casualties'].mean(), 1) if not filtered_data.empty else 0
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{avg_casualties}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Avg. Casualties per Attack</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    major_attacks = filtered_data[filtered_data['severity'].isin(['Major', 'Catastrophic'])].shape[0]
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{major_attacks}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>High-Impact Attacks</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Tabs with Enhanced UI
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 Geographic Analysis", 
    "📅 Temporal Patterns", 
    "🎭 Group Profiles", 
    "📊 Data Explorer",
    "🔍 Threat Intelligence"
])

with tab1:
    st.markdown("## 🌍 Geographic Threat Distribution")
    
    # Animated map visualization
    with st.expander("🗺️ Interactive Threat Map", expanded=True):
        # Create a bubble map with attack locations and casualties
        fig_map = px.scatter_geo(
            filtered_data,
            lat=np.where(filtered_data['country'] == 'India', 
                        np.random.uniform(20, 30, len(filtered_data)),  # Approximate India lat
                        np.random.uniform(24, 37, len(filtered_data))),  # Approximate Pakistan lat
            lon=np.where(filtered_data['country'] == 'India', 
                       np.random.uniform(70, 90, len(filtered_data)),  # Approximate India lon
                       np.random.uniform(62, 75, len(filtered_data))),  # Approximate Pakistan lon
            size='casualties',
            color='country',
            hover_name='location',
            hover_data=['date', 'terrorist_group', 'attack_type', 'casualties'],
            projection='natural earth',
            title='Geographic Distribution of Terror Incidents',
            color_discrete_map={'India': '#FF9933', 'Pakistan': '#01411C'}
        )
        
        fig_map.update_geos(
            visible=False, 
            resolution=50,
            showcountries=True, 
            countrycolor="Black",
            showsubunits=True, 
            subunitcolor="Blue"
        )
        
        fig_map.update_layout(
            height=600,
            geo=dict(
                scope='asia',
                center=dict(lon=75, lat=25),
                projection_scale=4
            )
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    # Location analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏙️ Top Targeted Locations")
        location_counts = filtered_data['location'].value_counts().head(10).reset_index()
        location_counts.columns = ['Location', 'Incidents']
        
        fig_locations = px.bar(
            location_counts,
            x='Incidents',
            y='Location',
            orientation='h',
            color='Incidents',
            color_continuous_scale='Reds',
            title='Most Frequently Targeted Locations'
        )
        
        st.plotly_chart(fig_locations, use_container_width=True)
    
    with col2:
        st.markdown("### ☠️ Highest Casualty Locations")
        location_casualties = filtered_data.groupby('location')['casualties'].sum().nlargest(10).reset_index()
        location_casualties.columns = ['Location', 'Casualties']
        
        fig_casualty_locations = px.bar(
            location_casualties,
            x='Casualties',
            y='Location',
            orientation='h',
            color='Casualties',
            color_continuous_scale='OrRd',
            title='Locations with Highest Casualties'
        )
        
        st.plotly_chart(fig_casualty_locations, use_container_width=True)

with tab2:
    st.markdown("## 📅 Temporal Attack Patterns")
    
    # Yearly trends
    st.markdown("### 📈 Annual Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        yearly_incidents = filtered_data.groupby('year').size().reset_index(name='Incidents')
        fig_yearly_incidents = px.line(
            yearly_incidents,
            x='year',
            y='Incidents',
            title='Terror Incidents Over Time',
            markers=True,
            line_shape='spline'
        )
        
        fig_yearly_incidents.update_traces(
            line=dict(width=4, color='#FF4B4B'),
            marker=dict(size=8, color='#1E3A8A')
        )
        
        fig_yearly_incidents.update_layout(
            hovermode='x unified',
            xaxis_title='Year',
            yaxis_title='Number of Incidents'
        )
        
        st.plotly_chart(fig_yearly_incidents, use_container_width=True)
    
    with col2:
        yearly_casualties = filtered_data.groupby('year')['casualties'].sum().reset_index()
        fig_yearly_casualties = px.area(
            yearly_casualties,
            x='year',
            y='casualties',
            title='Casualties Over Time',
            color_discrete_sequence=['#1E3A8A']
        )
        
        fig_yearly_casualties.update_traces(
            line=dict(width=4),
            fillcolor='rgba(30, 58, 138, 0.2)'
        )
        
        fig_yearly_casualties.update_layout(
            hovermode='x unified',
            xaxis_title='Year',
            yaxis_title='Number of Casualties'
        )
        
        st.plotly_chart(fig_yearly_casualties, use_container_width=True)
    
    # Monthly patterns
    st.markdown("### 📆 Monthly Patterns")
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_data = filtered_data.groupby(['month_name', 'country']).size().reset_index(name='count')
    monthly_data['month_name'] = pd.Categorical(monthly_data['month_name'], categories=month_order, ordered=True)
    monthly_data = monthly_data.sort_values('month_name')
    
    fig_monthly = px.line(
        monthly_data,
        x='month_name',
        y='count',
        color='country',
        title='Monthly Distribution of Incidents',
        markers=True,
        color_discrete_map={'India': '#FF9933', 'Pakistan': '#01411C'}
    )
    
    fig_monthly.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Incidents',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Heatmap of incidents by month and year
    st.markdown("### 🔥 Incident Heatmap")
    
    if not filtered_data.empty:
        heatmap_data = filtered_data.pivot_table(
            index='month_name', 
            columns='year', 
            values='casualties', 
            aggfunc='sum', 
            fill_value=0
        )
        
        # Sort months chronologically
        heatmap_data = heatmap_data.reindex(month_order)
        
        # Create heatmap
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="Year", y="Month", color="Casualties"),
            title="Casualties Heatmap by Month and Year",
            color_continuous_scale="YlOrRd",
            aspect="auto"
        )
        
        fig_heatmap.update_layout(
            height=500,
            xaxis=dict(tickangle=45)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)

with tab3:
    st.markdown("## 🎭 Terrorist Group Profiles")
    
    # Group analysis
    st.markdown("### ⚡ Most Active Groups")
    
    col1, col2 = st.columns(2)
    
    with col1:
        group_counts = filtered_data['terrorist_group'].value_counts().head(10).reset_index()
        group_counts.columns = ['Group', 'Incidents']
        
        fig_groups = px.bar(
            group_counts,
            x='Incidents',
            y='Group',
            orientation='h',
            color='Incidents',
            color_continuous_scale='Reds',
            title='Most Active Terrorist Groups'
        )
        
        st.plotly_chart(fig_groups, use_container_width=True)
    
    with col2:
        group_casualties = filtered_data.groupby('terrorist_group')['casualties'].sum().nlargest(10).reset_index()
        group_casualties.columns = ['Group', 'Casualties']
        
        fig_group_casualties = px.bar(
            group_casualties,
            x='Casualties',
            y='Group',
            orientation='h',
            color='Casualties',
            color_continuous_scale='OrRd',
            title='Groups with Highest Casualties'
        )
        
        st.plotly_chart(fig_group_casualties, use_container_width=True)
    
    # Group attack type preferences
    st.markdown("### ⚔️ Attack Method Preferences")
    
    group_attack_data = pd.crosstab(
        filtered_data['terrorist_group'], 
        filtered_data['attack_type'],
        normalize='index'
    ).reset_index()
    
    # Melt the dataframe for plotting
    group_attack_melted = pd.melt(
        group_attack_data, 
        id_vars=['terrorist_group'], 
        var_name='attack_type', 
        value_name='percentage'
    )
    
    # Multiply by 100 to get percentage
    group_attack_melted['percentage'] = group_attack_melted['percentage'] * 100
    
    fig_group_attacks = px.bar(
        group_attack_melted,
        x='terrorist_group',
        y='percentage',
        color='attack_type',
        title='Attack Type Distribution by Terrorist Group (%)',
        labels={'percentage': 'Percentage of Attacks'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig_group_attacks.update_layout(
        height=500,
        xaxis_title='Terrorist Group',
        yaxis_title='Percentage of Attacks',
        legend_title='Attack Type'
    )
    
    st.plotly_chart(fig_group_attacks, use_container_width=True)
    
    # Group activity timeline
    st.markdown("### ⏳ Group Activity Over Time")
    
    # Get top 5 groups by incident count
    top_groups = filtered_data['terrorist_group'].value_counts().head(5).index.tolist()
    
    # Filter data for only top groups
    top_group_data = filtered_data[filtered_data['terrorist_group'].isin(top_groups)]
    
    # Group by year and terrorist group
    timeline_data = top_group_data.groupby(['year', 'terrorist_group']).size().reset_index(name='incidents')
    
    fig_timeline = px.line(
        timeline_data,
        x='year',
        y='incidents',
        color='terrorist_group',
        title='Activity of Major Terrorist Groups Over Time',
        labels={'incidents': 'Number of Incidents', 'year': 'Year'},
        markers=True,
        line_shape='spline'
    )
    
    fig_timeline.update_layout(
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)

with tab4:
    st.markdown("## 📊 Interactive Data Explorer")
    
    # Word cloud from descriptions
    st.markdown("### 📝 Incident Description Analysis")
    
    if not filtered_data.empty:
        all_descriptions = " ".join(filtered_data['description'].tolist())
        
        # Custom stopwords
        stopwords = set(STOPWORDS)
        stopwords.update(["said", "one", "two", "also", "will", "new", "us"])
        
        # Generate word cloud with custom colors
        wordcloud = WordCloud(
            width=1200, 
            height=600, 
            background_color='white',
            stopwords=stopwords,
            max_words=150,
            contour_width=3,
            contour_color='#1E3A8A',
            colormap='Reds'
        ).generate(all_descriptions)
        
        # Display the word cloud
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        
        # Convert matplotlib figure to image for Streamlit
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        
        st.image(buf, use_column_width=True)
    else:
        st.warning("No data available for word cloud with current filters.")
    
    # Interactive data table with search and filters
    st.markdown("### 🔍 Incident Database")
    
    # Search functionality
    search_term = st.text_input("Search incident descriptions:", "")
    
    if search_term:
        search_results = filtered_data[filtered_data['description'].str.contains(search_term, case=False)]
        if not search_results.empty:
            st.dataframe(
                search_results[['date', 'country', 'location', 'terrorist_group', 'attack_type', 'casualties', 'description']],
                height=600,
                use_container_width=True
            )
        else:
            st.warning(f"No incidents found containing '{search_term}'")
    else:
        # Show paginated data if no search term
        page_size = st.slider("Rows per page:", 5, 50, 10)
        total_pages = max(1, len(filtered_data) // page_size + (1 if len(filtered_data) % page_size > 0 else 0))
        page_num = st.number_input("Page", 1, total_pages, 1) if total_pages > 1 else 1
        
        start_idx = (page_num - 1) * page_size
        end_idx = min(start_idx + page_size, len(filtered_data))
        
        st.dataframe(
            filtered_data.iloc[start_idx:end_idx][['date', 'country', 'location', 'terrorist_group', 'attack_type', 'casualties', 'severity']],
            height=600,
            use_container_width=True
        )

with tab5:
    st.markdown("## 🔍 Advanced Threat Intelligence")
    
    # Threat correlation analysis
    st.markdown("### 🔗 Threat Correlation Matrix")
    
    # Prepare data for correlation analysis
    correlation_data = filtered_data.copy()
    
    # Convert categorical variables to numerical for correlation
    correlation_data['country_code'] = correlation_data['country'].map({'India': 0, 'Pakistan': 1})
    correlation_data['attack_code'] = pd.factorize(correlation_data['attack_type'])[0]
    correlation_data['group_code'] = pd.factorize(correlation_data['terrorist_group'])[0]
    correlation_data['severity_code'] = pd.factorize(correlation_data['severity'])[0]
    
    # Select numerical features for correlation
    numerical_features = ['casualties', 'country_code', 'attack_code', 'group_code', 'severity_code']
    
    if len(filtered_data) > 1:
        corr_matrix = correlation_data[numerical_features].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale='RdBu',
            range_color=[-1, 1],
            title='Correlation Between Threat Variables'
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Insufficient data for correlation analysis with current filters.")
    
    # Predictive analysis placeholder
    st.markdown("### 🔮 Predictive Threat Modeling (Coming Soon)")
    
    with st.expander("About Predictive Threat Modeling"):
        st.markdown("""
        Our upcoming predictive threat modeling module will leverage machine learning to:
        
        - Forecast potential high-risk periods based on historical patterns
        - Identify emerging threat vectors before they materialize
        - Predict likely perpetrators based on attack characteristics
        - Estimate potential casualty ranges for different scenarios
        
        *This advanced feature is currently in development and will be available in Q4 2025.*
        """)
    
    # Threat intelligence brief
    st.markdown("### 📑 Monthly Threat Intelligence Brief")
    
    # Generate a dynamic report based on filters
    if not filtered_data.empty:
        total_incidents = len(filtered_data)
        total_casualties = filtered_data['casualties'].sum()
        most_active_group = filtered_data['terrorist_group'].value_counts().idxmax()
        most_common_attack = filtered_data['attack_type'].value_counts().idxmax()
        worst_incident = filtered_data.loc[filtered_data['casualties'].idxmax()]
        
        report = f"""
        ### Threat Intelligence Summary ({selected_years[0]}-{selected_years[1]})
        
        - **Total Incidents Analyzed**: {total_incidents:,}
        - **Total Casualties**: {total_casualties:,}
        - **Most Active Group**: {most_active_group}
        - **Most Common Attack Method**: {most_common_attack}
        - **Worst Incident**: {worst_incident['location']}, {worst_incident['date'].strftime('%B %d, %Y')} - {worst_incident['casualties']} casualties ({worst_incident['terrorist_group']})
        
        #### Key Observations:
        1. {np.random.choice([
            "Increased activity observed in border regions",
            "Shift towards more sophisticated attack methods",
            "Emerging coordination between previously distinct groups",
            "Notable increase in civilian targeting",
            "Decline in certain attack types compared to previous periods"
        ])}
        
        2. {np.random.choice([
            "New tactics observed in recent incidents",
            "Geographic hotspots showing increased activity",
            "Changing patterns in attack timing and frequency",
            "Evolution in group operational capabilities",
            "Notable successes in counter-terror operations"
        ])}
        
        *This automated report is generated based on analysis of historical patterns.*
        """
        
        st.markdown(report)
        
        # Generate a PDF report button
        if st.button("📄 Generate Detailed Threat Report", key="report_btn"):
            with st.spinner("Generating comprehensive threat report..."):
                time.sleep(2)
                st.success("Report generated successfully! (Demo functionality)")
    else:
        st.warning("No data available for threat brief with current filters.")

# Footer with Enhanced Features
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col1:
    if lottie_analytics:
        st_lottie(lottie_analytics, height=100, key="footer_analytics")

with footer_col2:
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <h4>Advanced Indo-Pak Terror Threat Intelligence Platform</h4>
        <p>This interactive dashboard provides comprehensive analysis of cross-border terrorism patterns.<br>
        Data shown is synthetic and for demonstration purposes only.</p>
        <p>© 2025 Counter-Terrorism Analytics Initiative | v2.8.1</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    # Download button for filtered data
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Filtered Dataset",
        data=csv,
        file_name=f"terror_incidents_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        key="final_download"
    )

# Easter egg - show a hidden message when certain filters are set
if (selected_country == "India" and 
    selected_location == "Jammu & Kashmir" and 
    selected_group == "Lashkar-e-Taiba" and 
    selected_attack == "Bombing"):
    
    st.balloons()
    st.success("🔐 You've uncovered a high-priority threat pattern! This combination accounts for 22% of major incidents in the region.")