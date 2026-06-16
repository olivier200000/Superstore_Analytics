# ════════════════════════════════════════════════════════════════════════════
# SUPERSTORE ANALYTICS DASHBOARD
# ════════════════════════════════════════════════════════════════════════════

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Superstore Analytics Dashboard",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# GLOBAL PALETTES
# ──────────────────────────────────────────────────────────────────────────
COLOR_SALES   = "#1d4ed8"   # Blue
COLOR_PROFIT  = "#15803d"   # Green
COLOR_WARN    = "#b45309"   # Amber
COLOR_DANGER  = "#991b1b"   # Red

PALETTE_SET2   = px.colors.qualitative.Set2
SALES_PROFIT_MAP = {"Sales": COLOR_SALES, "Profit": COLOR_PROFIT}

# Reordered Navigation: Team page is first
PAGES = [
    "Meet the Team",
    "Executive Summary",
    "Sales Analysis",
    "Profitability Analysis",
    "Regional Analysis",
    "Risk Center",
    "Ethics & Governance",
    "Recommendations",
    "Dataset Metadata",
]

US_STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC",
}

# ──────────────────────────────────────────────────────────────────────────
# CUSTOM STYLING (Deep Green, Times New Roman, Justified Text)
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Times New Roman', Times, serif !important;
        background-color: #062c15 !important; /* Deep Green Background */
        color: #ffffff !important; /* White text */
    }
    
    [data-testid="stSidebar"], .stSlider, .stMultiSelect {
        font-family: 'Times New Roman', Times, serif !important;
    }

    p, li, span, label {
        text-align: justify;
        font-family: 'Times New Roman', Times, serif !important;
    }
    
    .section-header {
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 1.45rem;
        font-weight: 700;
        color: #ffffff;
        border-left: 6px solid #15803d;
        padding-left: 12px;
        margin: 28px 0 16px 0;
        text-transform: uppercase;
    }
    
    .page-title { 
        font-family: 'Times New Roman', Times, serif !important;
        font-size: 2.2rem; 
        font-weight: 800; 
        color: #ffffff; 
        margin-bottom: 4px; 
    }
    
    .page-subtitle { 
        font-family: 'Times New Roman', Times, serif !important;
        color: #d1d5db; 
        font-size: 1.05rem; 
        margin-bottom: 24px; 
        font-style: italic;
    }
    
    .insight-block { background: #111827; border-left: 5px solid #15803d; border-radius: 8px; padding: 16px; margin-bottom: 12px; border: 1px solid #374151; }
    .glossary-block { background: #111827; border-left: 5px solid #1d4ed8; border-radius: 8px; padding: 16px; margin-bottom: 12px; border: 1px solid #374151; }
    
    .member-card { background: #ffffff; color: #000000; border-radius: 8px; padding: 16px; margin-bottom: 10px; border-left: 5px solid #1d4ed8; }
    .leader-card { background: #f0fdf4; color: #000000; border-radius: 8px; padding: 16px; margin-bottom: 10px; border-left: 5px solid #b45309; }
    
    .alert-tile { border-radius: 8px; padding: 16px; text-align: center; border: 2px solid; background-color: #111827; }
    .alert-tile h2 { margin: 0; font-size: 1.8rem; font-weight: bold; }
    .alert-tile p { margin: 4px 0 0 0; font-size: 0.9rem; font-weight: 600; text-align: center; }

    .meta-card { background: #111827; border: 1px solid #374151; border-left: 5px solid #1d4ed8; border-radius: 8px; padding: 20px; margin-bottom: 14px; }
    .meta-card h4 { color: #60a5fa; margin: 0 0 6px 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; }
    .meta-card p { color: #ffffff; margin: 0; font-size: 1.05rem; }
    .meta-card a { color: #60a5fa; }

    .dataframe { font-family: 'Times New Roman', Times, serif !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# DATA PIPELINE
# ──────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading data...")
def load_data(file_or_path):
    data = pd.read_excel(file_or_path)
    data.columns = [c.strip() for c in data.columns]
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    
    data["Year"] = data["Order Date"].dt.year
    data["Month"] = data["Order Date"].dt.to_period("M").astype(str)
    data["Quarter"] = "Q" + data["Order Date"].dt.quarter.astype(str) + " " + data["Year"].astype(str)
    data["Profit Margin %"] = (data["Profit"] / data["Sales"] * 100).round(2)
    
    if "State" in data.columns:
        data["State Code"] = data["State"].map(US_STATE_ABBR)
    return data

DATA_FILE = "super.xlsx"
if os.path.exists(DATA_FILE):
    df = load_data(DATA_FILE)
else:
    st.sidebar.warning("Please upload your super.xlsx file.")
    uploaded_file = st.sidebar.file_uploader("Upload Superstore dataset (.xlsx)", type=["xlsx"])
    if uploaded_file is None:
        st.title("Superstore Analytics Dashboard")
        st.info("Welcome! Please drop the `super.xlsx` file in the sidebar to start.")
        st.stop()
    df = load_data(uploaded_file)

# ──────────────────────────────────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #111827, #15803d); padding: 20px; border-radius: 12px; margin-bottom: 24px; border: 1px solid #374151;'>
      <h1 style='color: white; margin: 0; font-size: 2.1rem; font-family: "Times New Roman", Times, serif;'>Superstore Analytics Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)

def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def page_title(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def fmt_money(value):
    if abs(value) >= 1_000_000: return f"${value/1_000_000:,.2f}M"
    if abs(value) >= 1_000: return f"${value/1_000:,.1f}K"
    return f"${value:,.0f}"

# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ──────────────────────────────────────────────────────────────────────────
render_header()

st.sidebar.title("Navigation")

if "nav_index" not in st.session_state:
    st.session_state["nav_index"] = 0

page = st.sidebar.radio(
    "pages", 
    PAGES, 
    index=st.session_state["nav_index"],
    key="navigation_radio"
)

st.session_state["nav_index"] = PAGES.index(page)

st.sidebar.markdown("---")

regions    = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
years      = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
profit_range = st.sidebar.slider("Profit Range ($)", float(df["Profit"].min()), float(df["Profit"].max()), (float(df["Profit"].min()), float(df["Profit"].max())))

filtered = df[
    df["Region"].isin(regions) & 
    df["Category"].isin(categories) & 
    df["Year"].isin(years) & 
    df["Profit"].between(profit_range[0], profit_range[1])
]

st.sidebar.metric("Filtered Rows", f"{len(filtered):,}")

if len(filtered) == 0:
    st.error("No data found. Adjust your filters in the sidebar.")
    st.stop()

# ──────────────────────────────────────────────────────────────────────────
# DATA CALCULATIONS
# ──────────────────────────────────────────────────────────────────────────
total_sales   = filtered["Sales"].sum()
total_profit  = filtered["Profit"].sum()
avg_sales     = filtered["Sales"].mean()
total_orders  = filtered["Order ID"].nunique()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

loss_df    = filtered[filtered["Profit"] < 0]
loss_count = len(loss_df)
loss_pct   = (loss_count / len(filtered) * 100) if len(filtered) > 0 else 0

high_disc      = filtered[filtered["Discount"] >= 0.4]
high_disc_loss = len(filtered[(filtered["Discount"] >= 0.4) & (filtered["Profit"] < 0)])
missing        = int(filtered.isnull().sum().sum())
dup_rows       = int(filtered.duplicated().sum())

best_region   = filtered.groupby("Region")["Sales"].sum().idxmax()
best_category = filtered.groupby("Category")["Sales"].sum().idxmax()
worst_sub      = filtered.groupby("Sub-Category")["Profit"].sum().idxmin()

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — MEET THE TEAM
# ════════════════════════════════════════════════════════════════════════════
if page == "Meet the Team":
    page_title("Project Contributors", "The group members who built this dashboard app.")

    st.markdown("""
    <p style='margin-bottom: 20px; font-size: 1.1rem;'>
    Welcome to our project dashboard. We made this app to look at the store's data and find ways to help the business grow and make more money. Below are the names of our group members and their contributions in this project.
    </p>
    """, unsafe_allow_html=True)

    section_header("Our Group Members")
    

    members = [
        ("Dusengimana Olivier", "Group Leader and Streamlit Dashboard Developer", True),
        ("Christian Habineza", "Dataset and Metadata Specialist", False),
        ("Gilbert Niyonkuru", "Data Cleaning and Preparation Specialist", False),
        ("Shadia Uwimbabazi", "Data Visualization Specialist", False),
        ("Dative Akimana", "Data Analyst, Ethics and Insights Specialist", False),
    ]

    for name, role, is_leader in members:
        card_class = "leader-card" if is_leader else "member-card"
        prefix = "Leader | " if is_leader else "Member | "
        st.markdown(f'<div class="{card_class}"><strong>{prefix}{name}</strong><br><small style="color:#4b5563;">{role}</small></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Go to Dashboard Overview", use_container_width=True):
        st.session_state["nav_index"] = 1
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════════════════════
elif page == "Executive Summary":
    page_title("Executive Summary", "A simple summary of how the business is doing right now.")
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Money Made", fmt_money(total_sales))
    c2.metric("Total Profit", fmt_money(total_profit))
    c3.metric("Avg Order Value", fmt_money(avg_sales))
    c4.metric("Total Sales Count", f"{total_orders:,}")
    c5.metric("Profit Margin %", f"{profit_margin:.1f}%")
    c6.metric("Losing Sales Rate", f"{loss_pct:.1f}%")

    section_header("Sales and Profit Over Time")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        monthly = filtered.groupby("Month")[["Sales", "Profit"]].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Sales"], mode="lines+markers", name="Money Made", line=dict(color=COLOR_SALES, width=3)))
        fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Profit"], mode="lines", name="Profit", line=dict(color=COLOR_PROFIT, width=2, dash="dash")))
        fig.update_layout(title="Monthly Trends", xaxis_tickangle=-45, height=330, margin=dict(t=40, b=40, l=10, r=10), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_t2:
        yearly = filtered.groupby("Year")[["Sales", "Profit"]].sum().reset_index()
        fig = px.bar(yearly, x="Year", y=["Sales", "Profit"], barmode="group", title="Yearly Trends", color_discrete_map=SALES_PROFIT_MAP, height=330)
        fig.update_layout(margin=dict(t=40, b=40, l=10, r=10), template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    section_header("Main Findings Summary")
    st.markdown(f"""
    <div class="insight-block">
        <strong>Money Made:</strong> We brought in a total of <strong>{fmt_money(total_sales)}</strong>. Out of that money, our profit is <strong>{fmt_money(total_profit)}</strong>. This means our profit score is <strong>{profit_margin:.1f}%</strong>.
    </div>
    <div class="insight-block">
        <strong>Best Performing Region and Category:</strong> We sell the most items in the <strong>{best_region}</strong> region. Also, our best-selling type of products comes from the <strong>{best_category}</strong> department.
    </div>
    <div class="insight-block">
        <strong>Areas of Concern:</strong> We are facing a big problem selling <strong>{worst_sub}</strong>. Right now, we have <strong>{loss_count:,} different orders</strong> ({loss_pct:.1f}% of all sales) that are losing money instead of making it.
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SALES ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Sales Analysis":
    page_title("Sales Analysis", "Looking closer at where our money comes from.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        sub_data = filtered.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=True)
        fig = px.bar(sub_data, x="Sales", y="Sub-Category", orientation="h", title="Money Made by Item Groups", color="Sales", color_continuous_scale="Blues", height=380)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    with col_c2:
        ship_data = filtered.groupby("Ship Mode")["Sales"].sum().reset_index()
        fig = px.pie(ship_data, values="Sales", names="Ship Mode", title="How We Ship Our Items", color_discrete_sequence=PALETTE_SET2, hole=0.4, height=380)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    section_header("Our Best Products")
    top_n = st.slider("Show Top Products Count:", 1, 15, 10)
    top_products = filtered.groupby("Product Name")["Sales"].sum().nlargest(top_n).reset_index()
    fig = px.bar(top_products, x="Sales", y="Product Name", orientation="h", color="Sales", color_continuous_scale="Teal", height=max(320, top_n * 26))
    fig.update_layout(yaxis=dict(autorange="reversed"), template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PROFITABILITY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Profitability Analysis":
    page_title("Profitability Analysis", "Finding out which items made a lot of money and which ones made losses.")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig = px.box(filtered, x="Category", y="Profit", color="Category", title="Profit Spread by Big Categories", color_discrete_sequence=PALETTE_SET2, height=360)
        fig.add_hline(y=0, line_dash="dash", line_color=COLOR_DANGER)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    with col_d2:
        margin_df = filtered.groupby("Category")["Profit Margin %"].mean().reset_index().sort_values("Profit Margin %", ascending=False)
        fig = px.bar(margin_df, x="Category", y="Profit Margin %", title="Profit Percentage by Department", color="Profit Margin %", color_continuous_scale="RdYlGn", height=360)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    section_header("The 10 Items Losing the Most Money")
    if len(loss_df) > 0:
        top_losses = loss_df[["Product Name", "Category", "Region", "Sales", "Profit", "Discount"]].sort_values("Profit").head(10).reset_index(drop=True)
        st.dataframe(top_losses.style.format({"Sales": "${:,.2f}", "Profit": "${:,.2f}", "Discount": "{:.0%}"}).map(lambda x: "background-color: #5c1d1d; color: white" if x < 0 else "", subset=["Profit"]), use_container_width=True)
    else:
        st.success("Great news! No sales are losing money inside this filter view.")

# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — REGIONAL ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Regional Analysis":
    page_title("Regional Analysis", "Looking at our sales performance map across different places.")

    if "State Code" in filtered.columns:
        metric_choice = st.radio("Choose What to See on the Map:", ["Sales", "Profit"], horizontal=True)
        state_data = filtered.groupby(["State", "State Code"])[["Sales", "Profit"]].sum().reset_index()
        
        fig = px.choropleth(
            state_data, 
            locations="State Code", 
            locationmode="USA-states", 
            color=metric_choice, 
            scope="usa", 
            hover_name="State", 
            color_continuous_scale="Blues" if metric_choice == "Sales" else "RdYlGn", 
            title=f"Map of USA {metric_choice}", 
            height=420
        )
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
        cs1, cs2 = st.columns(2)
        with cs1:
            st.markdown("##### Top 5 States Making the Most Profit")
            st.dataframe(state_data.nlargest(5, "Profit")[["State", "Sales", "Profit"]], use_container_width=True, hide_index=True)
        with cs2:
            st.markdown("##### Top 5 States Losing the Most Money")
            st.dataframe(state_data.nsmallest(5, "Profit")[["State", "Sales", "Profit"]], use_container_width=True, hide_index=True)
    else:
        st.info("No location data found to draw maps.")

# ════════════════════════════════════════════════════════════════════════════
# PAGE 6 — RISK CENTER
# ════════════════════════════════════════════════════════════════════════════
elif page == "Risk Center":
    page_title("Problem Areas", "Looking at how big discounts hurt our total profit.")

    r1, r2, r3, r4 = st.columns(4)
    with r1: st.markdown(f'<div class="alert-tile" style="border-color:{COLOR_DANGER};"><h2 style="color:{COLOR_DANGER};">{loss_count:,}</h2><p style="color:#ffffff;">Losing Sales Lines</p></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="alert-tile" style="border-color:{COLOR_WARN};"><h2 style="color:{COLOR_WARN};">{len(high_disc):,}</h2><p style="color:#ffffff;">Big Discounts Given (≥40%)</p></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="alert-tile" style="border-color:{COLOR_DANGER};"><h2 style="color:{COLOR_DANGER};">{high_disc_loss:,}</h2><p style="color:#ffffff;">Money Lost Due to Discounts</p></div>', unsafe_allow_html=True)
    with r4: st.markdown(f'<div class="alert-tile" style="border-color:#15803d;"><h2 style="color:#15803d;">{missing}</h2><p style="color:#ffffff;">Empty Box Data Errors</p></div>', unsafe_allow_html=True)

    section_header("How Discounts Destroy Profits")
    fig = px.scatter(filtered, x="Discount", y="Profit", color="Category", trendline="ols", title="When Discounts Pass 40%, Profits Drop Below Zero", color_discrete_sequence=PALETTE_SET2, opacity=0.6, height=380)
    fig.add_vline(x=0.4, line_dash="dash", line_color=COLOR_DANGER)
    fig.add_hline(y=0, line_dash="dash", line_color="#ffffff")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <p style='margin-top: 15px;'>
    This chart shows a clear story. When we give a discount that is bigger than 40% (past the red dotted line), almost all those sales drop below zero. This means we are losing money because we are giving too much price cuts, not because the items are expensive to make.
    </p>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 7 — ETHICS & GOVERNANCE
# ════════════════════════════════════════════════════════════════════════════
elif page == "Ethics & Governance":
    page_title("Ethics & Safety Rules", "How we protect customer information and show honest data.")

    section_header("Keeping Customer Information Safe")
    st.markdown("""
    <p style='margin-bottom: 15px;'>
    To respect the law and protect our customers, we keep our database clean and safe. We do not show private things that can leak identity profiles like real customer names, phone digits, or exact home street numbers.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    | Safety Step | What We Did | Why We Did It |
    | :--- | :--- | :--- |
    | **No Names Used** | Removed all personal customer names and postal codes. | Keeps bad people from tracking down our real customers. |
    | **Big Group Maps** | Showed states and regions instead of street locations. | Keeps information general enough to be safe but useful. |
    | **Code Locking** | Locked down data exports with system code keys. | Makes sure downloaded copies do not reveal private facts. |
    """)

    section_header("Honest Data Checks")
    st.markdown(f"""
    * **Clean Data:** The system looked at the rows and found **{missing}** missing boxes and **{dup_rows}** double-written data rows.
    * **No Hiding Bad News:** We do not hide our mistakes. All **{loss_count} sales that lost money** are completely visible on this dashboard so the boss can see the true story.
    """)

    section_header("Word Definitions Made Simple")
    glossary = [
        ("Aggregation Bias (Group Tricking)", "When a big group look good, but small parts inside it are failing.", f"Our '{best_category}' group makes the most overall money, but when you look inside, there are still some single items losing lots of cash."),
        ("Temporal Distortion (Time Mistakes)", "When numbers look weird because one month had more calendar entries than others.", "If one month has more holiday sales rows, it makes other normal months look bad even if they did fine."),
        ("Data Minimization (Keeping It Small)", "Only keeping and showing the data you really need to solve a problem.", "Removing customer home numbers from our app screens while keeping the state names active to build our maps.")
    ]
    for term, definition, example in glossary:
        st.markdown(f'<div class="glossary-block"><strong>{term}</strong><br><small style="color:#d1d5db;">What it means: {definition}</small><br><small style="color:#60a5fa;"><b>Example:</b> {example}</small></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 8 — RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════
elif page == "Recommendations":
    page_title("How to Fix Our Business", "Simple, step-by-step choices to help the store stop losing money.")

    section_header("What the Data Is Telling Us")
    st.markdown(f"""
    * **The Money We Have:** We made a total of **{fmt_money(total_sales)}** in sales. Our profit score is **{profit_margin:.1f}%**.
    * **The Big Hole:** We are losing too much money trying to sell **{worst_sub}**.
    * **The Price Cut Problem:** We had **{high_disc_loss} different sales** where we gave a discount of 40% or more. Every single one of those choices lost us money.
    """)

    section_header("5 Easy Things We Must Do Now")
    st.markdown("""
    <p style='margin-bottom: 15px;'>
    Here is a simple plan to fix our profit problems. We have ranked them from the most urgent to the least urgent:
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    | What to Do | Why We Must Do It | How Urgent Is It? |
    | :--- | :--- | :--- |
    | **Stop giving discounts bigger than 20%** | When we give price cuts of 40% or more, we lose money every single time. | **DO THIS NOW (CRITICAL)** |
    | **Change prices for Tables and Bookcases** | These two items are making the biggest losses in the whole store. | **DO THIS NOW (CRITICAL)** |
    | **Add a computer warning at the cash register** | This will block a sale if the discount is too high before the order goes through. | **DO THIS SOON (HIGH)** |
    | **Spend more marketing money on Technology items** | Technology items are very safe and bring home the biggest profit margins. | **DO THIS SOON (HIGH)** |
    | **Clean up the computer database every 3 months** | This removes double entries and empty text boxes to keep the charts accurate. | **DO THIS LATER (LOW)** |
    """)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to Team Page", use_container_width=True):
        st.session_state["nav_index"] = 0
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# PAGE 9 — DATASET METADATA
# ════════════════════════════════════════════════════════════════════════════
elif page == "Dataset Metadata":
    page_title("Dataset Metadata", "Full information about the data source used in this dashboard.")

    st.markdown("""
    <p style='margin-bottom: 24px; font-size: 1.05rem;'>
    This page gives full details about the dataset we used to build this dashboard. Good data science work always shows where the data came from, who made it, and when it was created. This helps anyone reading our work to check, trust, and repeat what we have done.
    </p>
    """, unsafe_allow_html=True)

    # ── Core identity ──────────────────────────────────────────────────────
    section_header("Dataset Identity")

    m1, m2 = st.columns(2)
    with m1:
        st.markdown("""
        <div class="meta-card">
            <h4>📄 Dataset Name</h4>
            <p>Superstore Dataset — Final</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="meta-card">
            <h4>🗂️ Dataset Type</h4>
            <p>Tabular (structured rows and columns in Excel / CSV format)</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="meta-card">
            <h4>📅 Date Published / Last Updated</h4>
            <p>Last updated approximately <strong>4 years ago</strong> on Kaggle
            (circa 2021 based on the Kaggle upload record).</p>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="meta-card">
            <h4>✍️ Author / Creator</h4>
            <p><strong>Vivek Chowdhury</strong><br>
            <small style="color:#9ca3af;">Kaggle username: <em>vivek468</em><br>
            Contact: reachable via the Kaggle profile page linked below.</small></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="meta-card">
            <h4>🔗 Repository / Dataset Link</h4>
            <p><a href="https://www.kaggle.com/datasets/vivek468/superstore-dataset-final"
               target="_blank">
               kaggle.com/datasets/vivek468/superstore-dataset-final
            </a></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="meta-card">
            <h4>📦 File Used in This Project</h4>
            <p><code>super.xlsx</code> — downloaded from Kaggle and loaded directly
            into this Streamlit dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Dataset description ────────────────────────────────────────────────
    section_header("What Is in the Dataset?")
    st.markdown("""
    <p style='margin-bottom: 14px;'>
    The Superstore dataset contains sales transaction records from a fictional United States retail company.
    It is widely used in data analysis and business intelligence teaching because it is clean, realistic, and rich
    with different types of information. Below is a summary of its main columns:
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    | Column Name | What It Means |
    | :--- | :--- |
    | **Order ID** | A unique code number given to each customer order. |
    | **Order Date / Ship Date** | The date the order was placed and the date it was sent out. |
    | **Ship Mode** | How the package was delivered (Standard, Second Class, First Class, Same Day). |
    | **Customer ID / Name** | A code and name for each customer (names are hidden in our dashboard for privacy). |
    | **Segment** | Type of customer: Consumer, Corporate, or Home Office. |
    | **Country / City / State / Region** | Location information where the sale happened. |
    | **Product ID / Product Name** | A code and full name for each product sold. |
    | **Category / Sub-Category** | The big group (e.g., Technology) and smaller group (e.g., Phones) of the product. |
    | **Sales** | How much money was received from the customer for that item. |
    | **Quantity** | How many units of the item were sold. |
    | **Discount** | The price reduction percentage given to the customer (0 = no discount, 0.5 = 50% off). |
    | **Profit** | The money left over after removing the cost of the item from the selling price. |
    """)

    # ── Dataset stats from loaded data ────────────────────────────────────
    section_header("Dataset Size and Coverage")
    ds1, ds2, ds3, ds4 = st.columns(4)
    ds1.metric("Total Rows (Records)", f"{len(df):,}")
    ds2.metric("Total Columns", f"{len(df.columns)}")
    ds3.metric("Years Covered", f"{df['Year'].min()} – {df['Year'].max()}")
    ds4.metric("Unique Products", f"{df['Product Name'].nunique():,}")

    # ── Related work ──────────────────────────────────────────────────────
    section_header("Other Research That Has Used This Dataset")
    st.markdown("""
    <p style='margin-bottom: 14px;'>
    Because this dataset is very popular on Kaggle, many students and data analysts around the world have used it
    in their own projects. Some well-known types of work done with this dataset include:
    </p>
    <div class="insight-block">
        <strong>Sales and Profit Dashboards:</strong> Many Tableau and Power BI tutorials use this dataset
        as a teaching example to build interactive business dashboards similar to what we have built here.
    </div>
    <div class="insight-block">
        <strong>Machine Learning Projects:</strong> Some researchers have used this dataset to train
        prediction models that try to forecast which sales will be profitable before they happen.
    </div>
    <div class="insight-block">
        <strong>Discount Impact Studies:</strong> Several Kaggle notebooks have specifically studied how
        the discount column in this dataset causes profit losses — the same problem we highlight in our
        Risk Center page.
    </div>
    <p style='margin-top: 14px;'>
    You can browse community notebooks and analyses built on this dataset on the official Kaggle page:
    <a href="https://www.kaggle.com/datasets/vivek468/superstore-dataset-final/code" target="_blank" style="color:#60a5fa;">
    kaggle.com/datasets/vivek468/superstore-dataset-final/code</a>.
    </p>
    """, unsafe_allow_html=True)

    # ── License & ethical use ─────────────────────────────────────────────
    section_header("License and Ethical Use")
    st.markdown("""
    <p>
    This dataset was shared publicly on Kaggle for educational and non-commercial use. We have used it
    strictly for academic learning purposes as part of our university coursework. No real customer names,
    addresses, or personal identifiers have been displayed in this dashboard. All analysis has been performed
    honestly and transparently, with no changes made to the original data values.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to Recommendations", use_container_width=True):
        st.session_state["nav_index"] = PAGES.index("Recommendations")
        st.rerun()