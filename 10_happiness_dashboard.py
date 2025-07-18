import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- Continent assignment helper ---
try:
    import pycountry_convert as pc
except ImportError:
    st.error("Please install pycountry-convert: pip install pycountry-convert")
    st.stop()

def country_to_continent(country_name):
    try:
        country_corrections = {
            'United States': 'United States of America',
            'Russia': 'Russian Federation',
            'South Korea': 'Korea, Republic of',
            'North Korea': 'Korea, Democratic People\'s Republic of',
            'Czechia': 'Czech Republic',
            'Vietnam': 'Viet Nam',
            'Iran': 'Iran, Islamic Republic of',
            'Syria': 'Syrian Arab Republic',
            'Laos': 'Lao People\'s Democratic Republic',
            'Moldova': 'Moldova, Republic of',
            'Tanzania': 'Tanzania, United Republic of',
            'Venezuela': 'Venezuela, Bolivarian Republic of',
            'Bolivia': 'Bolivia, Plurinational State of',
            'Brunei': 'Brunei Darussalam',
            'Palestine': 'Palestine, State of',
            'Congo (Brazzaville)': 'Congo',
            'Congo (Kinshasa)': 'Congo, The Democratic Republic of the',
            'Ivory Coast': "Côte d'Ivoire"
        }
        country_name = country_corrections.get(country_name, country_name)
        country_code = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except Exception:
        return None

# --- Load data from disk ---
st.title("🌍 World Happiness Interactive Dashboard")

csv_path = "world_happiness_merged_2005_2024.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    st.error(f"File not found: {csv_path}")
    st.stop()

# --- Add Continent column ---
with st.spinner("Assigning continents..."):
    # Updated to use 'Country name' instead of 'Country'
    df['Continent'] = df['Country name'].apply(country_to_continent)
    df = df.dropna(subset=['Continent'])

# --- Sidebar filters ---
st.sidebar.header("Filters")

continents = ['All'] + sorted(df['Continent'].unique())
selected_continent = st.sidebar.selectbox("Select Continent", continents, index=0)

# Updated to exclude correct column names and use 'Life Ladder' as default
indicator_options = [col for col in df.columns if col not in ['Country name', 'year', 'Continent']]
default_indicator = 'Life Ladder' if 'Life Ladder' in indicator_options else indicator_options[0]
selected_indicator = st.sidebar.selectbox("Select Indicator", indicator_options, index=indicator_options.index(default_indicator))

if selected_continent == 'All':
    filtered_df = df
else:
    filtered_df = df[df['Continent'] == selected_continent]

# --- Choropleth Map ---
st.subheader(f"World Map of {selected_indicator}")

fig_map = px.choropleth(
    filtered_df,
    locations='Country name',  # Updated to use 'Country name'
    locationmode='country names',
    color=selected_indicator,
    hover_name='Country name',  # Updated to use 'Country name'
    color_continuous_scale=[
        "#08306b", "#2171b5", "#6baed6", "#9ecae1", "#e5f5f9",
        "#fcae91", "#fb6a4a", "#cb181d"
    ],
    title=f'World Map of {selected_indicator}'
)

st.plotly_chart(fig_map, use_container_width=True)

# --- Box Plot ---
st.subheader(f"{selected_indicator} Distribution by Continent")

fig_box = px.box(
    filtered_df,
    x='Continent',
    y=selected_indicator,
    color='Continent',
    color_discrete_sequence=px.colors.qualitative.Set2,
    points="all"
)

st.plotly_chart(fig_box, use_container_width=True)

# --- Scatter Plot ---
# Updated to use 'Log GDP per capita' instead of 'GDP_per_Capita'
if 'Log GDP per capita' in df.columns and selected_indicator != 'Log GDP per capita':
    st.subheader(f"GDP per Capita vs. {selected_indicator}")
    
    fig_scatter = px.scatter(
        filtered_df,
        x='Log GDP per capita',  # Updated column name
        y=selected_indicator,
        color='Continent',
        hover_name='Country name',  # Updated to use 'Country name'
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f'Log GDP per Capita vs. {selected_indicator}'
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
