# 📊 Telegram Analysis Dashboard

## Overview

This directory contains comprehensive visualization tools for your Telegram analysis results based on the DMCA Thematic Coding Guide. You have multiple dashboard options to choose from based on your needs.

## 🎯 Dashboard Options

### 1. Interactive Streamlit Dashboard (Recommended)
**File:** `telegram_analysis_dashboard.py`
**Launcher:** `launch_dashboard.py`

**Features:**
- 📊 Interactive charts and visualizations
- 🔍 Real-time data filtering and exploration
- 📱 Responsive design that works on all devices
- 🧭 Multi-page navigation with 10 different analysis views
- 📂 File upload capability for new datasets
- 🔄 Dynamic content updates

**Usage:**
```bash
# Launch the interactive dashboard
python3 launch_dashboard.py

# Or manually run streamlit
streamlit run telegram_analysis_dashboard.py
```

**Dashboard Pages:**
- 📈 **Overview:** Executive summary with key metrics
- 📊 **Categories:** Content category distribution analysis
- 🔍 **Subcategories:** Deep dive into subcategory patterns
- ⚡ **Intensity:** Message intensity distribution and analysis
- 🚀 **Engagement:** Viral spread and engagement patterns
- 💬 **Linguistics:** Top linguistic markers and patterns
- 📸 **Media:** Media content distribution analysis
- 📅 **Temporal:** Time-based pattern analysis
- 🔎 **Explorer:** Interactive message content browser
- 🧠 **Insights:** Research findings and recommendations

### 2. Static HTML Dashboard
**File:** `telegram_analysis_dashboard.html`
**Generator:** `generate_static_dashboard.py`

**Features:**
- 🌐 Self-contained HTML file that works offline
- 📊 Professional-looking static visualizations
- 📱 Mobile-responsive design
- 🎨 Beautiful gradient styling and modern UI
- 📈 All key charts and insights in one page
- 💾 Easy to share and archive

**Usage:**
```bash
# Generate static dashboard
python3 generate_static_dashboard.py

# Then open telegram_analysis_dashboard.html in your browser
```

## 📂 Required Files

Your analysis must have generated these files for the dashboards to work:

**Option 1: Combined Analysis Results (12,000 messages - Recommended)**
```
combined_analysis_results/
├── coded_messages_detailed.csv    # Combined detailed message analysis
├── analysis_summary.json          # Combined summary statistics
└── analysis_summary_readable.md   # Combined human-readable summary
```

**Option 2: Single Dataset Results (6,000 messages)**
```
telegram_analysis_results/
├── coded_messages_detailed.csv    # Single dataset detailed analysis
├── analysis_summary.json          # Single dataset summary statistics
└── analysis_summary_readable.md   # Single dataset human-readable summary
```

**Note:** The dashboards will automatically use combined results if available, otherwise fall back to single dataset results.

If these files don't exist, run the analysis first:
```bash
python3 telegram_codebook_analyzer.py [your_data_directory]
# Then combine multiple datasets if needed:
python3 combine_analysis_results.py
```

## 🔧 Dependencies

### For Interactive Dashboard (Streamlit):
```bash
pip3 install streamlit plotly pandas numpy
```

### For Static Dashboard:
```bash
pip3 install plotly pandas
```

## 📊 Dashboard Features

### Key Visualizations
1. **Overview Metrics Cards** - Total messages, relevance rate, viral content
2. **Category Distribution** - Pie and bar charts showing content categories
3. **Subcategory Analysis** - Top 10 subcategories with detailed breakdown
4. **Intensity Heatmaps** - Message intensity distribution (Levels 1-5)
5. **Linguistic Markers** - Top 15 most frequent markers with context
6. **Engagement Scatter** - Views vs forwards relationship analysis
7. **Media Analysis** - Photo/document distribution and strategy insights
8. **Temporal Patterns** - Daily message volumes and category trends

### Research Insights
- **Religious Opposition Analysis** - 977 occurrences of "sin" as primary marker
- **Masculinity Crisis Patterns** - "Beta male" and emasculation narratives
- **Coordination Evidence** - "Masculinity Saturday" recurring campaigns
- **Viral Amplification** - 85.9% forward rate indicating high engagement
- **Media Strategy** - 53% multimedia content for increased viral potential

## 🎨 Dashboard Screenshots

### Interactive Dashboard Navigation
The Streamlit dashboard provides:
- Sidebar navigation between analysis views
- Real-time data filtering and exploration
- Interactive charts with hover details
- Message content browser with search
- Research insights and recommendations

### Static Dashboard Layout
The HTML dashboard includes:
- Executive summary metrics cards
- Professional chart layouts in grid format
- Research insights summary
- Mobile-responsive design
- Offline functionality

## 📈 Analysis Framework

Both dashboards visualize results from the **DMCA Thematic Coding Guide v1.0**:

1. **Digital Disinformation & Anti-Gender Narratives**
2. **Masculinity & Gender Backlash**
3. **LGBTQ+ Hate Speech & Anti-Rights Rhetoric**
4. **SRHR & Moral Panic**
5. **Gender-Based Violence Disinformation**
6. **Political & Policy-Driven Gender Panic**
7. **AI & Platform Amplification Patterns**

## 🔍 Usage Tips

### Interactive Dashboard:
- Use filters in the Explorer page to find specific content types
- Check the Temporal page for time-based campaign patterns
- View Engagement page to identify most viral content
- Use Linguistics page to understand framing strategies

### Static Dashboard:
- Perfect for presentations and reports
- Can be embedded in websites or shared via email
- Includes all key insights in a single scrollable page
- Works without internet connection

## 🚀 Quick Start

1. **Ensure you have analysis results:**
   ```bash
   ls telegram_analysis_results/
   # Should show: coded_messages_detailed.csv, analysis_summary.json
   ```

2. **Choose your dashboard type:**
   
   **Interactive (recommended):**
   ```bash
   python3 launch_dashboard.py
   ```
   
   **Static:**
   ```bash
   python3 generate_static_dashboard.py
   open telegram_analysis_dashboard.html
   ```

3. **Explore the data and insights!**

## 📋 Troubleshooting

### Common Issues:

**"Analysis results not found"**
- Run `python3 telegram_codebook_analyzer.py [data_dir]` first

**"Module not found" errors**
- Install dependencies: `pip3 install streamlit plotly pandas`

**Dashboard won't start**
- Check Python version: `python3 --version` (needs 3.7+)
- Try: `streamlit run telegram_analysis_dashboard.py` directly

**Charts not displaying**
- For static dashboard, ensure internet connection for Plotly CDN
- Try refreshing the browser page

## 💡 Advanced Usage

### Analyzing Multiple Datasets:
```bash
# Analyze all your datasets
python3 telegram_codebook_analyzer.py dataset1/ -o results1/
python3 telegram_codebook_analyzer.py dataset2/ -o results2/

# Upload different results in the interactive dashboard
# Or generate separate static dashboards
```

### Customizing Charts:
- Edit `telegram_analysis_dashboard.py` for Streamlit customizations
- Edit `generate_static_dashboard.py` for static chart modifications

### Sharing Results:
- Interactive: Share the URL when dashboard is running
- Static: Share the `telegram_analysis_dashboard.html` file

---

**Framework:** DMCA Thematic Coding Guide v1.0  
**Analyst:** Chaos  
**Date:** August 2025
