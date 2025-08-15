#!/usr/bin/env python3
"""
Static HTML Dashboard Generator
Creates a static HTML dashboard for Telegram analysis results
With comprehensive sample data when actual analysis files are not available

Author: Chaos
Version: 2.0
Date: August 2025
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import json
import os
import numpy as np
from datetime import datetime, timedelta

class StaticDashboardGenerator:
    def __init__(self, csv_path, json_path):
        self.csv_path = csv_path
        self.json_path = json_path
        self.df = None
        self.summary_data = None
        self.charts = []
        
    def load_data(self):
        """Load analysis data"""
        try:
            self.df = pd.read_csv(self.csv_path)
            with open(self.json_path, 'r') as f:
                self.summary_data = json.load(f)
            print("✅ Data loaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def create_overview_chart(self):
        """Create overview metrics chart"""
        if not self.summary_data:
            return ""
        
        summary = self.summary_data['analysis_summary']
        engagement = self.summary_data.get('engagement_analysis', {})
        
        # Create metrics visualization
        fig = go.Figure()
        
        metrics = [
            ("Total Messages", summary['total_messages_analyzed']),
            ("Relevant Messages", summary['relevant_messages_found']),
            ("Viral Messages", engagement.get('viral_messages', 0)),
            ("High Engagement", engagement.get('high_engagement_messages', 0))
        ]
        
        fig.add_trace(go.Bar(
            x=[m[0] for m in metrics],
            y=[m[1] for m in metrics],
            name="Overview Metrics",
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        ))
        
        fig.update_layout(
            title="📊 Analysis Overview Metrics",
            xaxis_title="Metric",
            yaxis_title="Count",
            height=400
        )
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_category_chart(self):
        """Create category distribution chart"""
        if not self.summary_data or 'category_distribution' not in self.summary_data:
            return ""
        
        categories = self.summary_data['category_distribution']
        
        # Pie chart
        fig = px.pie(
            values=list(categories.values()),
            names=list(categories.keys()),
            title="📈 Anti-Gender Content Categories Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_subcategory_chart(self):
        """Create subcategory analysis chart"""
        if not self.summary_data or 'subcategory_distribution' not in self.summary_data:
            return ""
        
        subcats = self.summary_data['subcategory_distribution']
        top_subcats = dict(list(subcats.items())[:10])
        
        fig = px.bar(
            x=list(top_subcats.values()),
            y=list(top_subcats.keys()),
            orientation='h',
            title="🔍 Top 10 Subcategories",
            labels={'x': 'Number of Messages', 'y': 'Subcategory'},
            color=list(top_subcats.values()),
            color_continuous_scale='plasma'
        )
        fig.update_layout(height=500)
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_intensity_chart(self):
        """Create intensity distribution chart"""
        if not self.summary_data or 'intensity_distribution' not in self.summary_data:
            return ""
        
        intensity = self.summary_data['intensity_distribution']
        
        levels = [f"Level {k}" for k in sorted(intensity.keys())]
        counts = [intensity[k] for k in sorted(intensity.keys())]
        
        fig = px.bar(
            x=levels,
            y=counts,
            title="⚡ Message Intensity Distribution",
            labels={'x': 'Intensity Level', 'y': 'Number of Messages'},
            color=counts,
            color_continuous_scale='reds'
        )
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_linguistic_markers_chart(self):
        """Create linguistic markers chart"""
        if not self.summary_data or 'top_linguistic_markers' not in self.summary_data:
            return ""
        
        markers = self.summary_data['top_linguistic_markers']
        top_markers = dict(list(markers.items())[:15])
        
        fig = px.bar(
            x=list(top_markers.values()),
            y=list(top_markers.keys()),
            orientation='h',
            title="💬 Top 15 Linguistic Markers",
            labels={'x': 'Occurrences', 'y': 'Linguistic Marker'},
            color=list(top_markers.values()),
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=600)
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_engagement_chart(self):
        """Create engagement analysis chart"""
        if self.df is None:
            return ""
        
        # Views vs Forwards scatter plot
        fig = px.scatter(
            self.df,
            x='Views',
            y='Forwards',
            color='Intensity_Score',
            title="🚀 Views vs Forwards Relationship",
            labels={'x': 'Views', 'y': 'Forwards'},
            hover_data=['Categories'],
            color_continuous_scale='viridis'
        )
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_media_chart(self):
        """Create media content analysis chart"""
        if not self.summary_data:
            return ""
        
        media_count = self.summary_data.get('content_with_media', 0)
        total_relevant = self.summary_data['analysis_summary']['relevant_messages_found']
        
        fig = px.pie(
            values=[media_count, total_relevant - media_count],
            names=['With Media', 'Text Only'],
            title="📸 Media Content Distribution",
            color_discrete_sequence=['#ff7f0e', '#1f77b4']
        )
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_timeline_chart(self):
        """Create timeline analysis chart"""
        if self.df is None or 'Date' not in self.df.columns:
            return ""
        
        # Ensure Date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.df['Date']):
            self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Group by date and count messages
        daily_counts = self.df.groupby(self.df['Date'].dt.date).size().reset_index()
        daily_counts.columns = ['Date', 'Messages']
        
        fig = px.line(
            daily_counts,
            x='Date',
            y='Messages',
            title="📅 Daily Message Volume Timeline",
            labels={'x': 'Date', 'y': 'Number of Messages'}
        )
        fig.update_traces(line=dict(color='#1f77b4', width=3))
        fig.update_layout(height=400)
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def create_views_distribution_chart(self):
        """Create views distribution histogram"""
        if self.df is None:
            return ""
        
        fig = px.histogram(
            self.df,
            x='Views',
            nbins=30,
            title="👀 Views Distribution Analysis",
            labels={'x': 'Views', 'y': 'Number of Messages'},
            color_discrete_sequence=['#2ca02c']
        )
        fig.update_layout(height=400)
        
        return pyo.plot(fig, output_type='div', include_plotlyjs=False)
    
    def load_sample_data(self):
        """Load comprehensive sample data for demonstration"""
        print("📊 Loading sample data for demonstration...")
        
        # Create comprehensive sample data
        self.summary_data = {
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
                "4.traditional_family": 25,
                "5.imported_ideology": 20,
                "6.moral_corruption": 15,
                "7.family_destruction": 12,
                "8.children_targeting": 8
            },
            "intensity_distribution": {
                "1": 1312,
                "2": 3
            },
            "engagement_analysis": {
                "viral_messages": 1129,
                "average_views": 8547,
                "average_forwards": 2.1,
                "max_views": 89000,
                "high_engagement_messages": 456
            },
            "top_linguistic_markers": {
                "sin": 977,
                "immoral": 156,
                "abomination": 89,
                "against God": 67,
                "imported": 45,
                "our culture": 34,
                "beta male": 23,
                "emasculation": 12,
                "traditional values": 45,
                "family values": 38,
                "western influence": 29,
                "moral decay": 25,
                "unnatural": 67,
                "corruption": 43,
                "destruction": 31
            },
            "content_with_media": 700,
            "media_distribution": {
                "photo": 450,
                "document": 250
            }
        }
        
        # Create realistic sample DataFrame
        np.random.seed(42)  # For reproducible results
        sample_data = []
        categories = list(self.summary_data['category_distribution'].keys())
        subcategories = list(self.summary_data['subcategory_distribution'].keys())
        
        # Generate diverse sample data
        for i in range(1315):
            category = np.random.choice(categories, p=[0.947, 0.027, 0.023, 0.003])
            subcategory = np.random.choice(subcategories[:4])  # Top 4 subcategories
            intensity = np.random.choice([1, 2], p=[0.998, 0.002])
            
            # Generate realistic view and forward counts
            views = int(np.random.lognormal(7.5, 1.5))  # Log-normal distribution
            views = max(100, min(views, 89000))  # Constrain to realistic range
            
            forwards = int(np.random.poisson(2.1))  # Poisson distribution
            forwards = max(0, min(forwards, 20))  # Constrain to realistic range
            
            # Generate dates over the past year
            date = datetime.now() - timedelta(days=np.random.randint(0, 365))
            
            sample_data.append({
                'Message_ID': f'msg_{i+1:04d}',
                'Text_Preview': f'Sample anti-gender message content {i+1}... [religious framing, cultural authenticity, moral opposition]',
                'Categories': category,
                'Subcategories': subcategory,
                'Intensity_Score': intensity,
                'Views': views,
                'Forwards': forwards,
                'Date': date,
                'Has_Media': np.random.choice([True, False], p=[0.53, 0.47])
            })
        
        self.df = pd.DataFrame(sample_data)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        print("✅ Sample data loaded successfully")
        return True
    
    def generate_html_dashboard(self, output_path="telegram_analysis_dashboard.html", use_sample_data=False):
        """Generate complete HTML dashboard"""
        if use_sample_data:
            if not self.load_sample_data():
                return False
        else:
            if not self.load_data():
                return False
        
        print("📊 Generating charts...")
        
        # Generate all charts
        overview_chart = self.create_overview_chart()
        category_chart = self.create_category_chart()
        subcategory_chart = self.create_subcategory_chart()
        intensity_chart = self.create_intensity_chart()
        linguistic_chart = self.create_linguistic_markers_chart()
        engagement_chart = self.create_engagement_chart()
        media_chart = self.create_media_chart()
        timeline_chart = self.create_timeline_chart()
        views_chart = self.create_views_distribution_chart()
        
        # Get summary statistics
        summary = self.summary_data['analysis_summary']
        engagement = self.summary_data.get('engagement_analysis', {})
        
        # HTML template
        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Telegram Analysis Dashboard</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 40px;
                    color: #2c3e50;
                }}
                .header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    color: #1f77b4;
                }}
                .header p {{
                    font-size: 1.2em;
                    color: #7f8c8d;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                .metric-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .metric-value {{
                    font-size: 2em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .metric-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                .chart-container {{
                    margin-bottom: 40px;
                    background: white;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .chart-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                    gap: 30px;
                    margin-bottom: 40px;
                }}
                .insights {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-top: 40px;
                }}
                .insights h3 {{
                    margin-top: 0;
                    font-size: 1.5em;
                }}
                .insights ul {{
                    margin: 0;
                    padding-left: 20px;
                }}
                .insights li {{
                    margin-bottom: 10px;
                }}
                .timestamp {{
                    text-align: center;
                    color: #7f8c8d;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ecf0f1;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Telegram Analysis Dashboard</h1>
                    <p>Anti-Gender Narratives Analysis - DMCA Thematic Coding Framework v1.0</p>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{summary['total_messages_analyzed']:,}</div>
                        <div class="metric-label">Total Messages Analyzed</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary['relevant_messages_found']:,}</div>
                        <div class="metric-label">Relevant Messages Found</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{summary['relevance_rate']:.2f}%</div>
                        <div class="metric-label">Relevance Rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{engagement.get('viral_messages', 0):,}</div>
                        <div class="metric-label">Viral Messages</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    {overview_chart}
                </div>
                
                <div class="chart-grid">
                    <div class="chart-container">
                        {category_chart}
                    </div>
                    <div class="chart-container">
                        {intensity_chart}
                    </div>
                </div>
                
                <div class="chart-container">
                    {subcategory_chart}
                </div>
                
                <div class="chart-container">
                    {linguistic_chart}
                </div>
                
                <div class="chart-grid">
                    <div class="chart-container">
                        {engagement_chart}
                    </div>
                    <div class="chart-container">
                        {media_chart}
                    </div>
                </div>
                
                <div class="insights">
                    <h3>🧠 Key Research Insights</h3>
                    <ul>
                        <li><strong>Religious Opposition Dominance:</strong> 97% of coded content uses religious framing with "sin" appearing 977 times</li>
                        <li><strong>Sophisticated Messaging Strategy:</strong> 99.9% content at Level 1 intensity, designed to evade content moderation</li>
                        <li><strong>High Viral Potential:</strong> 85.9% of relevant messages were forwarded, indicating strong engagement</li>
                        <li><strong>Coordinated Campaign Evidence:</strong> "Masculinity Saturday" recurring pattern suggests organized efforts</li>
                        <li><strong>Media Strategy:</strong> 53% of relevant messages include multimedia content for increased viral potential</li>
                    </ul>
                </div>
                
                <div class="timestamp">
                    <p>Analysis generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
                    <p>Framework: DMCA Thematic Coding Guide v1.0 | Analyst: Chaos</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Static dashboard generated: {output_path}")
        return True

def main():
    print("🚀 Generating Static HTML Dashboard...")
    
    # File paths - try combined results first, then fallback to single dataset
    csv_path = "../combined_analysis_results/coded_messages_detailed.csv"
    json_path = "../combined_analysis_results/analysis_summary.json"
    
    # Fallback to single dataset if combined doesn't exist
    if not os.path.exists(csv_path) or not os.path.exists(json_path):
        csv_path = "../telegram_analysis_results/coded_messages_detailed.csv"
        json_path = "../telegram_analysis_results/analysis_summary.json"
    
    # Generate dashboard - use sample data if analysis files don't exist
    generator = StaticDashboardGenerator(csv_path, json_path)
    use_sample = not (os.path.exists(csv_path) and os.path.exists(json_path))
    
    if use_sample:
        print("📊 Analysis results not found, generating dashboard with comprehensive sample data...")
        print("💡 This demonstrates all the features your dashboard will have with real data.")
    
    if generator.generate_html_dashboard(use_sample_data=use_sample):
        print("\n" + "="*50)
        print("🎉 Dashboard created successfully!")
        print("📂 File: telegram_analysis_dashboard.html")
        print("🌐 Open the file in your browser to view the dashboard")
        if use_sample:
            print("📝 Note: This dashboard uses sample data for demonstration")
        print("="*50)
    else:
        print("❌ Failed to generate dashboard")

if __name__ == "__main__":
    main()
