import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from scipy.stats import chi2_contingency, ttest_ind
import warnings
import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Salescope - Walmart Sales Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ff7f0e;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Loads and preprocesses Walmart sales data for analysis"""
    df = pd.read_csv('Walmart_Sales_Data.csv')
    
    df['Date'] = pd.to_datetime(df['Date'])
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time
    df['hour'] = pd.to_datetime(df['Time'].astype(str), format='%H:%M:%S').dt.hour
    df['day_name'] = df['Date'].dt.day_name()
    df['month_name'] = df['Date'].dt.month_name()
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    
    def time_of_day(t):
        if t >= pd.to_datetime('05:00:00').time() and t < pd.to_datetime('12:00:00').time():
            return 'Morning'
        elif t >= pd.to_datetime('12:00:00').time() and t < pd.to_datetime('17:00:00').time():
            return 'Afternoon'
        else:
            return 'Evening'
    
    df['time_of_day'] = df['Time'].apply(time_of_day)
    
    numeric_columns = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross margin percentage', 'gross income', 'Rating']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def generate_pdf_report(df_filtered, date_range, branches, cities):
    """Creates a comprehensive PDF report with analysis results and insights"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=15,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.darkblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6,
        textColor=colors.darkgreen
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4
    )
    
    story = []
    
    story.append(Paragraph("Salescope - Walmart Sales Analytics Report", title_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("Developed and Analysed by: Srikar MK & Alekhya Bulusu", normal_style))
    story.append(Paragraph("LinkedIn: https://www.linkedin.com/in/srikarmk/ | https://www.linkedin.com/in/alekhyabulusu/", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(
        f"This report provides a comprehensive analysis of Walmart sales data covering {len(df_filtered):,} transactions "
        f"with a total revenue of ${df_filtered['Total'].sum():,.2f}. The analysis reveals key patterns in customer behavior, "
        f"product performance, and temporal trends that can inform strategic business decisions.",
        normal_style
    ))
    story.append(Spacer(1, 8))
    

    story.append(Paragraph("Key Performance Indicators", heading_style))
    

    metrics_data = [
        ['Metric', 'Value'],
        ['Total Revenue', f"${df_filtered['Total'].sum():,.2f}"],
        ['Average Transaction Value', f"${df_filtered['Total'].mean():.2f}"],
        ['Total Transactions', f"{len(df_filtered):,}"],
        ['Unique Customers', f"{df_filtered['Invoice ID'].nunique():,}"],
        ['Peak Revenue Day', f"{df_filtered.groupby('day_name')['Total'].sum().idxmax()}"],
        ['Peak Revenue Hour', f"{df_filtered.groupby('hour')['Total'].sum().idxmax()}:00"],
        ['Most Popular Product', f"{df_filtered['Product line'].value_counts().index[0]}"],
        ['Most Common Payment', f"{df_filtered['Payment'].value_counts().index[0]}"]
    ]
    
    metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Customer Demographics", heading_style))
    
    story.append(Paragraph("Gender Distribution", subheading_style))
    gender_counts = df_filtered['Gender'].value_counts()
    for gender, count in gender_counts.items():
        percentage = (count / len(df_filtered)) * 100
        story.append(Paragraph(f"• {gender}: {count:,} customers ({percentage:.1f}%)", normal_style))
    
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Customer Type Distribution", subheading_style))
    customer_type_counts = df_filtered['Customer type'].value_counts()
    for customer_type, count in customer_type_counts.items():
        percentage = (count / len(df_filtered)) * 100
        story.append(Paragraph(f"• {customer_type}: {count:,} customers ({percentage:.1f}%)", normal_style))
    
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Product Performance Analysis", heading_style))
    
    story.append(Paragraph("Revenue by Product Line", subheading_style))
    revenue_by_product = df_filtered.groupby('Product line')['Total'].sum().sort_values(ascending=False)
    total_revenue = revenue_by_product.sum()
    
    for product, revenue in revenue_by_product.items():
        percentage = (revenue / total_revenue) * 100
        story.append(Paragraph(f"• {product}: ${revenue:,.2f} ({percentage:.1f}%)", normal_style))
    
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Statistical Analysis", heading_style))
    
    story.append(Paragraph("Hypothesis Testing Results", subheading_style))
    
    male_spending = df_filtered[df_filtered['Gender'] == 'Male']['Total']
    female_spending = df_filtered[df_filtered['Gender'] == 'Female']['Total']
    
    if len(male_spending) > 0 and len(female_spending) > 0:
        t_stat, p_value = ttest_ind(male_spending, female_spending)
        story.append(Paragraph(f"• Gender Differences: Male ${male_spending.mean():.2f} vs Female ${female_spending.mean():.2f} (p={p_value:.3f})", normal_style))
        if p_value < 0.05:
            story.append(Paragraph(f"  → Significant difference between genders", normal_style))
        else:
            story.append(Paragraph(f"  → No significant difference between genders", normal_style))
    
    member_spending = df_filtered[df_filtered['Customer type'] == 'Member']['Total']
    normal_spending = df_filtered[df_filtered['Customer type'] == 'Normal']['Total']
    
    if len(member_spending) > 0 and len(normal_spending) > 0:
        t_stat, p_value = ttest_ind(member_spending, normal_spending)
        story.append(Paragraph(f"• Customer Type: Member ${member_spending.mean():.2f} vs Normal ${normal_spending.mean():.2f} (p={p_value:.3f})", normal_style))
        if p_value < 0.05:
            story.append(Paragraph(f"  → Significant difference between customer types", normal_style))
        else:
            story.append(Paragraph(f"  → No significant difference between customer types", normal_style))
    
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Temporal Analysis", heading_style))
    
    story.append(Paragraph("Daily Performance", subheading_style))
    daily_revenue = df_filtered.groupby('day_name')['Total'].sum().sort_values(ascending=False)
    for day, revenue in daily_revenue.items():
        percentage = (revenue / daily_revenue.sum()) * 100
        story.append(Paragraph(f"• {day}: ${revenue:,.2f} ({percentage:.1f}%)", normal_style))
    
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Hourly Performance (Top 5)", subheading_style))
    hourly_revenue = df_filtered.groupby('hour')['Total'].sum().sort_values(ascending=False).head()
    for hour, revenue in hourly_revenue.items():
        percentage = (revenue / hourly_revenue.sum()) * 100
        story.append(Paragraph(f"• {hour:02d}:00: ${revenue:,.2f} ({percentage:.1f}%)", normal_style))
    
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Key Business Insights", heading_style))
    
    peak_hour = df_filtered.groupby('hour')['Total'].sum().idxmax()
    top_product = df_filtered['Product line'].value_counts().index[0]
    top_payment = df_filtered['Payment'].value_counts().index[0]
    
    member_spending = df_filtered[df_filtered['Customer type'] == 'Member']['Total'].mean()
    normal_spending = df_filtered[df_filtered['Customer type'] == 'Normal']['Total'].mean()
    
    weekend_spending = df_filtered[df_filtered['is_weekend'] == True]['Total'].mean()
    weekday_spending = df_filtered[df_filtered['is_weekend'] == False]['Total'].mean()
    
    insights = [
        f"• Peak Performance: {df_filtered.groupby('day_name')['Total'].sum().idxmax()} is the most profitable day, with {peak_hour}:00 being the peak hour",
        f"• Product Strategy: {top_product} is the most popular product line - consider expanding inventory",
        f"• Payment Trends: {top_payment} is the preferred payment method - optimize for digital payments",
        f"• Operational Focus: Schedule maximum staffing during {peak_hour}:00-{peak_hour+1}:00 for optimal performance"
    ]
    
    for insight in insights:
        story.append(Paragraph(insight, normal_style))
    

    story.append(Paragraph("---", normal_style))
    story.append(Paragraph(f"Report generated by Salescope - Walmart Sales Analytics Dashboard", normal_style))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
    story.append(Paragraph(f"Data Period: {date_range[0] if len(date_range) == 2 else 'All Data'} to {date_range[1] if len(date_range) == 2 else 'All Data'}", normal_style))
    story.append(Paragraph(f"Branches: {', '.join(branches)}", normal_style))
    story.append(Paragraph(f"Cities: {', '.join(cities)}", normal_style))
    story.append(Paragraph(f"Data analyzed: {len(df_filtered):,} transactions", normal_style))
    story.append(Paragraph(f"Developed and Analysed by: Srikar MK & Alekhya Bulusu", normal_style))
    story.append(Paragraph(f"LinkedIn: https://www.linkedin.com/in/srikarmk/ | https://www.linkedin.com/in/alekhyabulusu/", normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def main():
    """Main dashboard application with interactive filters and analysis"""
    st.markdown('<h1 class="main-header">🛒 Salescope - Walmart Sales Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem;">
        <p><strong>Developed and Analysed by: </strong> 
        <a href="https://www.linkedin.com/in/srikarmk/" target="_blank">Srikar MK</a>  & 
        <a href="https://www.linkedin.com/in/alekhyabulusu/" target="_blank">Alekhya Bulusu</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    
    st.sidebar.title("📊 Dashboard Controls")
    
    st.sidebar.subheader("📅 Date Range")
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    st.sidebar.subheader("🏪 Branch Filter")
    branches = st.sidebar.multiselect(
        "Select branches",
        options=df['Branch'].unique(),
        default=df['Branch'].unique()
    )
    df_filtered = df_filtered[df_filtered['Branch'].isin(branches)]
    
    st.sidebar.subheader("🏙️ City Filter")
    cities = st.sidebar.multiselect(
        "Select cities",
        options=df['City'].unique(),
        default=df['City'].unique()
    )
    df_filtered = df_filtered[df_filtered['City'].isin(cities)]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download PDF Report", type="primary", use_container_width=True):
            with st.spinner("Generating PDF report..."):
                try:
                    pdf_data = generate_pdf_report(df_filtered, date_range, branches, cities)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"walmart_sales_report_{timestamp}.pdf"
                    
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.success("✅ PDF report generated successfully! Click the download button above to save it.")
                    
                except Exception as e:
                    st.error(f"❌ Error generating PDF report: {str(e)}")
                    st.info("💡 Make sure you have the required dependencies installed: `pip install reportlab`")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "📊 Statistical Analysis", "🔍 Customer Insights", "⏰ Time Analysis", "📋 Detailed Reports"])
    
    with tab1:
        st.subheader("💡 Key Business Insights")
        
        peak_hour = df_filtered.groupby('hour')['Total'].sum().idxmax()
        peak_day = df_filtered.groupby('day_name')['Total'].sum().idxmax()
        top_product = df_filtered['Product line'].value_counts().index[0]
        top_payment = df_filtered['Payment'].value_counts().index[0]
        
        member_spending = df_filtered[df_filtered['Customer type'] == 'Member']['Total'].mean()
        normal_spending = df_filtered[df_filtered['Customer type'] == 'Normal']['Total'].mean()
        
        weekend_spending = df_filtered[df_filtered['is_weekend'] == True]['Total'].mean()
        weekday_spending = df_filtered[df_filtered['is_weekend'] == False]['Total'].mean()
        
        insights = [
            f"**Peak Performance**: {peak_day} is the most profitable day, with {peak_hour}:00 being the peak hour",
            f"**Product Strategy**: {top_product} is the most popular product line - consider expanding inventory",
            f"**Payment Trends**: {top_payment} is the preferred payment method - optimize for digital payments",
            f"**Operational Focus**: Schedule maximum staffing during {peak_hour}:00-{peak_hour+1}:00 for optimal performance"
        ]
        
        for insight in insights:
            st.markdown(insight)
        
        st.header("📈 Sales Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = df_filtered['Total'].sum()
            st.metric(
                label="💰 Total Revenue",
                value=f"${total_revenue:,.2f}",
                delta=f"{((total_revenue / df['Total'].sum()) - 1) * 100:.1f}% vs Total"
            )
        
        with col2:
            avg_transaction = df_filtered['Total'].mean()
            st.metric(
                label="💳 Avg Transaction",
                value=f"${avg_transaction:.2f}",
                delta=f"{((avg_transaction / df['Total'].mean()) - 1) * 100:.1f}% vs Total"
            )
        
        with col3:
            total_transactions = len(df_filtered)
            st.metric(
                label="🛒 Total Transactions",
                value=f"{total_transactions:,}",
                delta=f"{((total_transactions / len(df)) - 1) * 100:.1f}% vs Total"
            )
        
        with col4:
            unique_customers = df_filtered['Invoice ID'].nunique()
            st.metric(
                label="👥 Unique Customers",
                value=f"{unique_customers:,}",
                delta=f"{((unique_customers / df['Invoice ID'].nunique()) - 1) * 100:.1f}% vs Total"
            )
        
        st.subheader("📊 Revenue by Product Line")
        revenue_by_product = df_filtered.groupby('Product line')['Total'].sum().sort_values(ascending=False)
        
        fig = px.pie(
            values=revenue_by_product.values,
            names=revenue_by_product.index,
            title="Revenue Distribution by Product Line"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🏆 Top Performing Branches")
        branch_performance = df_filtered.groupby('Branch').agg({
            'Total': ['sum', 'mean', 'count']
        }).round(2)
        branch_performance.columns = ['Total Revenue', 'Avg Transaction', 'Transaction Count']
        branch_performance = branch_performance.sort_values('Total Revenue', ascending=False)
        
        st.dataframe(branch_performance, use_container_width=True)
    
    with tab2:
        st.header("📊 Statistical Analysis")
        
        st.subheader("📈 Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                df_filtered, 
                x='Total', 
                nbins=30,
                title="Distribution of Transaction Values",
                labels={'Total': 'Transaction Value ($)', 'count': 'Frequency'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(
                df_filtered, 
                x='Rating', 
                nbins=20,
                title="Distribution of Customer Ratings",
                labels={'Rating': 'Rating Score', 'count': 'Frequency'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔗 Correlation Analysis")
        numeric_columns = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross margin percentage', 'gross income', 'Rating']
        correlation_matrix = df_filtered[numeric_columns].corr()
        
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix of Numeric Variables",
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🧪 Hypothesis Testing")
        
        st.write("**Gender Differences in Spending:**")
        male_spending = df_filtered[df_filtered['Gender'] == 'Male']['Total']
        female_spending = df_filtered[df_filtered['Gender'] == 'Female']['Total']
        
        if len(male_spending) > 0 and len(female_spending) > 0:
            t_stat, p_value = ttest_ind(male_spending, female_spending)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Male Avg Spending", f"${male_spending.mean():.2f}")
            with col2:
                st.metric("Female Avg Spending", f"${female_spending.mean():.2f}")
            with col3:
                st.metric("P-value", f"{p_value:.4f}")
            
            if p_value < 0.05:
                st.success("✅ Significant difference in spending between genders")
            else:
                st.info("ℹ️ No significant difference in spending between genders")
    
    with tab3:
        st.header("🔍 Customer Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Customer Type Distribution")
            customer_type_counts = df_filtered['Customer type'].value_counts()
            fig = px.pie(
                values=customer_type_counts.values,
                names=customer_type_counts.index,
                title="Customer Type Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🚻 Gender Distribution")
            gender_counts = df_filtered['Gender'].value_counts()
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="Gender Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("💳 Payment Method Analysis")
        payment_analysis = df_filtered.groupby('Payment').agg({
            'Total': ['sum', 'mean', 'count']
        }).round(2)
        payment_analysis.columns = ['Total Revenue', 'Avg Transaction', 'Transaction Count']
        payment_analysis = payment_analysis.sort_values('Total Revenue', ascending=False)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.dataframe(payment_analysis, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=payment_analysis.index,
                y=payment_analysis['Total Revenue'],
                title="Revenue by Payment Method",
                labels={'x': 'Payment Method', 'y': 'Total Revenue ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("💡 Customer Behavior Insights")
        
        gender_product = df_filtered.groupby(['Gender', 'Product line']).size().unstack(fill_value=0)
        
        fig = px.bar(
            gender_product.T,
            title="Product Preferences by Gender",
            labels={'index': 'Product Line', 'value': 'Number of Transactions'}
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("⏰ Time Analysis")
        
        st.subheader("📅 Daily Revenue Trend")
        daily_revenue = df_filtered.groupby('Date')['Total'].sum().reset_index()
        
        fig = px.line(
            daily_revenue,
            x='Date',
            y='Total',
            title="Daily Revenue Trend",
            labels={'Total': 'Revenue ($)', 'Date': 'Date'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🕐 Revenue by Hour")
            hourly_revenue = df_filtered.groupby('hour')['Total'].sum()
            
            fig = px.bar(
                x=hourly_revenue.index,
                y=hourly_revenue.values,
                title="Revenue by Hour of Day",
                labels={'x': 'Hour', 'y': 'Revenue ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Sales by Day of Week")
            daily_sales = df_filtered.groupby('day_name')['Total'].sum()
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_sales = daily_sales.reindex(days_order)
            
            fig = px.bar(
                x=daily_sales.index,
                y=daily_sales.values,
                title="Revenue by Day of Week",
                labels={'x': 'Day of Week', 'y': 'Revenue ($)'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("🔥 Revenue Heatmap: Day vs Hour")
        heatmap_data = df_filtered.pivot_table(
            values='Total', 
            index='day_name', 
            columns='hour', 
            aggfunc='sum'
        ).fillna(0)
        
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(days_order)
        
        fig = px.imshow(
            heatmap_data,
            title="Revenue Heatmap: Day of Week vs Hour",
            labels={'x': 'Hour', 'y': 'Day of Week', 'color': 'Revenue ($)'},
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("📋 Detailed Reports")
        
        st.subheader("📊 Summary Statistics")
        
        numeric_columns = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross margin percentage', 'gross income', 'Rating']
        summary_stats = df_filtered[numeric_columns].describe()
        st.dataframe(summary_stats, use_container_width=True)
        
        st.subheader("🏆 Top 10 Highest Value Transactions")
        top_transactions = df_filtered.nlargest(10, 'Total')[
            ['Invoice ID', 'Date', 'Time', 'Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Total']
        ]
        st.dataframe(top_transactions, use_container_width=True)
        
        # Export data
        st.subheader("📥 Export Data")
        
        if st.button("Download Filtered Data as CSV"):
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"walmart_sales_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Data quality report
        st.subheader("🔍 Data Quality Report")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            missing_data = df_filtered.isnull().sum()
            st.write("**Missing Values:**")
            for col, missing in missing_data.items():
                if missing > 0:
                    st.write(f"- {col}: {missing}")
                else:
                    st.write(f"- {col}: ✅ No missing values")
        
        with col2:
            st.write("**Data Types:**")
            for col, dtype in df_filtered.dtypes.items():
                st.write(f"- {col}: {dtype}")
        
        with col3:
            st.write("**Data Range:**")
            st.write(f"- Date range: {df_filtered['Date'].min()} to {df_filtered['Date'].max()}")
            st.write(f"- Total range: ${df_filtered['Total'].min():.2f} to ${df_filtered['Total'].max():.2f}")
            st.write(f"- Rating range: {df_filtered['Rating'].min():.1f} to {df_filtered['Rating'].max():.1f}")

if __name__ == "__main__":
    main()
