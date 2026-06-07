# 🚀 Quick Start Guide

## Running Locally (Fastest Way)

### Step 1: Open Terminal
```bash
cd c:\Users\Admin\Desktop\coding\ML\ch_1
```

### Step 2: Install Dependencies (First time only)
```bash
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
streamlit run app.py
```

### Step 4: Open in Browser
- The app will automatically open at `http://localhost:8501`
- Or manually navigate to that URL

---

## 🌐 Deploy to Streamlit Cloud (Free & Easy)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file to `app.py`
6. Click "Deploy"

**Done!** Your app is live on the internet 🎉

---

## 📦 Deploy to Heroku (Requires Account)

### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create App
```bash
heroku create your-unique-app-name
```

### Step 4: Deploy
```bash
git push heroku main
```

### Step 5: Open App
```bash
heroku open
```

---

## 🔗 Deploy to AWS

### Option A: EC2 Instance
1. Launch EC2 instance (Ubuntu)
2. Install Python and dependencies
3. Clone repository
4. Run: `streamlit run app.py --server.port=80`

### Option B: AWS Lambda + API Gateway
- Requires serverless configuration
- More complex setup

---

## 💾 Tips

- Keep `insurance.csv` in the same folder as `app.py`
- The model trains on first run (takes ~10 seconds)
- Subsequent runs load cached model (instant)
- Model and scaler are saved as `.pkl` files

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Run: `pip install -r requirements.txt` |
| CSV file not found | Copy `insurance.csv` to the app directory |
| Port 8501 in use | Run: `streamlit run app.py --server.port=8502` |
| App not opening | Manually go to `http://localhost:8501` |

---

## 📞 Get Help

- Streamlit Docs: https://docs.streamlit.io
- Common Issues: https://docs.streamlit.io/library/troubleshooting
