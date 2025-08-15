# 🚀 Dashboard Deployment Guide

## Overview
This guide covers multiple deployment options for your Telegram Analysis Dashboard, from easiest to most advanced.

## 📋 Prerequisites
✅ `streamlit_app.py` - Main dashboard application  
✅ `requirements.txt` - Python dependencies  
✅ `.streamlit/config.toml` - Streamlit configuration  
✅ `DEPLOYMENT_README.md` - Public description  

## 🎯 Deployment Options

### 1. Streamlit Cloud (Recommended - FREE)
**Best for**: Quick deployment, sharing with researchers, academic use

**Steps:**
1. **Create GitHub Repository**
   ```bash
   # Initialize git repo (if not already done)
   git init
   git add streamlit_app.py requirements.txt .streamlit/
   git add DEPLOYMENT_README.md
   git commit -m "Add Telegram Analysis Dashboard"
   
   # Push to GitHub
   git remote add origin https://github.com/YOUR_USERNAME/telegram-dashboard
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Click "Deploy!"

3. **Your dashboard will be live at**: `https://YOUR_USERNAME-telegram-dashboard-streamlit-app-xxxxx.streamlit.app`

**Pros**: Free, easy, automatic updates from GitHub  
**Cons**: Public by default, limited resources

---

### 2. Railway (Easy - $5/month)
**Best for**: Private deployments, more control, better performance

**Steps:**
1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   # or
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Deploy**
   ```bash
   railway login
   railway init
   railway add
   railway deploy
   ```

3. **Configure**
   - Set start command: `streamlit run streamlit_app.py --server.port $PORT`
   - Add environment variables if needed

**Pros**: Private, custom domains, good performance  
**Cons**: Costs $5/month after trial

---

### 3. Heroku (Reliable - $7/month)
**Best for**: Production apps, enterprise use

**Steps:**
1. **Create Heroku App**
   ```bash
   # Install Heroku CLI first
   heroku create your-telegram-dashboard
   ```

2. **Add Procfile**
   ```bash
   echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

3. **Deploy**
   ```bash
   git add Procfile
   git commit -m "Add Procfile for Heroku"
   git push heroku main
   ```

**Pros**: Very reliable, good for production  
**Cons**: Costs money, more complex setup

---

### 4. Render (Modern - FREE/Paid)
**Best for**: Modern alternative to Heroku

**Steps:**
1. **Connect GitHub**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository

2. **Configure Web Service**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

**Pros**: Free tier available, modern platform  
**Cons**: Free tier has limitations

---

## 🔐 Security Considerations

### For Sensitive Research Data:
1. **Use Private Repositories** - Never commit actual data files
2. **Environment Variables** - Store any API keys securely
3. **Access Control** - Consider adding authentication:

```python
# Add to streamlit_app.py for basic password protection
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "your_research_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password incorrect")
        return False
    else:
        return True

# Add at start of run_dashboard method:
if not check_password():
    return
```

## 🎨 Customization

### Custom Domain (Railway/Heroku)
- Add your domain in platform settings
- Update DNS records to point to your deployment

### Branding
- Edit colors in `.streamlit/config.toml`
- Update title and descriptions in `streamlit_app.py`
- Add your institution logo

## 📊 Usage Analytics

### Add Google Analytics (Optional)
```python
# Add to streamlit_app.py head
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
""", unsafe_allow_html=True)
```

## 🔧 Troubleshooting

### Common Issues:
1. **Port Error**: Ensure `--server.port $PORT` in start command
2. **Dependencies**: Check `requirements.txt` has all packages
3. **Memory**: Large datasets may need paid tiers
4. **Timeout**: Consider optimizing data loading

### Debug Mode:
```bash
# Test locally first
streamlit run streamlit_app.py --server.port 8501
```

## 📋 Deployment Checklist

Before deploying:
- [ ] Test dashboard locally
- [ ] Check all charts render correctly
- [ ] Verify file upload functionality
- [ ] Test demo mode
- [ ] Remove any local file paths
- [ ] Update README with usage instructions
- [ ] Consider data sensitivity and access controls

## 🎯 Recommended Approach

For your research dashboard, I recommend:

1. **Start with Streamlit Cloud** (free, easy sharing)
2. **Upgrade to Railway** if you need privacy/performance
3. **Add authentication** if handling sensitive data
4. **Use demo mode** for public sharing, upload mode for researchers

---

**Need help?** The dashboard includes both upload functionality for your real data and demo mode for public demonstrations, making it perfect for academic research sharing!
