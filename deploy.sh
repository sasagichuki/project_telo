#!/bin/bash

echo "🚀 Telegram Analysis Dashboard - Quick Deploy"
echo "=============================================="

# Check if git is configured
if ! git config user.name > /dev/null; then
    echo "⚠️  Git user not configured. Let's set that up:"
    read -p "Enter your name: " username
    read -p "Enter your email: " useremail
    git config --global user.name "$username"
    git config --global user.email "$useremail"
    echo "✅ Git configured!"
fi

echo ""
echo "📋 Deployment Options:"
echo "1. Streamlit Cloud (FREE - Recommended)"
echo "2. Railway ($5/month)"
echo "3. Heroku ($7/month)"
echo "4. Render (FREE/Paid)"
echo ""

read -p "Choose deployment option (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Streamlit Cloud Deployment"
        echo "=============================="
        echo "1. Go to: https://share.streamlit.io"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New app'"
        echo "4. Connect your GitHub repository"
        echo "5. Set main file: streamlit_app.py"
        echo "6. Click Deploy!"
        echo ""
        echo "📂 You'll need to:"
        echo "   - Create a GitHub repository"
        echo "   - Push this code to GitHub"
        echo "   - Connect it to Streamlit Cloud"
        echo ""
        echo "🔗 Want help creating the GitHub repo? (y/n)"
        read -p "> " github_help
        
        if [[ $github_help == "y" || $github_help == "Y" ]]; then
            echo ""
            echo "📁 GitHub Repository Setup:"
            echo "1. Go to: https://github.com/new"
            echo "2. Repository name: telegram-analysis-dashboard"
            echo "3. Make it Private (recommended for research)"
            echo "4. Don't initialize with README (we have files already)"
            echo "5. Click 'Create repository'"
            echo ""
            echo "Then run these commands:"
            echo "git remote add origin https://github.com/YOUR_USERNAME/telegram-analysis-dashboard"
            echo "git branch -M main"
            echo "git push -u origin main"
        fi
        ;;
    2)
        echo ""
        echo "🚂 Railway Deployment"
        echo "===================="
        echo "1. Install Railway CLI: npm install -g @railway/cli"
        echo "2. Run: railway login"
        echo "3. Run: railway init"
        echo "4. Run: railway deploy"
        echo ""
        echo "💡 Railway offers $5/month for private hosting"
        ;;
    3)
        echo ""
        echo "🟣 Heroku Deployment"
        echo "==================="
        echo "1. Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli"
        echo "2. Create Procfile:"
        echo 'web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0' > Procfile
        git add Procfile
        git commit -m "Add Procfile for Heroku"
        echo "3. Run: heroku create your-dashboard-name"
        echo "4. Run: git push heroku main"
        echo ""
        echo "✅ Procfile created and committed!"
        ;;
    4)
        echo ""
        echo "🎨 Render Deployment"
        echo "==================="
        echo "1. Go to: https://render.com"
        echo "2. Connect your GitHub repository"
        echo "3. Create a Web Service"
        echo "4. Build Command: pip install -r requirements.txt"
        echo "5. Start Command: streamlit run streamlit_app.py --server.port \$PORT --server.address 0.0.0.0"
        echo ""
        echo "💡 Render offers a free tier with limitations"
        ;;
    *)
        echo "❌ Invalid option. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🔐 Security Note:"
echo "Your dashboard uses file upload for data, so:"
echo "✅ No sensitive data is stored in the code"
echo "✅ Users upload their own analysis files"
echo "✅ Demo mode available for public sharing"
echo ""
echo "📊 Dashboard Features:"
echo "✅ Upload CSV + JSON analysis files"
echo "✅ Interactive visualizations"
echo "✅ Demo mode with sample data"
echo "✅ Mobile-responsive design"
echo "✅ Research insights based on DMCA framework"
echo ""
echo "🎉 Happy deploying! Your dashboard will help researchers"
echo "   explore anti-gender narrative patterns effectively."
