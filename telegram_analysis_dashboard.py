#!/usr/bin/env python3
"""
Telegram Analysis Dashboard
Interactive visualization dashboard for DMCA Thematic Coding analysis results

Author: Chaos
Version: 1.0
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
</style>
""", unsafe_allow_html=True)

class TelegramAnalysisDashboard:
    def __init__(self):
        self.df = None
        self.summary_data = None
        
    def load_data(self, csv_path, json_path):
        """Load analysis data from CSV and JSON files"""
        try:
            self.df = pd.read_csv(csv_path)
            with open(json_path, 'r') as f:
                self.summary_data = json.load(f)
            return True
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return False
    
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

    def create_subcategory_analysis(self):
        """Create subcategory analysis visualization"""
        st.markdown('<div class="category-header">🔍 Subcategory Deep Dive</div>', unsafe_allow_html=True)
        
        if self.summary_data and 'subcategory_distribution' in self.summary_data:
            subcats = self.summary_data['subcategory_distribution']
            
            # Top 10 subcategories
            top_subcats = dict(list(subcats.items())[:10])
            
            fig = px.bar(
                x=list(top_subcats.values()),
                y=list(top_subcats.keys()),
                orientation='h',
                title="Top 10 Subcategories by Message Count",
                labels={'x': 'Number of Messages', 'y': 'Subcategory'},
                color=list(top_subcats.values()),
                color_continuous_scale='plasma'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # Subcategory insights
            st.markdown('<div class="insight-box">', unsafe_allow_html=True)
            st.markdown("**Key Insights:**")
            st.markdown(f"• **Religious Opposition (3.religious_opposition)** dominates with {subcats.get('3.religious_opposition', 0)} messages")
            st.markdown(f"• **Emasculation Narratives (2.emasculation)** shows {subcats.get('2.emasculation', 0)} coordinated messages")
            st.markdown(f"• **Cultural Authenticity (1.cultural_authenticity)** appears {subcats.get('1.cultural_authenticity', 0)} times")
            st.markdown('</div>', unsafe_allow_html=True)

    def create_intensity_analysis(self):
        """Create intensity distribution analysis"""
        st.markdown('<div class="category-header">⚡ Message Intensity Analysis</div>', unsafe_allow_html=True)
        
        if self.summary_data and 'intensity_distribution' in self.summary_data:
            intensity = self.summary_data['intensity_distribution']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Intensity distribution
                levels = [f"Level {k}" for k in sorted(intensity.keys())]
                counts = [intensity[k] for k in sorted(intensity.keys())]
                
                fig = px.bar(
                    x=levels,
                    y=counts,
                    title="Message Intensity Distribution",
                    labels={'x': 'Intensity Level', 'y': 'Number of Messages'},
                    color=counts,
                    color_continuous_scale='reds'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Intensity explanation
                st.markdown("**Intensity Scale:**")
                st.markdown("- **Level 1:** Subtle suggestions and implicit messaging")
                st.markdown("- **Level 2:** Moderate explicit content")
                st.markdown("- **Level 3:** Direct accusations without evidence")
                st.markdown("- **Level 4:** Strong coordinated messaging")
                st.markdown("- **Level 5:** Systematic campaigns with documentation")
                
                if intensity.get('1', 0) > intensity.get('2', 0) + intensity.get('3', 0):
                    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                    st.markdown("**⚠️ Analysis Alert:** High prevalence of Level 1 intensity suggests sophisticated messaging designed to evade content moderation.")
                    st.markdown('</div>', unsafe_allow_html=True)

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

    def create_linguistic_markers(self):
        """Create linguistic markers analysis"""
        st.markdown('<div class="category-header">💬 Linguistic Markers Analysis</div>', unsafe_allow_html=True)
        
        if self.summary_data and 'top_linguistic_markers' in self.summary_data:
            markers = self.summary_data['top_linguistic_markers']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top markers bar chart
                top_markers = dict(list(markers.items())[:15])
                
                fig = px.bar(
                    x=list(top_markers.values()),
                    y=list(top_markers.keys()),
                    orientation='h',
                    title="Top 15 Linguistic Markers",
                    labels={'x': 'Occurrences', 'y': 'Linguistic Marker'},
                    color=list(top_markers.values()),
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Marker insights
                st.markdown("**Key Linguistic Patterns:**")
                
                religious_markers = ['sin', 'immoral', 'abomination']
                masculinity_markers = ['beta male', 'emasculation', 'real men']
                cultural_markers = ['imported', 'our culture', 'traditional values']
                
                religious_count = sum(markers.get(m, 0) for m in religious_markers)
                masculinity_count = sum(markers.get(m, 0) for m in masculinity_markers)
                cultural_count = sum(markers.get(m, 0) for m in cultural_markers)
                
                st.markdown(f"**Religious Opposition:** {religious_count} total occurrences")
                st.markdown(f"- 'sin': {markers.get('sin', 0)} times")
                st.markdown(f"- 'immoral': {markers.get('immoral', 0)} times")
                
                st.markdown(f"**Masculinity Crisis:** {masculinity_count} total occurrences")
                st.markdown(f"- 'beta male': {markers.get('beta male', 0)} times")
                st.markdown(f"- 'emasculation': {markers.get('emasculation', 0)} times")
                
                st.markdown(f"**Cultural Authenticity:** {cultural_count} total occurrences")
                st.markdown(f"- 'imported': {markers.get('imported', 0)} times")
                st.markdown(f"- 'our culture': {markers.get('our culture', 0)} times")

    def create_media_analysis(self):
        """Create media content analysis"""
        st.markdown('<div class="category-header">📸 Media Content Analysis</div>', unsafe_allow_html=True)
        
        if self.summary_data:
            media_count = self.summary_data.get('content_with_media', 0)
            total_relevant = self.summary_data['analysis_summary']['relevant_messages_found']
            media_percentage = (media_count / total_relevant * 100) if total_relevant > 0 else 0
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Media vs non-media distribution
                fig = px.pie(
                    values=[media_count, total_relevant - media_count],
                    names=['With Media', 'Text Only'],
                    title="Media Content Distribution",
                    color_discrete_sequence=['#ff7f0e', '#1f77b4']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric(
                    "Messages with Media",
                    f"{media_count:,}",
                    f"{media_percentage:.1f}% of relevant messages"
                )
                
                if 'media_distribution' in self.summary_data:
                    media_types = self.summary_data['media_distribution']
                    st.markdown("**Media Type Breakdown:**")
                    for media_type, count in media_types.items():
                        if media_type:
                            st.markdown(f"- {media_type.title()}: {count} messages")
                
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("**Strategic Insight:** High media usage suggests sophisticated content strategy designed to increase engagement and viral potential.")
                st.markdown('</div>', unsafe_allow_html=True)

    def create_temporal_analysis(self):
        """Create temporal patterns analysis"""
        st.markdown('<div class="category-header">📅 Temporal Patterns</div>', unsafe_allow_html=True)
        
        if self.df is not None and 'Date' in self.df.columns:
            # Convert date column
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Date_Only'] = self.df['Date'].dt.date
            
            # Daily message counts
            daily_counts = self.df.groupby('Date_Only').size().reset_index(name='Message_Count')
            
            fig = px.line(
                daily_counts,
                x='Date_Only',
                y='Message_Count',
                title="Daily Anti-Gender Message Volume",
                labels={'Date_Only': 'Date', 'Message_Count': 'Number of Messages'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Category distribution over time
            if 'Categories' in self.df.columns:
                # Expand categories and create daily category counts
                category_data = []
                for _, row in self.df.iterrows():
                    categories = row['Categories'].split('; ') if row['Categories'] else []
                    for cat in categories:
                        category_data.append({
                            'Date': row['Date_Only'],
                            'Category': cat.strip()
                        })
                
                if category_data:
                    cat_df = pd.DataFrame(category_data)
                    daily_cat_counts = cat_df.groupby(['Date', 'Category']).size().reset_index(name='Count')
                    
                    fig = px.area(
                        daily_cat_counts,
                        x='Date',
                        y='Count',
                        color='Category',
                        title="Category Distribution Over Time",
                        labels={'Date': 'Date', 'Count': 'Number of Messages'}
                    )
                    st.plotly_chart(fig, use_container_width=True)

    def create_message_explorer(self):
        """Create message explorer section"""
        st.markdown('<div class="category-header">🔎 Message Content Explorer</div>', unsafe_allow_html=True)
        
        if self.df is not None:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                categories = ['All'] + list(set(cat.strip() for cats in self.df['Categories'].dropna() 
                                               for cat in cats.split('; ')))
                selected_category = st.selectbox("Filter by Category", categories)
            
            with col2:
                intensity_levels = ['All'] + sorted(self.df['Intensity_Score'].unique())
                selected_intensity = st.selectbox("Filter by Intensity", intensity_levels)
            
            with col3:
                min_views = st.number_input("Minimum Views", min_value=0, value=0)
            
            # Filter dataframe
            filtered_df = self.df.copy()
            
            if selected_category != 'All':
                filtered_df = filtered_df[filtered_df['Categories'].str.contains(selected_category, na=False)]
            
            if selected_intensity != 'All':
                filtered_df = filtered_df[filtered_df['Intensity_Score'] == selected_intensity]
            
            if min_views > 0:
                filtered_df = filtered_df[filtered_df['Views'] >= min_views]
            
            # Display results
            st.markdown(f"**Showing {len(filtered_df)} messages matching your criteria:**")
            
            # Sample messages
            if not filtered_df.empty:
                sample_size = min(10, len(filtered_df))
                sample_df = filtered_df.nlargest(sample_size, 'Views')[
                    ['Message_ID', 'Text_Preview', 'Categories', 'Intensity_Score', 'Views', 'Forwards']
                ]
                
                for _, row in sample_df.iterrows():
                    with st.expander(f"Message {row['Message_ID']} - {row['Views']} views"):
                        st.markdown(f"**Text Preview:** {row['Text_Preview']}")
                        st.markdown(f"**Categories:** {row['Categories']}")
                        st.markdown(f"**Intensity:** Level {row['Intensity_Score']}")
                        st.markdown(f"**Engagement:** {row['Views']} views, {row['Forwards']} forwards")

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

    def run_dashboard(self):
        """Main dashboard runner"""
        st.sidebar.title("📊 Navigation")
        
        # Data loading section
        st.sidebar.markdown("### Data Sources")
        csv_file = st.sidebar.file_uploader("Upload CSV Results", type=['csv'])
        json_file = st.sidebar.file_uploader("Upload JSON Summary", type=['json'])
        
        # Default file paths - try combined results first
        default_csv = "../combined_analysis_results/coded_messages_detailed.csv"
        default_json = "../combined_analysis_results/analysis_summary.json"
        
        # Fallback to single dataset if combined doesn't exist
        if not os.path.exists(default_csv) or not os.path.exists(default_json):
            default_csv = "../telegram_analysis_results/coded_messages_detailed.csv"
            default_json = "../telegram_analysis_results/analysis_summary.json"
        
        # Load data
        data_loaded = False
        if csv_file and json_file:
            # Save uploaded files temporarily
            with open("temp_analysis.csv", "wb") as f:
                f.write(csv_file.getvalue())
            with open("temp_summary.json", "wb") as f:
                f.write(json_file.getvalue())
            data_loaded = self.load_data("temp_analysis.csv", "temp_summary.json")
        elif os.path.exists(default_csv) and os.path.exists(default_json):
            data_loaded = self.load_data(default_csv, default_json)
            st.sidebar.success("✅ Using default analysis results")
        
        if not data_loaded:
            st.error("Please upload analysis results or ensure default files exist in telegram_analysis_results/")
            st.info("Expected files: coded_messages_detailed.csv and analysis_summary.json")
            return
        
        # Navigation
        pages = [
            "📈 Overview",
            "📊 Categories",
            "🔍 Subcategories", 
            "⚡ Intensity",
            "🚀 Engagement",
            "💬 Linguistics",
            "📸 Media",
            "📅 Temporal",
            "🔎 Explorer",
            "🧠 Insights"
        ]
        
        selected_page = st.sidebar.radio("Select Analysis View", pages)
        
        # Render selected page
        if selected_page == "📈 Overview":
            self.create_overview_metrics()
        elif selected_page == "📊 Categories":
            self.create_category_distribution()
        elif selected_page == "🔍 Subcategories":
            self.create_subcategory_analysis()
        elif selected_page == "⚡ Intensity":
            self.create_intensity_analysis()
        elif selected_page == "🚀 Engagement":
            self.create_engagement_analysis()
        elif selected_page == "💬 Linguistics":
            self.create_linguistic_markers()
        elif selected_page == "📸 Media":
            self.create_media_analysis()
        elif selected_page == "📅 Temporal":
            self.create_temporal_analysis()
        elif selected_page == "🔎 Explorer":
            self.create_message_explorer()
        elif selected_page == "🧠 Insights":
            self.create_research_insights()
        
        # Sidebar info
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
