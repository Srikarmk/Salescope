# Walmart Sales Analytics Project

**Developed and Analysed by:** [Srikar MK](https://www.linkedin.com/in/srikarmk/) & [Alekhya Bulusu](https://www.linkedin.com/in/alekhyabulusu/)

**You can visit the deployed website:** [https://walmart-sales-analysis.streamlit.app](https://walmart-sales-analysis.streamlit.app)

This project provides a comprehensive statistical analysis of Walmart sales data with an interactive Streamlit dashboard for visualization and exploration.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Dashboard

```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`


## 📊 Features

### Streamlit Dashboard

- **Interactive Filters**: Date range, branch, and city filters
- **Real-time Metrics**: Key performance indicators with comparisons
- **Visualizations**: Interactive charts and graphs using Plotly
- **Statistical Analysis**: Hypothesis testing and correlation analysis
- **Export Functionality**: Download filtered data as CSV
- **PDF Report Generation**: Comprehensive analysis report in PDF format

### Statistical Analysis Notebook

- **Descriptive Statistics**: Comprehensive data overview
- **Distribution Analysis**: Histograms, box plots, and normality tests
- **Hypothesis Testing**: T-tests, Chi-square tests, and ANOVA
- **Correlation Analysis**: Correlation matrices and relationship analysis
- **Time Series Analysis**: Trend analysis and seasonal patterns
- **Predictive Modeling**: Linear regression and Random Forest models

## 📈 Key Insights

### Business Performance

- **Total Revenue**: $322,966.75 across 1,000 transactions
- **Average Transaction**: $322.97
- **Peak Day**: Saturday (17.4% of weekly revenue)
- **Peak Hour**: 7:00 PM (12.3% of daily revenue)

### Customer Behavior

- **Member customers** spend significantly more than normal customers
- **Weekend customers** have higher transaction values
- **Gender preferences** exist for different product lines
- **Ewallet** is the most popular payment method (34.5%)

### Product Performance

- **Fashion accessories** generate the highest revenue (17.8%)
- **Health and beauty** has the lowest revenue share (15.7%)
- **Electronic accessories** show strong performance (16.8%)

## 🔬 Statistical Analysis Results

### Hypothesis Testing

1. **Gender Differences**: No significant difference in spending between genders (p = 0.22)
2. **Customer Type**: Members spend significantly more than normal customers (p = 0.032)
3. **Weekend vs Weekday**: Weekends generate significantly higher spending (p = 0.004)
4. **Gender-Product Association**: Significant association between gender and product preferences (p = 0.029)
5. **Customer-Payment Association**: Significant association between customer type and payment method (p = 0.013)

### Model Performance

- **Linear Regression R²**: 0.89
- **Random Forest R²**: 0.92
- **Cross-validation accuracy**: 91.3%

## 🛠️ Technical Details

### Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Static plotting
- **Plotly**: Interactive visualizations
- **SciPy**: Statistical functions
- **Scikit-learn**: Machine learning models

### Data Processing

- Date and time parsing
- Categorical variable encoding
- Missing value handling
- Outlier detection and treatment
- Feature engineering for time-based analysis

## 📋 Usage Instructions

### Dashboard Navigation

1. **Overview Tab**: Key metrics and revenue analysis
2. **Statistical Analysis Tab**: Distribution and correlation analysis
3. **Customer Insights Tab**: Demographics and behavior analysis
4. **Time Analysis Tab**: Temporal patterns and trends
5. **Detailed Reports Tab**: Summary statistics and data export

### Filtering Options

- **Date Range**: Select specific time periods
- **Branch**: Filter by store location (A, B, C)
- **City**: Filter by geographic location

### Export Features

- Download filtered data as CSV
- Generate comprehensive PDF reports
- View detailed summary statistics
- Access data quality reports

### PDF Report Features

- **Executive Summary**: High-level overview of key findings
- **Key Performance Indicators**: Comprehensive metrics table
- **Customer Demographics**: Gender and customer type analysis
- **Product Performance**: Revenue analysis by product line
- **Statistical Analysis**: Hypothesis testing results
- **Temporal Analysis**: Daily and hourly performance patterns
- **Business Recommendations**: Actionable insights based on data

## 📊 Sample Visualizations

The dashboard includes:

- Interactive pie charts for revenue distribution
- Bar charts for performance comparisons
- Line charts for time series analysis
- Heatmaps for correlation analysis
- Histograms for distribution analysis

## 🔍 Analysis Methodology

### Statistical Tests

- **Shapiro-Wilk Test**: Normality testing
- **Independent Samples T-test**: Group comparisons
- **Chi-square Test**: Categorical associations
- **Pearson Correlation**: Linear relationships
- **ANOVA**: Multiple group comparisons

### Data Quality

- **Missing Values**: Minimal missing data (< 0.1%)
- **Outliers**: Identified and analyzed
- **Data Types**: Properly formatted and validated
- **Consistency**: Cross-validated across sources

## 🚀 Future Enhancements

### Planned Features

1. **Real-time Data Integration**: Connect to live data sources
2. **Advanced ML Models**: Deep learning and ensemble methods
3. **Customer Segmentation**: RFM analysis and clustering
4. **Predictive Analytics**: Sales forecasting and demand prediction
5. **A/B Testing Framework**: Statistical testing for business experiments

### Technical Improvements

1. **Database Integration**: PostgreSQL/MongoDB connectivity
2. **API Development**: RESTful API for data access
3. **Cloud Deployment**: AWS/Azure deployment options
4. **Performance Optimization**: Caching and query optimization
5. **Security**: Authentication and authorization

## 📞 Connect with us

- **[Srikar MK](https://www.linkedin.com/in/srikarmk/)** - AI Developer and Data Science Student
- **[Alekhya Bulusu](https://www.linkedin.com/in/alekhyabulusu/)** - AI Developer and Data Science Student

**Data Period**: January 1, 2019 - March 30, 2019  
**Total Transactions**: 1,000  
**Analysis Type**: Comprehensive Statistical Analysis with Interactive Dashboard


