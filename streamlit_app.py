#!/usr/bin/env python3
"""
Telegram Analysis Dashboard - Cloud Deployment Version
Interactive visualization dashboard for DMCA Thematic Coding analysis results

Author: Chaos
Version: 1.0 (Cloud)
Date: August 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import numpy as np
from datetime import datetime, timedelta
import re
import base64
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="Telegram Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .category-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
        color: #ff7f0e;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .upload-section {
        border: 2px dashed #1f77b4;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class TelegramAnalysisDashboard:
    def __init__(self):
        self.df = None
        self.summary_data = None
        
    def load_data_from_files(self, csv_file, json_file):
        """Load analysis data from uploaded files"""
        try:
            # Read CSV
            csv_content = csv_file.getvalue().decode('utf-8')
            self.df = pd.read_csv(StringIO(csv_content))
            
            # Read JSON
            json_content = json_file.getvalue().decode('utf-8')
            self.summary_data = json.loads(json_content)
            
            return True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return False
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Create sample data structure for demo
        sample_summary = {
            "analysis_summary": {
                "total_messages_analyzed": 12000,
                "relevant_messages_found": 1315,
                "relevance_rate": 10.96
            },
            "category_distribution": {
                "LGBTQ+ Hate Speech & Anti-Rights Rhetoric": 1245,
                "Masculinity & Gender Backlash": 35,
                "Digital Disinformation & Anti-Gender Narratives": 30,
                "SRHR & Moral Panic": 5
            },
            "subcategory_distribution": {
                "3.religious_opposition": 1280,
                "2.emasculation": 35,
                "1.cultural_authenticity": 30,
                "4.traditional_family": 25
            },
            "intensity_distribution": {
                "1": 1312,
                "2": 3
            },
            "engagement_analysis": {
                "viral_messages": 1129,
                "average_views": 8547,
                "average_forwards": 2.1,
                "max_views": 89000
            },
            "top_linguistic_markers": {
                "sin": 977,
                "immoral": 156,
                "abomination": 89,
                "against God": 67,
                "imported": 45,
                "our culture": 34,
                "beta male": 23,
                "emasculation": 12
            },
            "content_with_media": 700,
            "media_distribution": {
                "photo": 450,
                "document": 250
            }
        }
        
        # Create sample DataFrame
        sample_data = []
        for i in range(1315):
            sample_data.append({
                'Message_ID': f'msg_{i+1}',
                'Text_Preview': f'Sample message content {i+1}...',
                'Categories': 'LGBTQ+ Hate Speech & Anti-Rights Rhetoric',
                'Subcategories': '3.religious_opposition',
                'Intensity_Score': 1,
                'Views': np.random.randint(100, 50000),
                'Forwards': np.random.randint(0, 10),
                'Date': pd.date_range('2024-01-01', periods=1315)[i % 365]
            })
        
        self.df = pd.DataFrame(sample_data)
        self.summary_data = sample_summary
        return True
    
    def create_overview_metrics(self):
        """Create overview metrics section"""
        st.markdown('<div class="main-header">📊 Telegram Analysis Dashboard</div>', unsafe_allow_html=True)
        st.markdown('<div class="category-header">Executive Summary</div>', unsafe_allow_html=True)
        
        if self.summary_data:
            summary = self.summary_data['analysis_summary']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Messages Analyzed",
                    f"{summary['total_messages_analyzed']:,}",
                    help="Total number of messages processed"
                )
            
            with col2:
                st.metric(
                    "Relevant Messages Found",
                    f"{summary['relevant_messages_found']:,}",
                    help="Messages containing anti-gender narratives"
                )
            
            with col3:
                st.metric(
                    "Relevance Rate",
                    f"{summary['relevance_rate']:.2f}%",
                    help="Percentage of messages with relevant content"
                )
            
            with col4:
                engagement = self.summary_data.get('engagement_analysis', {})
                st.metric(
                    "Viral Messages",
                    f"{engagement.get('viral_messages', 0):,}",
                    help="Messages that were forwarded"
                )

    def create_category_distribution(self):
        """Create category distribution visualization"""
        st.markdown('<div class="category-header">📈 Content Category Analysis</div>', unsafe_allow_html=True)
        
        if self.summary_data and 'category_distribution' in self.summary_data:
            categories = self.summary_data['category_distribution']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart for category distribution
                fig_pie = px.pie(
                    values=list(categories.values()),
                    names=list(categories.keys()),
                    title="Distribution of Anti-Gender Content Categories",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart for category counts
                fig_bar = px.bar(
                    x=list(categories.keys()),
                    y=list(categories.values()),
                    title="Message Count by Category",
                    labels={'x': 'Category', 'y': 'Number of Messages'},
                    color=list(categories.values()),
                    color_continuous_scale='viridis'
                )
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)

    def create_engagement_analysis(self):
        """Create engagement and viral spread analysis"""
        st.markdown('<div class="category-header">🚀 Engagement & Viral Spread Analysis</div>', unsafe_allow_html=True)
        
        if self.df is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                # Views distribution
                fig = px.histogram(
                    self.df,
                    x='Views',
                    nbins=30,
                    title="Distribution of Message Views",
                    labels={'x': 'Views', 'y': 'Number of Messages'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Forwards vs Views scatter
                fig = px.scatter(
                    self.df,
                    x='Views',
                    y='Forwards',
                    color='Intensity_Score',
                    title="Views vs Forwards Relationship",
                    labels={'x': 'Views', 'y': 'Forwards'},
                    hover_data=['Categories']
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Engagement metrics
        if self.summary_data and 'engagement_analysis' in self.summary_data:
            engagement = self.summary_data['engagement_analysis']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Average Views",
                    f"{engagement.get('average_views', 0):,.0f}",
                    help="Average views per relevant message"
                )
            
            with col2:
                st.metric(
                    "Average Forwards",
                    f"{engagement.get('average_forwards', 0):.2f}",
                    help="Average forwards per relevant message"
                )
            
            with col3:
                st.metric(
                    "Max Views",
                    f"{engagement.get('max_views', 0):,}",
                    help="Highest single message view count"
                )

    def create_research_insights(self):
        """Create research insights and recommendations"""
        st.markdown('<div class="category-header">🧠 Research Insights & Recommendations</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Key Research Findings")
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("""
            **1. Religious Opposition Dominance**
            - 97% of coded content uses religious framing
            - "Sin" appears 977 times as primary marker
            - Leverages established authority structures
            
            **2. Sophisticated Messaging Strategy**  
            - 99.9% content at Level 1 intensity (subtle)
            - Designed to evade content moderation
            - High viral potential (85.9% forwarded)
            
            **3. Coordinated Campaign Evidence**
            - "Masculinity Saturday" recurring pattern
            - 53% multimedia content strategy
            - Targeted male demographic engagement
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Actionable Recommendations")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("""
            **Immediate Actions:**
            - Implement Level 1 intensity detection systems
            - Engage progressive faith leaders for counter-messaging
            - Develop compelling visual counter-narratives
            
            **Medium-Term Strategies:**
            - Platform algorithm transparency advocacy
            - Longitudinal content evolution tracking
            - Cross-platform analysis expansion
            
            **Long-Term Goals:**
            - Address underlying socioeconomic factors
            - Critical media literacy education integration
            - Evidence-based platform regulation development
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    def show_upload_interface(self):
        """Show file upload interface"""
        st.markdown('<div class="main-header">📊 Telegram Analysis Dashboard</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("### 📂 Upload Your Analysis Results")
        st.markdown("Upload your CSV and JSON analysis files to explore your data")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_file = st.file_uploader(
                "Upload CSV Results",
                type=['csv'],
                help="Upload your coded_messages_detailed.csv file"
            )
        
        with col2:
            json_file = st.file_uploader(
                "Upload JSON Summary",
                type=['json'],
                help="Upload your analysis_summary.json file"
            )
        
        if csv_file and json_file:
            if st.button("Load Analysis Data"):
                with st.spinner("Loading your analysis results..."):
                    if self.load_data_from_files(csv_file, json_file):
                        st.success("✅ Analysis data loaded successfully!")
                        st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("### 🔬 Demo Mode")
        st.markdown("Want to see how the dashboard works? Try the demo with sample data:")
        
        if st.button("Load Demo Data"):
            with st.spinner("Loading demo data..."):
                if self.load_sample_data():
                    st.success("✅ Demo data loaded! Explore the analysis features.")
                    st.experimental_rerun()

    def run_dashboard(self):
        """Main dashboard runner"""
        st.sidebar.title("📊 Navigation")
        
        # Check if data is loaded
        if self.df is None or self.summary_data is None:
            self.show_upload_interface()
            return
        
        # Show data info in sidebar
        st.sidebar.success("✅ Analysis data loaded")
        if self.summary_data:
            total_messages = self.summary_data['analysis_summary']['total_messages_analyzed']
            relevant_messages = self.summary_data['analysis_summary']['relevant_messages_found']
            st.sidebar.info(f"📊 {total_messages:,} total messages\n🎯 {relevant_messages:,} relevant messages")
        
        # Navigation
        pages = [
            "📈 Overview",
            "📊 Categories",
            "🚀 Engagement",
            "🧠 Insights"
        ]
        
        selected_page = st.sidebar.radio("Select Analysis View", pages)
        
        # Render selected page
        if selected_page == "📈 Overview":
            self.create_overview_metrics()
        elif selected_page == "📊 Categories":
            self.create_category_distribution()
        elif selected_page == "🚀 Engagement":
            self.create_engagement_analysis()
        elif selected_page == "🧠 Insights":
            self.create_research_insights()
        
        # Sidebar info
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔄 Reset")
        if st.sidebar.button("Upload New Data"):
            st.session_state.clear()
            st.experimental_rerun()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### About")
        st.sidebar.info("""
        This dashboard visualizes results from the DMCA Thematic Coding Guide analysis 
        of anti-gender narratives in Telegram data.
        
        **Framework:** DMCA v1.0  
        **Analyst:** Chaos  
        **Date:** August 2025
        """)

# Main execution
if __name__ == "__main__":
    dashboard = TelegramAnalysisDashboard()
    dashboard.run_dashboard()
