import streamlit as st
import pandas as pd
import datetime as dt
import random as rd

st.set_page_config(page_title="ShopImpact", layout="wide", page_icon="🌿", initial_sidebar_state="collapsed")

if 'purchase_log' not in st.session_state:
    st.session_state.purchase_log = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'total_savings' not in st.session_state:
    st.session_state.total_savings = 0.0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary-green: #10B981;
    --dark-green: #059669;
    --light-green: #A7F3D0;
    --eco-blue: #3B82F6;
    --eco-teal: #06B6D4;
    --eco-yellow: #FBBF24;
    --eco-orange: #F97316;
    --soft-white: #F9FAFB;
    --card-bg: rgba(255, 255, 255, 0.95);
    --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

* {
    font-family: 'Inter', sans-serif;
}

body {
    background: linear-gradient(135deg, #F0F9FF 0%, #F0FFF4 100%);
    background-attachment: fixed;
    margin: 0;
    padding: 0;
}

.main-header {
    text-align: center;
    padding: 2rem 1rem;
    background: linear-gradient(135deg, var(--primary-green), var(--eco-teal));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0;
}

.main-title {
    font-size: 3.8rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    font-family: 'Poppins', sans-serif;
    letter-spacing: -0.5px;
    animation: fadeInDown 0.8s ease-out;
}

.subtitle {
    font-size: 1.4rem;
    color: #4B5563;
    font-weight: 400;
    margin-bottom: 2rem;
    animation: fadeInUp 1s ease-out;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.glass-card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: var(--shadow-medium);
    padding: 2rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.7s;
}

.glass-card:hover::before {
    left: 100%;
}

.card-title {
    color: var(--dark-green);
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
    border-bottom: 3px solid var(--light-green);
    position: relative;
}

.card-title::after {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, var(--primary-green), var(--eco-teal));
    border-radius: 3px;
}

.input-card {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(6, 182, 212, 0.05));
    border: 2px solid rgba(16, 185, 129, 0.2);
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary-green), var(--eco-teal));
    color: white;
    border: none;
    padding: 0.9rem 2rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    margin-top: 1rem;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
}

.stButton > button:active {
    transform: translateY(0);
}

.stButton > button::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -60%;
    width: 20%;
    height: 200%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transform: rotate(30deg);
    transition: left 0.7s;
}

.stButton > button:hover::after {
    left: 120%;
}

.eco-badge {
    display: inline-flex;
    align-items: center;
    background: linear-gradient(135deg, var(--eco-yellow), var(--eco-orange));
    color: white;
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    margin: 0.5rem;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: var(--shadow-soft);
    animation: badgePop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

@keyframes badgePop {
    0% { transform: scale(0.8); opacity: 0; }
    70% { transform: scale(1.1); }
    100% { transform: scale(1); opacity: 1; }
}

.eco-badge::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #FFD700, #FF8C00, #FFD700);
    border-radius: 27px;
    z-index: -1;
    opacity: 0.6;
    animation: badgeGlow 2s infinite;
}

@keyframes badgeGlow {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 0.9; }
}

.impact-metric {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--eco-blue), var(--eco-teal));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    line-height: 1;
    animation: metricPulse 3s infinite;
}

@keyframes metricPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.co2-progress {
    height: 28px;
    background: linear-gradient(90deg, var(--primary-green), var(--eco-teal), var(--eco-blue));
    border-radius: 14px;
    margin: 1.5rem 0;
    overflow: hidden;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    position: relative;
}

.progress-fill {
    height: 100%;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 14px;
    transition: width 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 15px;
    color: white;
    font-weight: 600;
    font-size: 0.9rem;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.tip-card {
    background: linear-gradient(135deg, rgba(224, 247, 250, 0.9), rgba(178, 235, 242, 0.9));
    border-left: 6px solid var(--eco-teal);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    animation: slideInLeft 0.6s ease-out;
}

@keyframes slideInLeft {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.graphic-container {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1));
    border: 3px dashed var(--primary-green);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.graphic-container:hover {
    border-style: solid;
    border-color: var(--eco-teal);
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.15));
}

.eco-tip {
    color: #4B5563;
    font-style: italic;
    font-size: 1.1rem;
    margin-bottom: 1rem;
}

.positive {
    color: var(--primary-green);
    font-weight: 600;
}

.negative {
    color: var(--eco-orange);
    font-weight: 600;
}

.data-table {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow-soft);
    margin: 1rem 0;
}

.data-table th {
    background: linear-gradient(135deg, var(--primary-green), var(--dark-green));
    color: white;
    padding: 1rem;
    font-weight: 600;
}

.data-table td {
    padding: 0.8rem 1rem;
    border-bottom: 1px solid #E5E7EB;
}

.data-table tr:hover {
    background: #F9FAFB;
}

.alternative-card {
    background: linear-gradient(135deg, rgba(232, 245, 233, 0.9), rgba(200, 230, 201, 0.9));
    padding: 1rem;
    border-radius: 12px;
    margin: 0.5rem 0;
    border-left: 4px solid var(--primary-green);
    transition: all 0.3s ease;
}

.alternative-card:hover {
    transform: translateX(5px);
    box-shadow: var(--shadow-soft);
}

.leaf-animation {
    animation: leafFloat 4s ease-in-out infinite;
}

@keyframes leafFloat {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25% { transform: translateY(-10px) rotate(2deg); }
    75% { transform: translateY(5px) rotate(-2deg); }
}

.footprint-animation {
    animation: footprintPulse 3s infinite;
}

@keyframes footprintPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.badge-animation {
    animation: badgeSpin 4s linear infinite;
}

@keyframes badgeSpin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.quote-container {
    background: linear-gradient(135deg, rgba(255, 248, 225, 0.9), rgba(255, 236, 179, 0.9));
    border: 2px solid var(--eco-yellow);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    font-size: 1.3rem;
    font-style: italic;
    color: #78350F;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}

.quote-container::before, .quote-container::after {
    content: '"';
    position: absolute;
    font-size: 4rem;
    color: var(--eco-yellow);
    opacity: 0.2;
}

.quote-container::before {
    top: 10px;
    left: 20px;
}

.quote-container::after {
    bottom: 10px;
    right: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">🌿 ShopImpact</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform Your Shopping Habits into Positive Environmental Action</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass-card input-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">➕ Log Your Purchase</div>', unsafe_allow_html=True)
    
    category = st.selectbox(
        "Select Product Category", 
        ["Clothing", "Electronics", "Food & Groceries", "Home Goods", "Personal Care", "Transportation"]
    )
    
    eco_level = st.select_slider(
        "Eco-Friendliness Level",
        options=["High Impact", "Moderate Impact", "Low Impact", "Eco-Friendly", "Carbon Neutral"],
        value="Moderate Impact"
    )
    
    price = st.number_input("Purchase Price ($)", min_value=0.0, value=50.0, step=5.0, format="%.2f")
    
    brand = st.text_input("Brand / Product Name", placeholder="e.g., Brand X T-Shirt")
    
    col_a, col_b = st.columns(2)
    with col_a:
        quantity = st.number_input("Quantity", min_value=1, value=1)
    with col_b:
        frequency = st.selectbox("Purchase Frequency", ["One-time", "Weekly", "Monthly", "Yearly"])
    
    if st.button("Calculate Environmental Impact", key="calculate_btn"):
        impact_multipliers = {
            "High Impact": 4.2,
            "Moderate Impact": 2.8,
            "Low Impact": 1.5,
            "Eco-Friendly": 0.8,
            "Carbon Neutral": 0.3
        }
        
        multiplier = impact_multipliers.get(eco_level, 2.0)
        co2_impact = round(price * quantity * multiplier, 2)
        
        purchase = {
            "timestamp": dt.datetime.now(),
            "category": category,
            "eco_level": eco_level,
            "brand": brand,
            "price": price,
            "quantity": quantity,
            "frequency": frequency,
            "co2_kg": co2_impact,
            "multiplier": multiplier
        }
        
        st.session_state.purchase_log.append(purchase)
        
        eco_tips = [
            "🌱 Consider bamboo-based products for lower environmental impact",
            "♻️ Look for products with recyclable packaging",
            "🚴 Transport choices greatly affect carbon footprint",
            "💧 Water usage varies significantly between products",
            "🌍 Locally sourced items reduce transportation emissions"
        ]
        
        random_tip = rd.choice(eco_tips)
        
        if multiplier <= 0.8:
            st.balloons()
            st.success(f"✅ Excellent Choice! Only {co2_impact}kg CO₂")
            if "Eco Champion" not in st.session_state.achievements:
                st.session_state.achievements.append("Eco Champion")
            
            st.markdown(f'''
            <div class="graphic-container">
                <div class="leaf-animation">
                    <svg width="120" height="120">
                        <path d="M60,20 Q80,30 80,50 Q80,70 60,80 Q40,70 40,50 Q40,30 60,20" 
                              fill="#10B981" stroke="#059669" stroke-width="2"/>
                        <line x1="60" y1="40" x2="60" y2="10" stroke="#A7F3D0" stroke-width="4"/>
                        <circle cx="65" cy="35" r="3" fill="#FBBF24"/>
                        <circle cx="45" cy="55" r="3" fill="#FBBF24"/>
                        <circle cx="75" cy="65" r="3" fill="#FBBF24"/>
                    </svg>
                </div>
                <p style="margin-top: 1rem; font-weight: 600; color: #059669;">Eco-Friendly Purchase! 🌿</p>
            </div>
            ''', unsafe_allow_html=True)
            
        elif multiplier <= 1.5:
            st.info(f"🌿 Good Choice: {co2_impact}kg CO₂")
            if "Green Shopper" not in st.session_state.achievements:
                st.session_state.achievements.append("Green Shopper")
        else:
            st.warning(f"⚠️ High Impact: {co2_impact}kg CO₂")
            
            st.markdown(f'''
            <div class="graphic-container">
                <div class="footprint-animation">
                    <svg width="120" height="120">
                        <circle cx="60" cy="60" r="25" fill="#F97316" stroke="#EA580C" stroke-width="2"/>
                        <circle cx="80" cy="40" r="12" fill="#F97316" stroke="#EA580C" stroke-width="1.5"/>
                        <circle cx="40" cy="40" r="12" fill="#F97316" stroke="#EA580C" stroke-width="1.5"/>
                        <circle cx="85" cy="70" r="12" fill="#F97316" stroke="#EA580C" stroke-width="1.5"/>
                        <circle cx="35" cy="70" r="12" fill="#F97316" stroke="#EA580C" stroke-width="1.5"/>
                    </svg>
                </div>
                <p style="margin-top: 1rem; font-weight: 600; color: #EA580C;">Consider Eco-Alternatives</p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown(f'<div class="tip-card">{random_tip}</div>', unsafe_allow_html=True)
        
        if multiplier <= 1.0:
            savings = price * 0.2
            st.session_state.total_savings += savings
            st.markdown(f'''
            <div style="background: linear-gradient(135deg, #FEF3C7, #FDE68A); 
                        padding: 1rem; border-radius: 12px; margin: 1rem 0;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.5rem;">💰</span>
                    <div>
                        <div style="font-weight: 600; color: #92400E;">Potential Savings</div>
                        <div style="font-size: 1.2rem; font-weight: 700; color: #92400E;">
                            Save up to ${savings:.2f} with sustainable alternatives
                        </div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🏆 Your Achievements</div>', unsafe_allow_html=True)
    
    if st.session_state.achievements:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        for badge in st.session_state.achievements:
            st.markdown(f'''
            <div class="badge-animation" style="display: inline-block; margin: 10px;">
                <svg width="80" height="80">
                    <circle cx="40" cy="40" r="35" fill="url(#grad{hash(badge)})" 
                            stroke="#FBBF24" stroke-width="3"/>
                    <text x="40" y="45" text-anchor="middle" font-size="24" fill="white">
                        {'🌿' if 'Eco' in badge else '💰' if 'Saver' in badge else '⭐'}
                    </text>
                    <defs>
                        <linearGradient id="grad{hash(badge)}" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#10B981;stop-opacity:1"/>
                            <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:1"/>
                        </linearGradient>
                    </defs>
                </svg>
                <div class="eco-badge">{badge}</div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("Start making sustainable purchases to unlock achievements!")
        st.markdown(f'''
        <div style="text-align: center; opacity: 0.5;">
            <svg width="100" height="100">
                <circle cx="50" cy="50" r="40" fill="#E5E7EB" stroke="#D1D5DB" stroke-width="2"/>
                <text x="50" y="58" text-anchor="middle" font-size="30" fill="#9CA3AF">🏆</text>
            </svg>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📊 Impact Dashboard</div>', unsafe_allow_html=True)
    
    if st.session_state.purchase_log:
        df = pd.DataFrame(st.session_state.purchase_log)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        total_spent = df['price'].sum()
        total_co2 = df['co2_kg'].sum()
        avg_impact = total_co2 / total_spent if total_spent > 0 else 0
        
        eco_purchases = len([p for p in st.session_state.purchase_log if p['multiplier'] <= 1.5])
        
        col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
        with col_metrics1:
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.markdown('<div style="font-weight: 600; color: #6B7280; margin-bottom: 5px;">Total Spent</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="impact-metric">${total_spent:.0f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_metrics2:
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.markdown('<div style="font-weight: 600; color: #6B7280; margin-bottom: 5px;">CO₂ Impact</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="impact-metric">{total_co2:.0f}<span style="font-size: 1rem;">kg</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with col_metrics3:
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.markdown('<div style="font-weight: 600; color: #6B7280; margin-bottom: 5px;">Eco Score</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="impact-metric">{eco_purchases}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        progress_percent = min(total_co2 / 1000 * 100, 100)
        st.markdown(f'''
        <div style="margin: 2rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-weight: 600; color: #059669;">Monthly Carbon Footprint</span>
                <span style="font-weight: 700; color: #059669;">{progress_percent:.1f}%</span>
            </div>
            <div class="co2-progress">
                <div class="progress-fill" style="width:{progress_percent}%">
                    {progress_percent:.0f}%
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        category_data = df.groupby('category')['co2_kg'].sum()
        if not category_data.empty:
            st.markdown('<div style="font-weight: 600; color: #374151; margin: 1.5rem 0 1rem 0;">Impact by Category</div>', unsafe_allow_html=True)
            chart_df = pd.DataFrame({
                'Category': category_data.index,
                'CO₂ Impact (kg)': category_data.values
            })
            st.bar_chart(chart_df.set_index('Category'), color="#10B981", height=250)
        
        st.markdown('<div style="font-weight: 600; color: #374151; margin: 1.5rem 0 1rem 0;">Recent Purchases</div>', unsafe_allow_html=True)
        recent = df.tail(5)[['timestamp', 'category', 'eco_level', 'price', 'co2_kg']].copy()
        recent['timestamp'] = recent['timestamp'].dt.strftime('%m/%d %H:%M')
        
        st.dataframe(
            recent.style.format({'price': '${:.2f}', 'co2_kg': '{:.1f} kg'})
            .apply(lambda x: ['color: #059669' if x['eco_level'] in ['Eco-Friendly', 'Carbon Neutral'] else 'color: #EA580C' for _ in x], axis=1),
            use_container_width=True,
            height=250
        )
    else:
        st.info("Log your first purchase to see your environmental impact dashboard")
        st.markdown('''
        <div style="text-align: center; padding: 3rem 1rem; opacity: 0.5;">
            <svg width="150" height="150">
                <circle cx="75" cy="75" r="60" fill="#F3F4F6" stroke="#E5E7EB" stroke-width="2"/>
                <path d="M75,30 L75,70 M75,80 L75,90" stroke="#9CA3AF" stroke-width="3" stroke-linecap="round"/>
                <path d="M60,45 Q75,30 90,45" stroke="#9CA3AF" stroke-width="3" fill="none"/>
                <text x="75" y="120" text-anchor="middle" font-size="14" fill="#6B7280">
                    Add purchases to begin
                </text>
            </svg>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🌱 Sustainable Alternatives</div>', unsafe_allow_html=True)
    
    categories = ["Clothing", "Electronics", "Food & Groceries", "Home Goods", "Personal Care"]
    selected_category = st.selectbox("Choose Category", categories)
    
    alternatives = {
        "Clothing": [
            {"name": "Organic Cotton T-Shirts", "savings": "40% less water", "icon": "👕"},
            {"name": "Bamboo Fabric Items", "savings": "65% lower CO₂", "icon": "🎋"},
            {"name": "Second-hand Clothing", "savings": "90% footprint reduction", "icon": "🔄"}
        ],
        "Electronics": [
            {"name": "Refurbished Devices", "savings": "70% materials saved", "icon": "🔄"},
            {"name": "Energy Star Rated", "savings": "30% less energy", "icon": "⚡"},
            {"name": "Solar Powered", "savings": "100% renewable", "icon": "☀️"}
        ],
        "Food & Groceries": [
            {"name": "Local Organic Produce", "savings": "60% less transport", "icon": "🥦"},
            {"name": "Plant-based Options", "savings": "50% less emissions", "icon": "🌱"},
            {"name": "Bulk Buying", "savings": "80% less packaging", "icon": "📦"}
        ]
    }
    
    if selected_category in alternatives:
        for alt in alternatives[selected_category]:
            st.markdown(f'''
            <div class="alternative-card">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.5rem;">{alt['icon']}</span>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600; color: #059669;">{alt['name']}</div>
                        <div style="font-size: 0.9rem; color: #6B7280;">{alt['savings']}</div>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    if st.session_state.total_savings > 0:
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, #D1FAE5, #A7F3D0); 
                    padding: 1.2rem; border-radius: 15px; margin-top: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-weight: 700; color: #065F46; font-size: 1.1rem;">Total Potential Savings</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #065F46;">
                        ${st.session_state.total_savings:.2f}
                    </div>
                    <div style="font-size: 0.9rem; color: #047857;">
                        By choosing sustainable alternatives
                    </div>
                </div>
                <span style="font-size: 2.5rem;">💰</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title" style="text-align: center;">🌍 Visual Impact Studio</div>', unsafe_allow_html=True)

graph_col1, graph_col2, graph_col3 = st.columns(3)

with graph_col1:
    st.markdown('<div class="graphic-container">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 600; color: #059669; margin-bottom: 1rem;">Eco Leaf Visualization</div>', unsafe_allow_html=True)
    if st.button("Generate Leaf Animation", key="leaf_btn"):
        st.markdown('''
        <div class="leaf-animation">
            <svg width="150" height="150">
                <path d="M75,25 Q95,35 95,55 Q95,75 75,85 Q55,75 55,55 Q55,35 75,25" 
                      fill="#10B981" stroke="#059669" stroke-width="2.5"/>
                <line x1="75" y1="45" x2="75" y2="15" stroke="#A7F3D0" stroke-width="5" stroke-linecap="round"/>
                <circle cx="80" cy="40" r="4" fill="#FBBF24"/>
                <circle cx="60" cy="60" r="4" fill="#FBBF24"/>
                <circle cx="85" cy="70" r="4" fill="#FBBF24"/>
                <circle cx="65" cy="30" r="4" fill="#FBBF24"/>
            </svg>
        </div>
        <p style="margin-top: 1rem; color: #047857; font-weight: 500;">Each leaf represents an eco-friendly choice</p>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with graph_col2:
    st.markdown('<div class="graphic-container">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 600; color: #EA580C; margin-bottom: 1rem;">Carbon Footprint</div>', unsafe_allow_html=True)
    if st.button("Show Footprint", key="foot_btn"):
        st.markdown('''
        <div class="footprint-animation">
            <svg width="150" height="150">
                <circle cx="75" cy="75" r="35" fill="#F97316" stroke="#EA580C" stroke-width="3"/>
                <circle cx="100" cy="50" r="18" fill="#F97316" stroke="#EA580C" stroke-width="2"/>
                <circle cx="50" cy="50" r="18" fill="#F97316" stroke="#EA580C" stroke-width="2"/>
                <circle cx="105" cy="85" r="18" fill="#F97316" stroke="#EA580C" stroke-width="2"/>
                <circle cx="45" cy="85" r="18" fill="#F97316" stroke="#EA580C" stroke-width="2"/>
                <line x1="80" y1="80" x2="95" y2="95" stroke="#EA580C" stroke-width="2"/>
                <line x1="70" y1="80" x2="55" y2="95" stroke="#EA580C" stroke-width="2"/>
            </svg>
        </div>
        <p style="margin-top: 1rem; color: #9A3412; font-weight: 500;">Visual representation of environmental impact</p>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with graph_col3:
    st.markdown('<div class="graphic-container">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 600; color: #3B82F6; margin-bottom: 1rem;">Achievement Badge</div>', unsafe_allow_html=True)
    badge_type = st.radio("Select Badge Type", ["Eco Warrior", "Carbon Saver", "Green Pioneer"], horizontal=True)
    if st.button("Create Badge", key="badge_btn"):
        st.markdown(f'''
        <div class="badge-animation">
            <svg width="150" height="150">
                <circle cx="75" cy="75" r="50" fill="url(#badgeGrad)" stroke="#3B82F6" stroke-width="4"/>
                <text x="75" y="85" text-anchor="middle" font-size="36" fill="white" font-weight="bold">
                    {'🌿' if badge_type == "Eco Warrior" else '💨' if badge_type == "Carbon Saver" else '⭐'}
                </text>
                <defs>
                    <linearGradient id="badgeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#10B981;stop-opacity:1"/>
                        <stop offset="50%" style="stop-color:#3B82F6;stop-opacity:1"/>
                        <stop offset="100%" style="stop-color:#8B5CF6;stop-opacity:1"/>
                    </linearGradient>
                </defs>
            </svg>
        </div>
        <p style="margin-top: 1rem; color: #1D4ED8; font-weight: 500;">{badge_type} Badge Created!</p>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">💭 Daily Eco Inspiration</div>', unsafe_allow_html=True)

inspirations = [
    "Every sustainable choice you make creates ripples of positive change across our planet.",
    "Your shopping cart is more powerful than you think - it votes for the world you want to live in.",
    "Small conscious choices today build a greener tomorrow for generations to come.",
    "Sustainability isn't about perfection - it's about making better choices, one purchase at a time.",
    "The most revolutionary act you can do is shop with intention and purpose for our planet."
]

current_inspiration = rd.choice(inspirations)
st.markdown(f'<div class="quote-container">{current_inspiration}</div>', unsafe_allow_html=True)

if st.button("✨ Get New Inspiration", key="inspire_btn"):
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.purchase_log:
    total_co2 = sum(p['co2_kg'] for p in st.session_state.purchase_log)
    green_purchases = sum(1 for p in st.session_state.purchase_log if p['multiplier'] <= 1.0)
    
    if total_co2 < 300 and "Carbon Conscious" not in st.session_state.achievements:
        st.session_state.achievements.append("Carbon Conscious")
        st.toast("🏆 Achievement Unlocked: Carbon Conscious!", icon="🎉")
    
    if green_purchases >= 5 and "Green Pioneer" not in st.session_state.achievements:
        st.session_state.achievements.append("Green Pioneer")
        st.toast("🏆 Achievement Unlocked: Green Pioneer!", icon="🌟")

st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; 
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1));
            border-radius: 20px; border: 1px solid rgba(16, 185, 129, 0.2);">
    <p style="color: #374151; font-size: 1rem; margin: 0;">
        <span style="font-weight: 700; color: #059669;">ShopImpact Pro</span> • 
        Designed with ♻️ for a Sustainable Future
    </p>
    <p style="color: #6B7280; font-size: 0.9rem; margin-top: 0.5rem;">
        Track your impact • Make better choices • Build a greener tomorrow
    </p>
</div>
""", unsafe_allow_html=True)

def hash(text):
    return sum(ord(c) for c in text)
