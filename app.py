import streamlit as st
import pandas as pd
import datetime as dt
import random as rd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import turtle
import io
from PIL import Image, ImageDraw, ImageFont
import math

st.set_page_config(page_title="ShopImpact", layout="wide", page_icon="🌿", initial_sidebar_state="collapsed")

if 'purchase_history' not in st.session_state:
    st.session_state.purchase_history = []

if 'achievement_collection' not in st.session_state:
    st.session_state.achievement_collection = []

if 'current_co2' not in st.session_state:
    st.session_state.current_co2 = 0.0

if 'eco_insights_index' not in st.session_state:
    st.session_state.eco_insights_index = 0

environmental_factors = {
    "Fashion": {"fast_fashion": 4.2, "ethical": 1.5, "vintage": 0.6},
    "Electronics": {"new": 5.1, "refurbished": 2.3, "repaired": 1.2},
    "Food & Beverage": {"imported": 3.4, "local": 1.3, "organic": 0.9},
    "Home Decor": {"mass_produced": 3.8, "handmade": 1.7, "upcycled": 0.8},
    "Personal Care": {"conventional": 2.7, "natural": 1.4, "package_free": 0.7}
}

sustainable_brands = {
    "Fashion": ["Patagonia", "Reformation", "Kotn", "Tentree", "Pangaia"],
    "Electronics": ["Fairphone", "Framework", "Teracube", "Shiftphone"],
    "Food & Beverage": ["Imperfect Foods", "Thrive Market", "Local Harvest"],
    "Home Decor": ["Sabai Design", "The Citizenry", "VivaTerra"],
    "Personal Care": ["Ethique", "Plaine Products", "Meow Meow Tweet"]
}

achievement_criteria = {
    "Eco Pioneer": {"threshold": 3, "desc": "First sustainable purchases"},
    "Carbon Crusader": {"threshold": 100, "desc": "Reduced 100kg CO₂"},
    "Green Visionary": {"threshold": 10, "desc": "10+ eco purchases"},
    "Conscious Consumer": {"threshold": 500, "desc": "$500 green spending"},
    "Planet Protector": {"threshold": 50, "desc": "50% lower footprint"}
}

eco_wisdom = [
    "Bamboo absorbs 35% more CO₂ than equivalent trees",
    "Circular fashion reduces water usage by 20,000L per kg",
    "Local produce travels 90% fewer miles",
    "Refurbished electronics save 80% raw materials",
    "Package-free shopping eliminates 300g plastic weekly"
]

inspirational_messages = [
    "Small choices create seismic shifts",
    "Your cart votes for the world you want",
    "Sustainability is the ultimate innovation",
    "Every purchase plants a seed of change",
    "Conscious consumption rewrites futures"
]

def create_turtle_eco_leaf(size=100):
    buffer = io.BytesIO()
    
    canvas_width = size * 2
    canvas_height = size * 2
    
    screen = turtle.TurtleScreen(turtle.TurtleGraphicsError)
    t = turtle.RawTurtle(screen)
    
    img = Image.new('RGB', (canvas_width, canvas_height), color=(240, 248, 240))
    draw = ImageDraw.Draw(img)
    
    t.speed(0)
    t.hideturtle()
    t.penup()
    t.goto(0, -size//2)
    t.pendown()
    
    t.fillcolor("#2E8B57")
    t.begin_fill()
    
    for _ in range(2):
        t.circle(size, 60)
        t.circle(size//2, 60)
        t.circle(size, 60)
        t.circle(size//2, 60)
    
    t.end_fill()
    
    t.penup()
    t.goto(0, -size//3)
    t.pendown()
    t.color("#8FBC8F")
    t.width(3)
    t.setheading(90)
    t.forward(size)
    
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def create_turtle_footprint(size=80):
    buffer = io.BytesIO()
    
    canvas_width = size * 3
    canvas_height = size * 3
    
    screen = turtle.TurtleScreen(turtle.TurtleGraphicsError)
    t = turtle.RawTurtle(screen)
    
    img = Image.new('RGB', (canvas_width, canvas_height), color=(255, 250, 240))
    draw = ImageDraw.Draw(img)
    
    t.speed(0)
    t.hideturtle()
    t.penup()
    
    t.goto(0, 0)
    t.pendown()
    t.color("#A0522D")
    t.fillcolor("#DEB887")
    
    t.begin_fill()
    for i in range(5):
        t.circle(size//4, 180)
        t.right(108)
    t.end_fill()
    
    for angle in [0, 72, 144, 216, 288]:
        t.penup()
        t.goto(0, 0)
        t.setheading(angle)
        t.forward(size//2)
        t.pendown()
        t.circle(size//8)
    
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def create_turtle_badge(size=60, badge_type="eco"):
    buffer = io.BytesIO()
    
    canvas_width = size * 2
    canvas_height = size * 2
    
    screen = turtle.TurtleScreen(turtle.TurtleGraphicsError)
    t = turtle.RawTurtle(screen)
    
    img = Image.new('RGB', (canvas_width, canvas_height), color=(245, 255, 245))
    draw = ImageDraw.Draw(img)
    
    t.speed(0)
    t.hideturtle()
    t.penup()
    
    colors = {
        "eco": ("#228B22", "#32CD32"),
        "savings": ("#FFD700", "#FFEC8B"),
        "impact": ("#1E90FF", "#87CEFA")
    }
    
    color1, color2 = colors.get(badge_type, ("#228B22", "#32CD32"))
    
    t.goto(0, -size//2)
    t.pendown()
    t.color(color1)
    t.fillcolor(color2)
    
    t.begin_fill()
    for _ in range(8):
        t.circle(size, 45)
        t.circle(size//3, 45)
    t.end_fill()
    
    t.penup()
    t.goto(0, 0)
    t.color("#FFFFFF")
    t.write("★", align="center", font=("Arial", size//2, "bold"))
    
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def generate_radial_chart(data):
    categories = list(data.keys())
    values = list(data.values())
    
    colors = ['#2E8B57', '#3CB371', '#66CDAA', '#8FBC8F', '#20B2AA']
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textinfo='label+percent',
        insidetextorientation='radial'
    )])
    
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.main-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    padding: 20px;
}

.header-gradient {
    background: linear-gradient(90deg, #2E8B57 0%, #3CB371 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glass-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
    padding: 25px;
    margin-bottom: 25px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
}

.eco-badge {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(45deg, #FFD700, #FFEC8B);
    color: #8B4513;
    padding: 8px 20px;
    border-radius: 50px;
    margin: 8px;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    animation: badgeGlow 2s infinite alternate;
    border: 2px solid #FFD700;
}

.impact-number {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #FF416C, #FF4B2B);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.positive-impact {
    background: linear-gradient(90deg, #00b09b, #96c93d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.eco-tip-box {
    background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
    border-left: 5px solid #0097A7;
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    animation: slideIn 0.5s ease-out;
}

.turtle-canvas {
    border: 2px dashed #2E8B57;
    border-radius: 15px;
    padding: 15px;
    background: #FAFFF5;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 200px;
}

.purchase-input {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #2E8B57;
    border-radius: 15px;
    padding: 20px;
}

.stButton > button {
    background: linear-gradient(90deg, #2E8B57, #3CB371);
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 25px;
    font-weight: 600;
    transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
}

.stSelectbox, .stNumberInput, .stTextInput {
    border-radius: 10px;
    border: 2px solid #3CB371;
}

@keyframes badgeGlow {
    0% { box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3); }
    100% { box-shadow: 0 4px 25px rgba(255, 215, 0, 0.6); }
}

@keyframes slideIn {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.animated-title {
    animation: pulse 2s infinite;
}

.co2-meter {
    height: 20px;
    background: linear-gradient(90deg, #00b09b, #96c93d, #FFD700, #FF416C);
    border-radius: 10px;
    margin: 10px 0;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    transition: width 1s ease;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown('<h1 class="header-gradient animated-title" style="text-align:center; font-size:3.5rem;">🌿 ShopImpact</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.2rem; color:#556B2F; margin-bottom:30px;">Transform Your Shopping Into Environmental Action</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#2E8B57;">➕ Log New Purchase</h3>', unsafe_allow_html=True)
    
    category = st.selectbox("Product Category", list(environmental_factors.keys()))
    production_type = st.selectbox("Production Type", ["fast_fashion", "ethical", "vintage", "new", "refurbished", "repaired", 
                                                      "imported", "local", "organic", "mass_produced", "handmade", "upcycled", 
                                                      "conventional", "natural", "package_free"])
    purchase_value = st.number_input("Purchase Amount ($)", min_value=1.0, value=50.0, step=10.0)
    item_brand = st.text_input("Brand/Item Name", value="Sustainable Choice")
    
    if st.button("Calculate Environmental Impact", key="calc_btn"):
        impact_multiplier = 2.5
        
        for cat, types in environmental_factors.items():
            if production_type in types:
                impact_multiplier = types[production_type]
                break
        
        co2_emission = round(purchase_value * impact_multiplier, 2)
        
        new_purchase = {
            "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "type": production_type,
            "brand": item_brand,
            "amount": purchase_value,
            "co2": co2_emission,
            "multiplier": impact_multiplier
        }
        
        st.session_state.purchase_history.append(new_purchase)
        st.session_state.current_co2 += co2_emission
        
        if impact_multiplier < 1.5:
            st.balloons()
            st.success(f"🌱 Eco-Friendly! Only {co2_emission}kg CO₂")
            if "Eco Pioneer" not in st.session_state.achievement_collection:
                st.session_state.achievement_collection.append("Eco Pioneer")
            
            leaf_img = create_turtle_eco_leaf()
            st.image(leaf_img, caption="Eco Leaf Generated with Turtle", use_column_width=True)
        else:
            st.warning(f"⚠️ Impact: {co2_emission}kg CO₂")
            footprint_img = create_turtle_footprint()
            st.image(footprint_img, caption="Carbon Footprint Visualization", use_column_width=True)
        
        current_tip = eco_wisdom[st.session_state.eco_insights_index % len(eco_wisdom)]
        st.session_state.eco_insights_index += 1
        
        st.markdown(f'<div class="eco-tip-box">💡 {current_tip}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#2E8B57;">🏆 Earned Achievements</h3>', unsafe_allow_html=True)
    
    if st.session_state.achievement_collection:
        cols = st.columns(2)
        for idx, badge in enumerate(st.session_state.achievement_collection):
            with cols[idx % 2]:
                badge_img = create_turtle_badge(badge_type="eco" if idx%3==0 else "savings" if idx%3==1 else "impact")
                st.image(badge_img, use_column_width=True)
                st.markdown(f'<div class="eco-badge" style="justify-content:center;">{badge}</div>', unsafe_allow_html=True)
    else:
        st.info("Make sustainable purchases to unlock achievements!")
        
        sample_badge = create_turtle_badge()
        st.image(sample_badge, caption="Sample Achievement Badge", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#2E8B57;">📊 Impact Dashboard</h3>', unsafe_allow_html=True)
    
    if st.session_state.purchase_history:
        df_purchases = pd.DataFrame(st.session_state.purchase_history)
        df_purchases['timestamp'] = pd.to_datetime(df_purchases['timestamp'])
        
        total_expenditure = df_purchases['amount'].sum()
        total_emissions = df_purchases['co2'].sum()
        avg_efficiency = total_emissions / total_expenditure if total_expenditure > 0 else 0
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown('<p style="text-align:center; margin-bottom:0;">Total Spending</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="impact-number" style="text-align:center;">${total_expenditure:.0f}</h2>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<p style="text-align:center; margin-bottom:0;">CO₂ Emissions</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="impact-number" style="text-align:center;">{total_emissions:.1f}kg</h2>', unsafe_allow_html=True)
        with col_c:
            st.markdown('<p style="text-align:center; margin-bottom:0;">Efficiency</p>', unsafe_allow_html=True)
            st.markdown(f'<h2 class="positive-impact" style="text-align:center; font-size:2.5rem;">{avg_efficiency:.2f}kg/$</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="co2-meter"><div class="meter-fill" style="width:70%;"></div></div>', unsafe_allow_html=True)
        
        category_data = df_purchases.groupby('category')['co2'].sum().to_dict()
        fig_chart = generate_radial_chart(category_data)
        st.plotly_chart(fig_chart, use_container_width=True)
        
        st.markdown("**Recent Purchases:**")
        recent_data = df_purchases.tail(5)[['timestamp', 'category', 'brand', 'amount', 'co2']]
        st.dataframe(recent_data.style.format({'amount':'${:.1f}', 'co2':'{:.1f} kg'}))
    else:
        st.info("Start logging purchases to see your environmental impact dashboard.")
        
        sample_data = {"Fashion": 45, "Electronics": 30, "Food": 25}
        fig_sample = generate_radial_chart(sample_data)
        st.plotly_chart(fig_sample, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:#2E8B57;">🌍 Sustainable Alternatives</h3>', unsafe_allow_html=True)
    
    selected_category = st.selectbox("Explore Category", list(sustainable_brands.keys()), key="alt_select")
    
    if selected_category in sustainable_brands:
        alternatives = sustainable_brands[selected_category]
        
        st.markdown("**Recommended Sustainable Brands:**")
        for alt in alternatives:
            col_x, col_y = st.columns([1, 4])
            with col_x:
                st.markdown("✅")
            with col_y:
                st.markdown(f"**{alt}**")
        
        reduction_potential = len(st.session_state.purchase_history) * 2.3
        st.markdown(f'<div style="background:#E8F5E9; padding:15px; border-radius:10px; margin-top:15px;">📈 Potential CO₂ Reduction: **{reduction_potential:.1f}kg** with sustainable choices</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h3 style="color:#2E8B57; text-align:center;">🎨 Interactive Turtle Graphics</h3>', unsafe_allow_html=True)

graphic_col1, graphic_col2, graphic_col3 = st.columns(3)

with graphic_col1:
    st.markdown('<div class="turtle-canvas">', unsafe_allow_html=True)
    st.markdown("**Eco Leaf Generator**")
    if st.button("Generate Leaf", key="leaf_btn"):
        leaf_art = create_turtle_eco_leaf(80)
        st.image(leaf_art, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with graphic_col2:
    st.markdown('<div class="turtle-canvas">', unsafe_allow_html=True)
    st.markdown("**Carbon Footprint**")
    if st.button("Show Footprint", key="footprint_btn"):
        footprint_art = create_turtle_footprint(60)
        st.image(footprint_art, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with graphic_col3:
    st.markdown('<div class="turtle-canvas">', unsafe_allow_html=True)
    st.markdown("**Achievement Badge**")
    badge_choice = st.selectbox("Badge Type", ["eco", "savings", "impact"], key="badge_select")
    if st.button("Create Badge", key="badge_btn"):
        badge_art = create_turtle_badge(50, badge_choice)
        st.image(badge_art, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h3 style="color:#2E8B57;">💭 Daily Inspiration</h3>', unsafe_allow_html=True)

current_message = inspirational_messages[rd.randint(0, len(inspirational_messages)-1)]
st.markdown(f'<div style="font-size:1.6rem; text-align:center; padding:25px; background:linear-gradient(135deg, #FFF8E1, #FFECB3); border-radius:15px; border:2px dashed #FFB300;">{current_message}</div>', unsafe_allow_html=True)

if st.button("Refresh Inspiration", key="inspire_btn"):
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.purchase_history:
    total_co2 = sum(p['co2'] for p in st.session_state.purchase_history)
    eco_purchases = sum(1 for p in st.session_state.purchase_history if p['multiplier'] < 2.0)
    
    if total_co2 < 150 and "Carbon Crusader" not in st.session_state.achievement_collection:
        st.session_state.achievement_collection.append("Carbon Crusader")
        st.toast("🏆 New Achievement: Carbon Crusader!", icon="🎉")
    
    if eco_purchases >= 5 and "Green Visionary" not in st.session_state.achievement_collection:
        st.session_state.achievement_collection.append("Green Visionary")
        st.toast("🏆 New Achievement: Green Visionary!", icon="🌟")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:40px; padding:20px; border-top:2px solid #2E8B57;">
    <p style="color:#556B2F; font-size:0.9rem;">
        ShopImpact v2.0 • Built with Streamlit & Turtle Graphics • 
        <a href="https://streamlit.io/cloud" style="color:#2E8B57; text-decoration:none;">Deploy on Streamlit Cloud</a>
    </p>
</div>
""", unsafe_allow_html=True)
