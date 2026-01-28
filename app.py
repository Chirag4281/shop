import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import random as rd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64
from matplotlib.path import Path

st.set_page_config(page_title="ShopImpact", layout="wide", page_icon="🌿")

if 'purchase_log' not in st.session_state:
    st.session_state.purchase_log = []

if 'achievements' not in st.session_state:
    st.session_state.achievements = []

if 'co2_total' not in st.session_state:
    st.session_state.co2_total = 0.0

product_impact = {
    "Clothing": {"fast": 3.8, "ethical": 1.3, "vintage": 0.7},
    "Electronics": {"new": 4.9, "refurbed": 2.4, "used": 1.8},
    "Food": {"imported": 3.2, "local": 1.2, "organic": 0.9},
    "Furniture": {"new": 4.1, "sustain": 2.2, "upcycled": 1.1},
    "Cosmetics": {"chem": 2.7, "natural": 1.4, "zerowaste": 0.8}
}

green_brands = {
    "Clothing": ["Patagonia", "Reformation", "Tentree", "Kotn"],
    "Electronics": ["Fairphone", "Framework", "Teracube"],
    "Food": ["Local Harvest", "Thrive", "Imperfect"],
    "Furniture": ["Sabai", "The Citizenry", "VivaTerra"],
    "Cosmetics": ["Ethique", "Plaine", "Meow Tweet"]
}

badge_data = {
    "Eco Starter": {"need": 1, "color": "#2E8B57"},
    "Green Shopper": {"need": 5, "color": "#3CB371"},
    "Carbon Hero": {"need": 100, "color": "#228B22"},
    "Budget Saver": {"need": 3, "color": "#FFD700"},
    "Planet Friend": {"need": 10, "color": "#1E90FF"}
}

eco_facts = [
    "Bamboo grows 35x faster than trees",
    "Second-hand cuts textile waste by 85%",
    "Local food travels 90% fewer miles",
    "Refurbed saves 80% materials",
    "Reusables prevent 450 plastics yearly"
]

eco_quotes = [
    "Each choice writes our planet's story",
    "Shop like the Earth depends on it",
    "Sustainability is smart economics",
    "Your cart shapes tomorrow's world",
    "Green choices ripple through time"
]

def make_matplotlib_leaf():
    fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
    ax.set_aspect('equal')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    
    angles = np.linspace(0, 2*np.pi, 13)
    radii = np.array([1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 1.0])
    
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    
    leaf = patches.Polygon(np.column_stack([x, y]), closed=True, 
                          facecolor='#2E8B57', edgecolor='#228B22', linewidth=2)
    ax.add_patch(leaf)
    
    ax.plot([0, 0], [-0.3, -1.2], color='#8FBC8F', linewidth=3)
    
    for _ in range(8):
        ang = rd.uniform(0, 2*np.pi)
        rad = rd.uniform(0, 0.8)
        dot_x = rad * np.cos(ang)
        dot_y = rad * np.sin(ang)
        ax.plot(dot_x, dot_y, 'o', color='#FFD700', markersize=4)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def make_matplotlib_footprint():
    fig, ax = plt.subplots(figsize=(3, 3), dpi=100)
    ax.set_aspect('equal')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.axis('off')
    
    center = patches.Circle((0, 0), 0.8, facecolor='#DEB887', edgecolor='#A0522D', linewidth=2)
    ax.add_patch(center)
    
    for i in range(5):
        angle = 2*np.pi*i/5
        toe_x = 1.2 * np.cos(angle)
        toe_y = 1.2 * np.sin(angle)
        toe = patches.Circle((toe_x, toe_y), 0.3, 
                            facecolor='#DEB887', edgecolor='#A0522D', linewidth=2)
        ax.add_patch(toe)
    
    for i in range(5):
        angle = 2*np.pi*i/5 + np.pi/5
        line_x = 0.4 * np.cos(angle)
        line_y = 0.4 * np.sin(angle)
        end_x = 0.8 * np.cos(angle)
        end_y = 0.8 * np.sin(angle)
        ax.plot([line_x, end_x], [line_y, end_y], color='#8B4513', linewidth=3)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def make_matplotlib_badge(badge_type="eco"):
    fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=100)
    ax.set_aspect('equal')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')
    
    colors = {
        "eco": ("#228B22", "#32CD32"),
        "savings": ("#FFD700", "#FFEC8B"),
        "impact": ("#1E90FF", "#87CEFA")
    }
    
    c1, c2 = colors.get(badge_type, ("#228B22", "#32CD32"))
    
    angles = np.linspace(0, 2*np.pi, 9)
    radii = [1.0, 0.7, 1.0, 0.7, 1.0, 0.7, 1.0, 0.7, 1.0]
    
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    
    badge = patches.Polygon(np.column_stack([x, y]), closed=True, 
                           facecolor=c2, edgecolor=c1, linewidth=3)
    ax.add_patch(badge)
    
    star_angles = np.linspace(0, 2*np.pi, 11)
    star_radii = np.array([0.4 if i%2==0 else 0.2 for i in range(11)])
    star_x = star_radii * np.cos(star_angles)
    star_y = star_radii * np.sin(star_angles)
    
    star = patches.Polygon(np.column_stack([star_x, star_y]), closed=True, 
                          facecolor='white', edgecolor=c1, linewidth=2)
    ax.add_patch(star)
    
    ax.text(0, 0, "★", fontsize=24, ha='center', va='center', color=c1)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf

def create_co2_chart(data_dict):
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    
    categories = list(data_dict.keys())
    values = list(data_dict.values())
    colors = ['#2E8B57', '#3CB371', '#66CDAA', '#8FBC8F', '#20B2AA']
    
    bars = ax.bar(categories, values, color=colors, edgecolor='white', linewidth=2)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.0f}', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('CO₂ (kg)', fontweight='bold')
    ax.set_title('Carbon Impact by Category', fontweight='bold', pad=15)
    ax.set_facecolor('#F8FFF8')
    fig.patch.set_facecolor('#F8FFF8')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#F8FFF8')
    plt.close(fig)
    buf.seek(0)
    return buf

st.markdown("""
<style>
.glass-panel {
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(12px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 12px 35px rgba(31, 38, 135, 0.18);
    padding: 28px;
    margin: 18px 0;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.glass-panel:hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 45px rgba(31, 38, 135, 0.25);
}

.eco-title {
    font-size: 3.8rem;
    background: linear-gradient(135deg, #2E8B57 0%, #3CB371 50%, #20B2AA 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-align: center;
    margin: 10px 0;
    font-weight: 800;
    letter-spacing: -0.5px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
}

.eco-subtitle {
    font-size: 1.4rem;
    color: #556B2F;
    text-align: center;
    margin-bottom: 40px;
    font-weight: 300;
    letter-spacing: 0.5px;
}

.badge-item {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, #FFD700 0%, #FFEC8B 100%);
    color: #8B4513;
    padding: 10px 22px;
    border-radius: 50px;
    margin: 10px;
    font-weight: 700;
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.25);
    border: 3px solid rgba(255, 255, 255, 0.5);
    animation: badgeFloat 3s ease-in-out infinite;
    position: relative;
    overflow: hidden;
}

.badge-item:before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
    transform: rotate(45deg);
    animation: shine 3s infinite;
}

@keyframes badgeFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes shine {
    0% { left: -50%; }
    100% { left: 150%; }
}

.impact-number {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(45deg, #FF416C, #FF4B2B);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.08);
    display: inline-block;
    padding: 5px;
}

.green-number {
    background: linear-gradient(45deg, #00b09b, #96c93d);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.tip-box {
    background: linear-gradient(135deg, #E0F7FA 0%, #B2EBF2 100%);
    border-left: 6px solid #0097A7;
    padding: 22px;
    border-radius: 18px;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
    animation: slideIn 0.7s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.tip-box:before {
    content: '💡';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 2.5rem;
    opacity: 0.15;
}

@keyframes slideIn {
    0% { transform: translateX(-30px); opacity: 0; }
    100% { transform: translateX(0); opacity: 1; }
}

.turtle-box {
    border: 3px dashed #2E8B57;
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(135deg, #FAFFF5 0%, #F0FFF0 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 240px;
    transition: all 0.3s ease;
}

.turtle-box:hover {
    border-color: #3CB371;
    box-shadow: 0 10px 25px rgba(46, 139, 87, 0.15);
}

.stButton > button {
    background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
    color: white;
    border: none;
    padding: 14px 32px;
    border-radius: 30px;
    font-weight: 700;
    font-size: 1.1rem;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 8px 25px rgba(46, 139, 87, 0.3);
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 15px 35px rgba(46, 139, 87, 0.4);
}

.stButton > button:after {
    content: '';
    position: absolute;
    top: -50%;
    left: -60%;
    width: 20%;
    height: 200%;
    background: rgba(255,255,255,0.3);
    transform: rotate(30deg);
    transition: all 0.5s;
}

.stButton > button:hover:after {
    left: 120%;
}

.co2-meter {
    height: 26px;
    background: linear-gradient(90deg, #00b09b, #96c93d, #FFD700, #FF8C00, #FF416C);
    border-radius: 13px;
    margin: 20px 0;
    overflow: hidden;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
}

.meter-fill {
    height: 100%;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 13px;
    transition: width 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 15px;
    color: white;
    font-weight: bold;
    font-size: 0.9rem;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.quote-display {
    background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
    border: 3px solid #FFB300;
    border-radius: 20px;
    padding: 30px;
    font-size: 1.8rem;
    text-align: center;
    font-style: italic;
    color: #5D4037;
    margin: 25px 0;
    position: relative;
    animation: quotePulse 4s infinite;
}

@keyframes quotePulse {
    0%, 100% { box-shadow: 0 10px 30px rgba(255, 179, 0, 0.15); }
    50% { box-shadow: 0 15px 40px rgba(255, 179, 0, 0.25); }
}

.quote-display:before, .quote-display:after {
    content: '"';
    font-size: 4rem;
    color: #FFB300;
    opacity: 0.3;
    position: absolute;
}

.quote-display:before {
    top: 10px;
    left: 20px;
}

.quote-display:after {
    bottom: 10px;
    right: 20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="eco-title">🌿 ShopImpact</div>', unsafe_allow_html=True)
st.markdown('<div class="eco-subtitle">Transform Shopping into Climate Action</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#2E8B57; border-bottom:3px solid #3CB371; padding-bottom:10px;">➕ Log Purchase</h2>', unsafe_allow_html=True)
    
    cat_choice = st.selectbox("Category", list(product_impact.keys()))
    prod_type = st.selectbox("Production", ["fast", "ethical", "vintage", "new", "refurbed", "used", 
                                          "imported", "local", "organic", "sustain", "upcycled", 
                                          "chem", "natural", "zerowaste"])
    price_val = st.number_input("Amount ($)", min_value=1.0, value=75.0, step=25.0)
    brand_name = st.text_input("Brand", "Sustainable Choice")
    
    if st.button("Calculate Impact", key="calc_main"):
        impact_val = 2.5
        
        for cat, types in product_impact.items():
            if prod_type in types:
                impact_val = types[prod_type]
                break
        
        co2_val = round(price_val * impact_val, 2)
        
        new_entry = {
            "time": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": cat_choice,
            "type": prod_type,
            "brand": brand_name,
            "price": price_val,
            "co2": co2_val,
            "mult": impact_val
        }
        
        st.session_state.purchase_log.append(new_entry)
        st.session_state.co2_total += co2_val
        
        if impact_val < 2.0:
            st.balloons()
            st.success(f"🌱 Sustainable! {co2_val}kg CO₂")
            if "Eco Starter" not in st.session_state.achievements:
                st.session_state.achievements.append("Eco Starter")
            
            leaf_img = make_matplotlib_leaf()
            st.image(leaf_img, caption="Eco Leaf", use_column_width=True)
        else:
            st.warning(f"⚠️ High Impact: {co2_val}kg CO₂")
            foot_img = make_matplotlib_footprint()
            st.image(foot_img, caption="Carbon Footprint", use_column_width=True)
        
        tip_idx = rd.randint(0, len(eco_facts)-1)
        st.markdown(f'<div class="tip-box">💡 {eco_facts[tip_idx]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#2E8B57; border-bottom:3px solid #3CB371; padding-bottom:10px;">🏆 Achievements</h2>', unsafe_allow_html=True)
    
    if st.session_state.achievements:
        cols_badges = st.columns(2)
        for idx, badge in enumerate(st.session_state.achievements):
            with cols_badges[idx % 2]:
                badge_img = make_matplotlib_badge("eco" if idx%3==0 else "savings" if idx%3==1 else "impact")
                st.image(badge_img, use_column_width=True)
                st.markdown(f'<div class="badge-item">{badge}</div>', unsafe_allow_html=True)
    else:
        st.info("Make sustainable purchases to unlock achievements!")
        sample_badge = make_matplotlib_badge()
        st.image(sample_badge, caption="Sample Badge", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#2E8B57; border-bottom:3px solid #3CB371; padding-bottom:10px;">📊 Impact Dashboard</h2>', unsafe_allow_html=True)
    
    if st.session_state.purchase_log:
        df_log = pd.DataFrame(st.session_state.purchase_log)
        df_log['time'] = pd.to_datetime(df_log['time'])
        
        total_price = df_log['price'].sum()
        total_co2 = df_log['co2'].sum()
        avg_ratio = total_co2 / total_price if total_price > 0 else 0
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown('<p style="text-align:center; margin-bottom:5px;">Total Spent</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="impact-number" style="text-align:center;">${total_price:.0f}</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<p style="text-align:center; margin-bottom:5px;">CO₂ Impact</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="impact-number" style="text-align:center;">{total_co2:.0f}kg</div>', unsafe_allow_html=True)
        with col_c:
            st.markdown('<p style="text-align:center; margin-bottom:5px;">Efficiency</p>', unsafe_allow_html=True)
            st.markdown(f'<div class="green-number" style="text-align:center; font-size:2.5rem;">{avg_ratio:.2f}kg/$</div>', unsafe_allow_html=True)
        
        progress_val = min(total_co2 / 500, 1.0) * 100
        st.markdown(f'<div class="co2-meter"><div class="meter-fill" style="width:{progress_val}%">{progress_val:.0f}%</div></div>', unsafe_allow_html=True)
        
        category_co2 = df_log.groupby('category')['co2'].sum().to_dict()
        if category_co2:
            chart_img = create_co2_chart(category_co2)
            st.image(chart_img, use_container_width=True)
        
        st.markdown("**Recent Purchases:**")
        recent_log = df_log.tail(5)[['time', 'category', 'brand', 'price', 'co2']]
        st.dataframe(recent_log.style.format({'price':'${:.1f}', 'co2':'{:.1f} kg'}))
    else:
        st.info("Start logging purchases to see your environmental impact.")
        
        sample_data = {"Clothing": 85, "Electronics": 120, "Food": 65, "Furniture": 95}
        sample_chart = create_co2_chart(sample_data)
        st.image(sample_chart, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<h2 style="color:#2E8B57; border-bottom:3px solid #3CB371; padding-bottom:10px;">🌍 Green Alternatives</h2>', unsafe_allow_html=True)
    
    alt_choice = st.selectbox("Browse Category", list(green_brands.keys()), key="alt_browse")
    
    if alt_choice in green_brands:
        st.markdown("**Recommended Brands:**")
        for brand in green_brands[alt_choice]:
            col_x, col_y = st.columns([1, 5])
            with col_x:
                st.markdown("🌱")
            with col_y:
                st.markdown(f"**{brand}**")
        
        potential_saving = len(st.session_state.purchase_log) * 2.1
        st.markdown(f'<div style="background:#E8F5E9; padding:18px; border-radius:15px; margin-top:20px; border-left:5px solid #4CAF50;">📈 Potential CO₂ Reduction: **{potential_saving:.1f}kg** with sustainable swaps</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown('<h2 style="color:#2E8B57; border-bottom:3px solid #3CB371; padding-bottom:10px; text-align:center;">🎨 Turtle Graphics Studio</h2>', unsafe_allow_html=True)

graph_col1, graph_col2, graph_col3 = st.columns(3)

with graph_col1:
    st.markdown('<div class="turtle-box">', unsafe_allow_html=True)
    st.markdown("**Eco Leaf**")
    if st.button("Generate Leaf", key="gen_leaf"):
        leaf_art = make_matplotlib_leaf()
        st.image(leaf_art, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with graph_col2:
    st.markdown('<div class="turtle-box">', unsafe_allow_html=True)
    st.markdown("**Carbon Footprint**")
    if st.button("Show Footprint", key="gen_foot"):
        foot_art = make_matplotlib_footprint()
        st.image(foot_art, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with graph_col3:
    st.markdown('<div class="turtle-box">', unsafe_allow_html=True)
    st.markdown("**Achievement Badge**")
    badge_style = st.radio("Style", ["eco", "savings", "impact"], horizontal=True, key="badge_style")
    if st.button("Create Badge", key="gen_badge"):
        badge_art = make_matplotlib_badge(badge_style)
        st.image(badge_art, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
st.markdown('<h2 style="color:#2E8B57; border-bottom:3px solid #3CB371; padding-bottom:10px;">💭 Daily Inspiration</h2>', unsafe_allow_html=True)

current_quote = rd.choice(eco_quotes)
st.markdown(f'<div class="quote-display">{current_quote}</div>', unsafe_allow_html=True)

if st.button("New Inspiration", key="new_inspire"):
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.purchase_log:
    total_carbon = sum(p['co2'] for p in st.session_state.purchase_log)
    green_count = sum(1 for p in st.session_state.purchase_log if p['mult'] < 2.0)
    
    if total_carbon < 200 and "Carbon Hero" not in st.session_state.achievements:
        st.session_state.achievements.append("Carbon Hero")
        st.toast("🏆 New Achievement: Carbon Hero!", icon="🎉")
    
    if green_count >= 3 and "Green Shopper" not in st.session_state.achievements:
        st.session_state.achievements.append("Green Shopper")
        st.toast("🏆 New Achievement: Green Shopper!", icon="🌟")

st.markdown("""
<div style="text-align:center; margin-top:50px; padding:25px; border-top:3px solid #2E8B57; background:rgba(46, 139, 87, 0.05); border-radius:20px;">
    <p style="color:#556B2F; font-size:1rem;">
        ShopImpact v3.0 • Built with Streamlit & Matplotlib • 
        <a href="https://streamlit.io/cloud" style="color:#2E8B57; text-decoration:none; font-weight:bold;">Deploy on Streamlit Cloud</a>
    </p>
</div>
""", unsafe_allow_html=True)
