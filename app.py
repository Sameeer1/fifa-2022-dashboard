import streamlit as st
import pandas as pd
import filters
import charts

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & CSS
# ---------------------------------------------------------
st.set_page_config(page_title="FIFA 2022 Analytics", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    /* Dark Background like Gemini */
    .stApp { background-color: #131314; color: #E8EAED; }
    
    /* Gradient Title Text */
    .gemini-title {
        background: -webkit-linear-gradient(45deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        margin-bottom: 0px;
    }
    
    /* KPI Metric Cards Styling */
    div[data-testid="stMetricValue"] { color: #E8EAED !important; font-size: 2.2rem !important; font-weight: bold;}
    div[data-testid="stMetricLabel"] { color: #9b72cb !important; font-size: 1.1rem !important; font-weight: bold;}
    
    /* Expander Styling */
    .streamlit-expanderHeader { background-color: #1E1F22 !important; color: white !important; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. HEADER
# ---------------------------------------------------------
st.markdown('<p class="gemini-title">Hello, Explorer.</p>', unsafe_allow_html=True)
st.markdown("### Uncover FIFA 2022 Squads and Match Insights")
st.markdown("---")

# ---------------------------------------------------------
# 3. DATA LOADING (Both Datasets)
# ---------------------------------------------------------
@st.cache_data
def load_match_data():
    return filters.load_and_clean_data('data/wcmatches.csv')

@st.cache_data
def load_squads_data():
    return pd.read_csv('data/squads.csv', encoding='latin1')

# Load matches data
try:
    df = load_match_data()
    if 'home_score' in df.columns and 'away_score' in df.columns:
        df['Total_Goals'] = df['home_score'] + df['away_score']
except FileNotFoundError:
    st.error("Match dataset not found. Please ensure 'wcmatches.csv' is in the 'data' folder.")
    st.stop()

# ---------------------------------------------------------
# 4. SQUADS SECTION (from squads.csv)
# ---------------------------------------------------------
st.markdown("#### ✨ Explore Teams & Full Squads")
try:
    squads_df = load_squads_data()
    if 'Team' in squads_df.columns and 'Player' in squads_df.columns:
        teams_list = sorted(squads_df['Team'].unique())
        selected_team = st.selectbox("Select a Team to view their Full Squad:", teams_list)
        
        team_data = squads_df[squads_df['Team'] == selected_team]
        team_players = team_data['Player'].tolist()
        
        with st.expander(f"View Full {selected_team} Squad ({len(team_players)} Players)"):
            st.markdown("---")
            for player in team_players:
                st.write(f"- ⚽ {player}")
            st.markdown("---")
    else:
        st.warning("Column names 'Team' or 'Player' not found in squads.csv.")
except FileNotFoundError:
    st.info("💡 Tip: Add 'squads.csv' to the 'data/' folder to see player lists.")

st.markdown("---")

# ---------------------------------------------------------
# 5. SIDEBAR FILTERS (Applies to Matches Data)
# ---------------------------------------------------------
st.sidebar.header("⚽ Filter Match Data")

if st.sidebar.button("Reset / Clear Filters"):
    st.rerun()

# Text Search
search_query = st.sidebar.text_input("Search Team (e.g., Argentina)")
if search_query and 'home_team' in df.columns:
    df = filters.filter_by_text_search(df, 'home_team', search_query)

# Category Filter
if 'tournament' in df.columns:
    categories = ['All'] + list(df['tournament'].unique())
    selected_cat = st.sidebar.selectbox("Select Tournament/Stage", categories)
    df = filters.filter_by_category(df, 'tournament', selected_cat)

# Multi-Select Filter
if 'home_team' in df.columns:
    teams = list(df['home_team'].unique())
    selected_teams = st.sidebar.multiselect("Select Home Teams", teams)
    df = filters.filter_by_multiselect(df, 'home_team', selected_teams)

# Numerical Range Slider
if 'Total_Goals' in df.columns:
    min_val = int(df['Total_Goals'].min())
    max_val = int(df['Total_Goals'].max())
    selected_range = st.sidebar.slider("Total Goals Range", min_val, max_val, (min_val, max_val))
    df = filters.filter_by_numerical_range(df, 'Total_Goals', selected_range[0], selected_range[1])

# Date Range Filter
if 'date' in df.columns:
    min_date = df['date'].dt.date.min()
    max_date = df['date'].dt.date.max()
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])
    if len(date_range) == 2:
        df = filters.filter_by_date(df, date_range[0], date_range[1])

# ---------------------------------------------------------
# 6. KPI SUMMARY CARDS
# ---------------------------------------------------------
st.markdown("#### 📊 Match Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric("Total Matches", len(df))
if 'Total_Goals' in df.columns:
    kpi2.metric("Total Goals Scored", int(df['Total_Goals'].sum()))
    kpi3.metric("Avg Goals per Match", round(df['Total_Goals'].mean(), 2))

st.markdown("---")

# ---------------------------------------------------------
# 7. DASHBOARD CHARTS
# ---------------------------------------------------------
st.markdown("#### 📈 Visual Insights")
tab1, tab2, tab3 = st.tabs(["Distributions & Counts", "Team Comparisons", "Trends & Correlations"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        if 'home_team' in df.columns:
            st.pyplot(charts.plot_pie_chart(df.head(15), 'home_team', "Top 15 Home Teams Frequency"))
        if 'Total_Goals' in df.columns:
            st.pyplot(charts.plot_histogram(df, 'Total_Goals', "Frequency of Total Goals"))
    with col_b:
        if 'home_team' in df.columns:
            st.pyplot(charts.plot_count_plot(df.head(50), 'home_team', "Match Counts by Team"))
        if 'Total_Goals' in df.columns and 'tournament' in df.columns:
            st.pyplot(charts.plot_violin_plot(df, 'tournament', 'Total_Goals', "Goals Density by Tournament"))

with tab2:
    col_c, col_d = st.columns(2)
    with col_c:
        if 'home_team' in df.columns and 'home_score' in df.columns:
            st.pyplot(charts.plot_bar_chart(df.head(10), 'home_team', 'home_score', "Home Score by Team"))
    with col_d:
        if 'home_score' in df.columns and 'away_score' in df.columns:
            st.pyplot(charts.plot_box_plot(df, 'home_score', 'away_score', "Home vs Away Score Spread"))

with tab3:
    col_e, col_f = st.columns(2)
    with col_e:
        if 'date' in df.columns and 'Total_Goals' in df.columns:
            st.pyplot(charts.plot_line_chart(df, 'date', 'Total_Goals', "Goals Trend Over Time"))
            st.pyplot(charts.plot_area_chart(df, 'date', 'Total_Goals', "Cumulative Goals Area"))
    with col_f:
        if 'home_score' in df.columns and 'away_score' in df.columns:
            st.pyplot(charts.plot_scatter_plot(df, 'home_score', 'away_score', "Home vs Away Goals Correlation"))
        st.pyplot(charts.plot_heatmap(df, "Numeric Features Correlation"))