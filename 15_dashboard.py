import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load and clean data - updated filename
df = pd.read_csv('world_happiness_merged_2005_2024.csv')
df.columns = [col.strip() for col in df.columns]

# Updated to use 'year' column
df['year'] = df['year'].astype(str).str.extract(r'(\d{4})').astype(int)

# Indicators you want to show - updated to actual column names
radar_indicators = [
    'Log GDP per capita', 'Social support', 'Healthy life expectancy at birth',
    'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'
]

def find_matching_columns(indicators, df_columns):
    col_map = {}
    for ind in indicators:
        # Direct match first, then fuzzy match
        if ind in df_columns:
            col_map[ind] = ind
        else:
            match = [col for col in df_columns
                     if col.lower().replace('_','').replace(' ','') == ind.lower().replace('_','').replace(' ','')]
            col_map[ind] = match[0] if match else None
    return col_map

col_map = find_matching_columns(radar_indicators, df.columns)
final_radar_indicators = [col_map[ind] for ind in radar_indicators if col_map[ind] is not None]

# Streamlit app
st.title("🌍 Country Happiness Profile Dashboard")

# Updated to use 'Country name'
country_list = sorted(df['Country name'].unique())
selected_country = st.selectbox("Select a Country", country_list)

# Updated to use 'Country name' and 'year'
df_country = df[df['Country name'] == selected_country].sort_values('year')
latest_year = df_country['year'].max()
latest_data = df_country[df_country['year'] == latest_year]

# Radar Chart
if not latest_data.empty:
    radar_values_raw = latest_data.iloc[0][final_radar_indicators].fillna(0).tolist()
    max_per_indicator = [df[ind].max() for ind in final_radar_indicators]
    radar_values = [v/m if m else 0 for v, m in zip(radar_values_raw, max_per_indicator)]
else:
    radar_values = [0] * len(final_radar_indicators)

radar_fig = go.Figure()

radar_fig.add_trace(go.Scatterpolar(
    r=radar_values,
    theta=final_radar_indicators,  # Use actual column names for display
    fill='toself',
    name=selected_country
))

radar_fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    title=f"{selected_country} - Happiness Indicators (Normalized, {latest_year})"
)

# Line Chart: Life Ladder Score Over Time - updated to use 'Life Ladder'
line_fig = px.line(
    df_country,
    x='year',
    y='Life Ladder',
    title=f"{selected_country} - Life Ladder Score Over Time",
    markers=True
)

# Bar Chart: Rank Over Time - updated to use 'Life Ladder' and 'year'
if 'Rank' in df.columns:
    df_rank = df_country
else:
    df_rank = df[df['year'].isin(df_country['year'])].copy()
    df_rank['Rank'] = df_rank.groupby('year')['Life Ladder'].rank(ascending=False, method='min')
    df_rank = df_rank[df_rank['Country name'] == selected_country]

bar_fig = px.bar(
    df_rank,
    x='year',
    y='Rank',
    title=f"{selected_country} - Happiness Rank Over Time",
    labels={'Rank': 'Rank (Lower is Better)'},
    text='Rank'
)

bar_fig.update_traces(textposition='outside')
bar_fig.update_yaxes(autorange='reversed')

# Layout: Show all three plots in one row
st.plotly_chart(radar_fig, use_container_width=True)
st.plotly_chart(line_fig, use_container_width=True)
st.plotly_chart(bar_fig, use_container_width=True)
