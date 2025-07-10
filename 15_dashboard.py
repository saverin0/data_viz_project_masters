import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Load and clean data
@st.cache_data
def load_data():
    try:
        # GitHub raw URL for your CSV file
        github_url = "https://raw.githubusercontent.com/saverin0/data_viz_project_masters/dce7ba3c7d58e91b2062b9efd9c0fa5205f729c4/world_happiness_merged_2005_2024.csv"
        
        # Try loading from GitHub first
        try:
            df = pd.read_csv(github_url)
            st.success("Data loaded successfully from GitHub repository")
        except Exception as e:
            st.warning(f"Could not load from GitHub: {str(e)}")
            # Fallback to local file
            possible_paths = [
                'world_happiness_merged_2005_2024.csv',
                './world_happiness_merged_2005_2024.csv',
                'data/world_happiness_merged_2005_2024.csv',
                '../world_happiness_merged_2005_2024.csv'
            ]
            
            df = None
            for path in possible_paths:
                try:
                    df = pd.read_csv(path)
                    st.success(f"Data loaded successfully from local file: {path}")
                    break
                except FileNotFoundError:
                    continue
            
            if df is None:
                st.error("Could not find the CSV file locally either. Please upload your data file using the uploader below.")
                st.stop()
        
        df.columns = [col.strip() for col in df.columns]
        
        # Handle year column more robustly
        if 'year' in df.columns:
            if df['year'].dtype == 'object':
                df['year'] = df['year'].astype(str).str.extract(r'(\d{4})').astype(int)
            else:
                df['year'] = df['year'].astype(int)
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

# File uploader as backup
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload CSV file (backup option)", type=['csv'])

if uploaded_file is not None:
    @st.cache_data
    def load_uploaded_data(uploaded_file):
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip() for col in df.columns]
        
        if 'year' in df.columns:
            if df['year'].dtype == 'object':
                df['year'] = df['year'].astype(str).str.extract(r'(\d{4})').astype(int)
            else:
                df['year'] = df['year'].astype(int)
        
        return df
    
    df = load_uploaded_data(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
else:
    df = load_data()

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
st.markdown("*Explore individual country happiness trends and indicators over time*")

# Sidebar for additional options
st.sidebar.header("Options")
show_comparison = st.sidebar.checkbox("Compare with another country", value=False)

# Updated to use 'Country name'
country_list = sorted(df['Country name'].unique())
selected_country = st.selectbox("Select a Country", country_list)

# Comparison country selection
if show_comparison:
    comparison_country = st.selectbox(
        "Select a country to compare", 
        [c for c in country_list if c != selected_country]
    )

# Updated to use 'Country name' and 'year'
df_country = df[df['Country name'] == selected_country].sort_values('year')

if not df_country.empty:
    latest_year = df_country['year'].max()
    latest_data = df_country[df_country['year'] == latest_year]
    
    # Display basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Latest Year", latest_year)
    with col2:
        if not latest_data.empty:
            latest_score = latest_data['Life Ladder'].iloc[0]
            st.metric("Latest Life Ladder Score", f"{latest_score:.2f}")
    with col3:
        years_available = len(df_country)
        st.metric("Years of Data", years_available)
    
    # Radar Chart
    if not latest_data.empty:
        radar_values_raw = latest_data.iloc[0][final_radar_indicators].fillna(0).tolist()
        max_per_indicator = [df[ind].max() for ind in final_radar_indicators]
        radar_values = [v/m if m else 0 for v, m in zip(radar_values_raw, max_per_indicator)]
    else:
        radar_values = [0] * len(final_radar_indicators)
    
    radar_fig = go.Figure()
    
    # Add main country
    radar_fig.add_trace(go.Scatterpolar(
        r=radar_values,
        theta=final_radar_indicators,
        fill='toself',
        name=selected_country,
        line_color='#1f77b4'
    ))
    
    # Add comparison country if selected
    if show_comparison:
        df_comparison = df[df['Country name'] == comparison_country].sort_values('year')
        if not df_comparison.empty:
            latest_comparison = df_comparison[df_comparison['year'] == latest_year]
            if not latest_comparison.empty:
                comp_values_raw = latest_comparison.iloc[0][final_radar_indicators].fillna(0).tolist()
                comp_values = [v/m if m else 0 for v, m in zip(comp_values_raw, max_per_indicator)]
                
                radar_fig.add_trace(go.Scatterpolar(
                    r=comp_values,
                    theta=final_radar_indicators,
                    fill='toself',
                    name=comparison_country,
                    line_color='#ff7f0e'
                ))
    
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        title=f"Happiness Indicators Comparison (Normalized, {latest_year})",
        height=500
    )
    
    # Line Chart: Life Ladder Score Over Time
    line_fig = px.line(
        df_country,
        x='year',
        y='Life Ladder',
        title=f"{selected_country} - Life Ladder Score Over Time",
        markers=True,
        color_discrete_sequence=['#1f77b4']
    )
    
    # Add comparison country to line chart
    if show_comparison:
        df_comparison = df[df['Country name'] == comparison_country].sort_values('year')
        if not df_comparison.empty:
            line_fig.add_scatter(
                x=df_comparison['year'],
                y=df_comparison['Life Ladder'],
                mode='lines+markers',
                name=comparison_country,
                line=dict(color='#ff7f0e')
            )
    
    line_fig.update_layout(height=400)
    
    # Bar Chart: Rank Over Time
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
        text='Rank',
        color_discrete_sequence=['#2ca02c']
    )
    
    bar_fig.update_traces(textposition='outside')
    bar_fig.update_yaxes(autorange='reversed')
    bar_fig.update_layout(height=400)
    
    # Layout: Show all three plots
    st.plotly_chart(radar_fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(line_fig, use_container_width=True)
    with col2:
        st.plotly_chart(bar_fig, use_container_width=True)
    
    # Data table
    if st.checkbox("Show raw data"):
        st.subheader(f"Raw data for {selected_country}")
        st.dataframe(df_country[['year'] + final_radar_indicators + ['Life Ladder']])

else:
    st.warning(f"No data available for {selected_country}")
