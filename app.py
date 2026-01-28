import streamlit as st
import pandas as pd
import datetime
import random
import json
import time
from collections import defaultdict

st.set_page_config(page_title="ShopImpact", layout="wide", page_icon="🌍")

if "purchases" not in st.session_state:
    st.session_state.purchases = []

if "eco_tips" not in st.session_state:
    st.session_state.eco_tips = [
        "Did you know bamboo has a lower footprint?",
        "Buying second-hand reduces waste by 80%",
        "Local produce saves transportation emissions",
        "Plant-based products often have lower CO₂ impact",
        "Reusable bags can save hundreds of plastic bags yearly"
    ]

if "badges" not in st.session_state:
    st.session_state.badges = []

if "motivational_quotes" not in st.session_state:
    st.session_state.motivational_quotes = [
        "Every green choice counts!",
        "You're making the planet smile!",
        "Sustainable shopping is smart shopping!",
        "Your choices inspire others!",
        "Small steps lead to big changes!"
    ]

product_multipliers = {
    "Clothing": {"fast_fashion": 3.2, "ethical_brand": 1.2, "second_hand": 0.8},
    "Electronics": {"new": 4.5, "refurbished": 2.1, "used": 1.8},
    "Food": {"imported": 2.8, "local": 1.2, "organic": 1.0},
    "Furniture": {"new_plastic": 3.5, "wood": 2.2, "upcycled": 1.0},
    "Cosmetics": {"chemical": 2.5, "natural": 1.5, "zero_waste": 0.9}
}

greener_alternatives = {
    "Clothing": ["Patagonia", "Thrift stores", "Reformation", "Organic cotton brands"],
    "Electronics": ["Refurbished Apple", "Fairphone", "Energy Star rated"],
    "Food": ["Local farmers market", "Organic brands", "Plant-based options"],
    "Furniture": ["Reclaimed wood", "Vintage stores", "IKEA sustainable line"],
    "Cosmetics": ["Lush", "Ethique", "Package-free shops"]
}

badge_rules = {
    "Eco Saver": {"threshold": 50, "message": "Monthly footprint under 50kg CO₂"},
    "Low Impact Shopper": {"count": 5, "message": "5+ eco-friendly purchases"},
    "Green Warrior": {"streak": 7, "message": "7 consecutive green choices"},
    "Budget Eco": {"saving": 200, "message": "Saved $200+ with green alternatives"},
    "Community Influencer": {"shares": 3, "message": "Shared 3+ tips with friends"}
}

st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 0;
        font-weight: 800;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #556B2F;
        text-align: center;
        margin-top: 0;
        font-weight: 300;
    }
    .card {
        background: linear-gradient(135deg, #F5F5DC, #E8F5E8);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(46, 139, 87, 0.15);
        margin: 15px 0;
        border-left: 6px solid #2E8B57;
    }
    .badge {
        display: inline-block;
        background: linear-gradient(45deg, #FFD700, #FFEC8B);
        color: #8B4513;
        padding: 8px 18px;
        border-radius: 50px;
        margin: 8px;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
        animation: pulse 2s infinite;
    }
    .eco-tip {
        background: #E0F7FA;
        border-left: 5px solid #0097A7;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        font-style: italic;
    }
    .footprint-value {
        font-size: 2.8rem;
        color: #D32F2F;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .positive {
        color: #388E3C;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .stButton>button {
        background: linear-gradient(90deg, #2E8B57, #3CB371);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 7px 20px rgba(46, 139, 87, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🌍 ShopImpact</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform Shopping into Sustainable Action</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 3, 2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Add New Purchase")
    product_type = st.selectbox("Product Type", list(product_multipliers.keys()))
    brand_type = st.selectbox("Brand Type", ["fast_fashion", "ethical_brand", "second_hand", "new", "refurbished", "used", "imported", "local", "organic", "new_plastic", "wood", "upcycled", "chemical", "natural", "zero_waste"])
    price = st.number_input("Price ($)", min_value=0.0, step=10.0, value=50.0)
    brand = st.text_input("Brand Name", "Your Brand")
    
    if st.button("Calculate & Add Purchase"):
        multiplier = 2.0
        for cat, types in product_multipliers.items():
            if brand_type in types:
                multiplier = types[brand_type]
                break
        
        co2_kg = round(price * multiplier, 2)
        purchase = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "product": product_type,
            "brand": brand,
            "brand_type": brand_type,
            "price": price,
            "co2_kg": co2_kg,
            "multiplier": multiplier
        }
        st.session_state.purchases.append(purchase)
        
        if multiplier < 1.5:
            st.balloons()
            st.success(f"✅ Eco-friendly choice! Only {co2_kg}kg CO₂")
            if "Low Impact Shopper" not in st.session_state.badges:
                st.session_state.badges.append("Low Impact Shopper")
        else:
            st.warning(f"⚠️ Higher impact: {co2_kg}kg CO₂")
        
        st.session_state.last_tip = random.choice(st.session_state.eco_tips)
        st.markdown(f'<div class="eco-tip">💡 {st.session_state.last_tip}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏆 Your Badges")
    if st.session_state.badges:
        for badge in st.session_state.badges:
            st.markdown(f'<div class="badge">✨ {badge}</div>', unsafe_allow_html=True)
    else:
        st.info("No badges yet. Make eco-friendly purchases to earn badges!")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Live Impact Dashboard")
    
    if st.session_state.purchases:
        df = pd.DataFrame(st.session_state.purchases)
        df['date'] = pd.to_datetime(df['date'])
        
        total_spent = df['price'].sum()
        total_co2 = df['co2_kg'].sum()
        avg_co2_per_dollar = round(total_co2 / total_spent, 3) if total_spent > 0 else 0
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Total Spent", f"${total_spent:.0f}")
        with col_b:
            st.metric("Total CO₂ Impact", f"{total_co2:.1f} kg")
        with col_c:
            st.metric("Efficiency", f"{avg_co2_per_dollar} kg/$")
        
        monthly = df.groupby(df['date'].dt.to_period('M')).agg({'price':'sum', 'co2_kg':'sum'}).tail(6)
        st.bar_chart(monthly['co2_kg'])
        
        recent = df.tail(5)
        st.dataframe(recent[['date', 'product', 'brand', 'price', 'co2_kg']].style.format({'price':'${:.1f}', 'co2_kg':'{:.1f} kg'}))
    else:
        st.info("No purchases yet. Add your first purchase to see your impact!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌿 Greener Alternatives")
    selected = st.selectbox("Product Category", list(greener_alternatives.keys()))
    st.write("Consider these sustainable options:")
    for alt in greener_alternatives[selected]:
        st.markdown(f"✅ {alt}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💭 Motivational Tips")
    quote = random.choice(st.session_state.motivational_quotes)
    st.markdown(f'<div style="font-size:1.4rem; color:#5D4037; padding:20px; text-align:center; background:#FFF8E1; border-radius:15px;">{quote}</div>', unsafe_allow_html=True)
    
    if st.button("Get New Tip"):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Eco Animation")
    animation_type = st.radio("Choose animation", ["Growing Tree", "CO₂ Reduction", "Happy Earth"])
    
    if animation_type == "Growing Tree":
        st.markdown("""
        <div style="text-align:center;">
            <div style="font-size:4rem; animation: pulse 1.5s infinite;">🌳</div>
            <p>Your purchases are planting virtual trees!</p>
        </div>
        """, unsafe_allow_html=True)
    elif animation_type == "CO₂ Reduction":
        st.markdown("""
        <div style="text-align:center;">
            <div style="font-size:4rem;">📉</div>
            <p>Your footprint is decreasing!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center;">
            <div style="font-size:4rem; animation: pulse 2s infinite;">😊</div>
            <p>The Earth is smiling because of you!</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Settings")
    dark_mode = st.checkbox("Dark Mode (Simulated)")
    if dark_mode:
        st.markdown('<style>body {background-color: #121212; color: white;}</style>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.purchases:
    co2_total = sum(p['co2_kg'] for p in st.session_state.purchases)
    if co2_total < 100 and "Eco Saver" not in st.session_state.badges:
        st.session_state.badges.append("Eco Saver")
        st.sidebar.success("🏆 New Badge Unlocked: Eco Saver!")
    
    eco_count = sum(1 for p in st.session_state.purchases if p['multiplier'] < 1.8)
    if eco_count >= 5 and "Green Warrior" not in st.session_state.badges:
        st.session_state.badges.append("Green Warrior")
        st.sidebar.success("🏆 New Badge Unlocked: Green Warrior!")

st.sidebar.markdown("---")
st.sidebar.info("**ShopImpact** v1.0 | Deploy your own on [Streamlit Cloud](https://streamlit.io/cloud)")
