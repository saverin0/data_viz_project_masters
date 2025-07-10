# 🌍 World Happiness Data Visualization Project

A comprehensive data visualization dashboard exploring the World Happiness Index data from 2005-2024, built as part of a Master's degree project.

## 📊 Project Overview

This project provides interactive visualizations of global happiness data, allowing users to explore relationships between happiness scores and various socioeconomic factors across different countries and continents. The dashboard includes choropleth maps, distribution plots, and correlation analyses.

## 🚀 Features

- **Interactive World Map**: Visualize happiness indicators across countries with color-coded choropleth maps
- **Continental Analysis**: Filter and compare data by continent with box plots showing distributions
- **Correlation Analysis**: Explore relationships between GDP per capita and other happiness indicators
- **Multiple Dashboards**: Two versions available with different feature sets
- **Real-time Filtering**: Dynamic continent and indicator selection

## 📁 Project Structure

```
data_viz_project_masters/
├── 10_happiness_dashboard.py      # Primary Streamlit dashboard
├── 15_dashboard.py               # Extended dashboard version
├── world_happiness_merged_2005_2024.csv  # Dataset (2005-2024)
├── World Happiness Index Report_GH.pdf   # Project report
├── requirements.txt              # Python dependencies
├── .devcontainer/               # Development container configuration
└── LICENSE                      # MIT License
```

## 🛠 Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/saverin0/data_viz_project_masters.git
   cd data_viz_project_masters
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   # Primary dashboard
   streamlit run 10_happiness_dashboard.py
   
   # Extended dashboard
   streamlit run 15_dashboard.py
   ```

### Using Development Container

This project includes a `.devcontainer` configuration for consistent development environments. If you're using VS Code with the Remote-Containers extension:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. The container will automatically set up the environment

## 📋 Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive plotting library
- **pycountry-convert**: Country to continent mapping

## 📈 Dashboard Features

### Primary Dashboard (`10_happiness_dashboard.py`)
- World choropleth map visualization
- Continental distribution analysis
- GDP vs. happiness correlation plots
- Interactive filtering by continent and indicator

### Extended Dashboard (`15_dashboard.py`)
- Additional visualization types
- Enhanced filtering options
- Extended analytical capabilities

## 📊 Data Description

The dataset (`world_happiness_merged_2005_2024.csv`) contains World Happiness Index data spanning from 2005 to 2024, including metrics such as:
- Life Ladder (Happiness Score)
- Log GDP per capita
- Social support
- Healthy life expectancy
- Freedom to make life choices
- Generosity
- Perceptions of corruption

## 📖 Usage

1. **Start the application** using one of the Streamlit commands above
2. **Use the sidebar** to filter data by continent
3. **Select indicators** from the dropdown to explore different metrics
4. **Interact with visualizations** by hovering, zooming, and clicking
5. **Compare continents** using the box plot distributions

## 📚 Academic Context

This project was developed as part of a Master's degree program, focusing on data visualization techniques and statistical analysis of global socioeconomic indicators. The accompanying report (`World Happiness Index Report_GH.pdf`) provides detailed analysis and insights.

## 🤝 Contributing

This is an academic project, but suggestions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**saverin0**
- GitHub: [@saverin0](https://github.com/saverin0)

## 🔗 Links

- [Repository](https://github.com/saverin0/data_viz_project_masters)
- [Issues](https://github.com/saverin0/data_viz_project_masters/issues)

---

*Created as part of a Master's degree data visualization project*
