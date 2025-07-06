import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load and clean data
df = pd.read_csv('world_happiness_report.csv')
df.columns = [col.strip() for col in df.columns]
df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)

# Indicators you want to show
radar_indicators = [
    'GDP_per_Capita', 'Social_Support', 'Healthy_Life_Expectancy',
    'Freedom', 'Generosity', 'Corruption_Perception'
]

def find_matching_columns(indicators, df_columns):
    col_map = {}
    for ind in indicators:
        match = [col for col in df_columns
                 if col.lower().replace('_','').replace(' ','') == ind.lower().replace('_','').replace(' ','')]
        col_map[ind] = match[0] if match else None
    return col_map

col_map = find_matching_columns(radar_indicators, df.columns)
final_radar_indicators = [col_map[ind] for ind in radar_indicators if col_map[ind] is not None]

# Streamlit app
st.title("🌍 Country Happiness Profile Dashboard")

country_list = sorted(df['Country'].unique())
selected_country = st.selectbox("Select a Country", country_list)

df_country = df[df['Country'] == selected_country].sort_values('Year')
latest_year = df_country['Year'].max()
latest_data = df_country[df_country['Year'] == latest_year]

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
    theta=radar_indicators[:len(radar_values)],
    fill='toself',
    name=selected_country
))
radar_fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    title=f"{selected_country} - Happiness Indicators (Normalized, {latest_year})"
)

# Line Chart: Happiness Score Over Time
line_fig = px.line(
    df_country,
    x='Year',
    y='Happiness_Score',
    title=f"{selected_country} - Happiness Score Over Time",
    markers=True
)

# Bar Chart: Rank Over Time
if 'Rank' in df.columns:
    df_rank = df_country
else:
    df_rank = df[df['Year'].isin(df_country['Year'])].copy()
    df_rank['Rank'] = df_rank.groupby('Year')['Happiness_Score'].rank(ascending=False, method='min')
    df_rank = df_rank[df_rank['Country'] == selected_country]

bar_fig = px.bar(
    df_rank,
    x='Year',
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
