import streamlit as st
import pandas as pd
import datetime as dt
import random as rd

st.set_page_config(page_title="ShopImpact", layout="wide", page_icon="🌿")

if 'purchase_log' not in st.session_state:
    st.session_state.purchase_log = []

if 'achievements' not in st.session_state:
    st.session_state.achievements = []

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

st.markdown("""
<style>
.shop-title {
    font-size: 3rem;
    color: #2E8B57;
    text-align: center;
    margin: 20px 0;
    font-weight: bold;
}

.shop-subtitle {
    font-size: 1.2rem;
    color: #556B2F;
    text-align: center;
    margin-bottom: 30px;
}

.data-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #E0E0E0;
}

.section-title {
    color: #2E8B57;
    border-bottom: 2px solid #3CB371;
    padding-bottom: 8px;
    margin-bottom: 20px;
    font-size: 1.4rem;
    font-weight: 600;
}

.badge-style {
    background: #FFD700;
    color: #8B4513;
    padding: 8px 16px;
    border-radius: 20px;
    margin: 6px;
    font-weight: 600;
    display: inline-block;
}

.tip-box {
    background: #E0F7FA;
    border-left: 4px solid #0097A7;
    padding: 15px;
    border-radius: 10px;
    margin: 15px 0;
}

.graphic-box {
    border: 2px solid #2E8B57;
    border-radius: 10px;
    padding: 20px;
    background: #FAFFF5;
    text-align: center;
    margin: 10px 0;
}

.co2-meter {
    height: 20px;
    background: #E0E0E0;
    border-radius: 10px;
    margin: 15px 0;
    overflow: hidden;
}

.meter-fill {
    height: 100%;
    background: #2E8B57;
    border-radius: 10px;
}

.alternative-item {
    background: #F1F8E9;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
    border-left: 3px solid #4CAF50;
}

.impact-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: #2E8B57;
}

.stButton > button {
    background: #2E8B57;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="shop-title">🌿 ShopImpact</div>', unsafe_allow_html=True)
st.markdown('<div class="shop-subtitle">Make Conscious Shopping Choices</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Log Purchase</div>', unsafe_allow_html=True)
    
    category = st.selectbox("Product Type", list(product_impact.keys()))
    prod_type = st.selectbox("Production Method", ["fast", "ethical", "vintage", "new", "refurbed", "used", 
                                                 "imported", "local", "organic", "sustain", "upcycled", 
                                                 "chem", "natural", "zerowaste"])
    price = st.number_input("Price ($)", min_value=1.0, value=50.0, step=10.0)
    brand = st.text_input("Brand", "Your Brand")
    
    if st.button("Calculate Impact"):
        impact = 2.5
        
        for cat, types in product_impact.items():
            if prod_type in types:
                impact = types[prod_type]
                break
        
        co2 = round(price * impact, 2)
        
        purchase = {
            "time": dt.datetime.now().strftime("%m/%d %H:%M"),
            "category": category,
            "type": prod_type,
            "brand": brand,
            "price": price,
            "co2": co2,
            "impact": impact
        }
        
        st.session_state.purchase_log.append(purchase)
        
        if impact < 2.0:
            st.success(f"✅ Eco-friendly: {co2}kg CO₂")
            if "Eco Starter" not in st.session_state.achievements:
                st.session_state.achievements.append("Eco Starter")
        else:
            st.warning(f"⚠️ Higher impact: {co2}kg CO₂")
        
        tips = [
            "Bamboo grows faster than trees",
            "Second-hand reduces textile waste",
            "Local food travels fewer miles",
            "Refurbished saves materials",
            "Reusables prevent plastic waste"
        ]
        
        st.markdown(f'<div class="tip-box">💡 {rd.choice(tips)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏆 Achievements</div>', unsafe_allow_html=True)
    
    if st.session_state.achievements:
        for badge in st.session_state.achievements:
            st.markdown(f'<div class="badge-style">✨ {badge}</div>', unsafe_allow_html=True)
    else:
        st.info("Make sustainable purchases to earn badges")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Your Impact</div>', unsafe_allow_html=True)
    
    if st.session_state.purchase_log:
        df = pd.DataFrame(st.session_state.purchase_log)
        
        total_price = df['price'].sum()
        total_co2 = df['co2'].sum()
        efficiency = total_co2 / total_price if total_price > 0 else 0
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Spent", f"${total_price:.0f}")
        with col_b:
            st.metric("CO₂ Impact", f"{total_co2:.0f} kg")
        with col_c:
            st.metric("Efficiency", f"{efficiency:.2f} kg/$")
        
        progress = min(total_co2 / 500, 1.0) * 100
        st.markdown(f'''
        <div style="margin:15px 0;">
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span style="font-weight:600; color:#2E8B57;">Carbon Progress</span>
                <span style="font-weight:600;">{progress:.0f}%</span>
            </div>
            <div class="co2-meter">
                <div class="meter-fill" style="width:{progress}%"></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        category_data = df.groupby('category')['co2'].sum()
        if not category_data.empty:
            chart_df = pd.DataFrame({
                'Category': category_data.index,
                'CO₂ (kg)': category_data.values
            })
            st.bar_chart(chart_df.set_index('Category'), color="#2E8B57", height=200)
        
        st.markdown("**Recent Purchases:**")
        recent = df.tail(5)[['time', 'category', 'brand', 'price', 'co2']]
        st.dataframe(recent.style.format({'price':'${:.1f}', 'co2':'{:.1f} kg'}), height=200)
    else:
        st.info("Log your first purchase to see impact data")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌱 Better Choices</div>', unsafe_allow_html=True)
    
    selected = st.selectbox("Category", list(green_brands.keys()))
    
    if selected in green_brands:
        for brand in green_brands[selected]:
            st.markdown(f'<div class="alternative-item">✅ {brand}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="data-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title" style="text-align:center;">🌍 Visual Impact</div>', unsafe_allow_html=True)

g1, g2, g3 = st.columns(3)

with g1:
    st.markdown('<div class="graphic-box">', unsafe_allow_html=True)
    st.markdown("**Eco Leaf**")
    st.markdown("""
    <svg width="120" height="120">
        <path d="M60,20 Q80,30 80,50 Q80,70 60,80 Q40,70 40,50 Q40,30 60,20" 
              fill="#2E8B57" stroke="#228B22"/>
        <line x1="60" y1="40" x2="60" y2="10" stroke="#8FBC8F" stroke-width="3"/>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="graphic-box">', unsafe_allow_html=True)
    st.markdown("**Footprint**")
    st.markdown("""
    <svg width="120" height="120">
        <circle cx="60" cy="60" r="30" fill="#DEB887" stroke="#A0522D"/>
        <circle cx="90" cy="40" r="15" fill="#DEB887" stroke="#A0522D"/>
        <circle cx="30" cy="40" r="15" fill="#DEB887" stroke="#A0522D"/>
        <circle cx="100" cy="70" r="15" fill="#DEB887" stroke="#A0522D"/>
        <circle cx="20" cy="70" r="15" fill="#DEB887" stroke="#A0522D"/>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g3:
    st.markdown('<div class="graphic-box">', unsafe_allow_html=True)
    st.markdown("**Badge**")
    st.markdown("""
    <svg width="120" height="120">
        <circle cx="60" cy="60" r="40" fill="#FFD700" stroke="#FF8C00"/>
        <text x="60" y="65" text-anchor="middle" font-size="30">⭐</text>
    </svg>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.purchase_log:
    total = sum(p['co2'] for p in st.session_state.purchase_log)
    green = sum(1 for p in st.session_state.purchase_log if p['impact'] < 2.0)
    
    if total < 200 and "Carbon Hero" not in st.session_state.achievements:
        st.session_state.achievements.append("Carbon Hero")
    
    if green >= 3 and "Green Shopper" not in st.session_state.achievements:
        st.session_state.achievements.append("Green Shopper")

st.markdown("""
<div style="text-align:center; margin-top:30px; padding:20px; border-top:1px solid #E0E0E0;">
    <p style="color:#556B2F;">ShopImpact • Conscious Shopping Tool</p>
</div>
""", unsafe_allow_html=True)
