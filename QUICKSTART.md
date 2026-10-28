# 🚀 Quick Start Guide

Follow these steps to run your Pragmatic Inference Research Platform!

---

## Step 1: Open TWO PowerShell/Terminal Windows

You need to run backend and frontend simultaneously.

---

## Step 2: Start the Backend API

**In Terminal 1:**

```powershell
cd "C:\Users\vaibhav\Desktop\CL PROJECT"
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process...
```

✅ **Success Check:** Visit http://localhost:8000/health in your browser
- Should see: `{"status":"ok","service":"pragmatic-inference-api"}`

🔧 **Troubleshooting:**
- If Python error: Make sure you activated the virtual environment (`.venv\Scripts\activate`)
- If port 8000 busy: Close any other apps using port 8000

**Keep this terminal running!** ⚠️

---

## Step 3: Start the Frontend

**In Terminal 2 (NEW window):**

```powershell
cd "C:\Users\vaibhav\Desktop\CL PROJECT"
cd frontend
npm run dev
```

**Expected Output:**
```
▲ Next.js 16.4.3 (Turbopack)
- Local:        http://localhost:3000
✓ Ready in 956ms
```

✅ **Success Check:** Visit http://localhost:3000 in your browser
- Should see: Professional homepage with "Inferring the Unsaid"

🔧 **Troubleshooting:**
- If "npm: command not found": Restart your terminal or check Node.js installation
- If port 3000 busy: Close other apps or use `npm run dev -- -p 3001`

**Keep this terminal running too!** ⚠️

---

## Step 4: Train Your First Model

1. **Open browser:** http://localhost:3000/experiments

2. **Configure:**
   - Dataset: `Synthetic Fixture` (already available)
   - Model: `TF-IDF + Logistic Regression`
   - Context Window: `Previous 1 Turn`

3. **Click:** "Train Model" button

4. **Wait:** ~5 seconds for training to complete

5. **Check:** You should see:
   - ✅ Green success message
   - 📊 Metrics displayed (accuracy, F1 score, confusion matrix)

⚠️ **Note:** Metrics will be low (0-50%) because synthetic data is tiny (10 examples). This is expected!

---

## Step 5: Run Pragmatic Inference

1. **Open browser:** http://localhost:3000/workbench

2. **Enter a conversation:**
   ```
   Turn 0 - Speaker X: "Can you pick me up from the airport?"
   Turn 1 - Speaker Y: "I have a meeting at that time."
   ```

3. **Configure:**
   - Target Turn: `t1` (the answer)
   - Model: `TF-IDF + Logistic Regression`
   - Context Window: `Previous 1 Turn`

4. **Click:** "Run Pragmatic Inference"

5. **See results:**
   - 🎯 Predicted interpretation
   - 📊 Probability distribution
   - 💡 Context used by model
   - 📝 Evidence spans

---

## Step 6: Explore the Interface

### 📄 Pages to Check:

1. **Homepage** (`/`):
   - Research overview
   - System pipeline
   - Model status

2. **Workbench** (`/workbench`):
   - Interactive inference
   - Add/edit conversation turns
   - Try different models and contexts

3. **Experiments** (`/experiments`):
   - Train models
   - View metrics
   - Compare configurations

4. **Datasets** (`/datasets`):
   - Dataset information
   - Label distributions
   - Circa setup instructions

---

## Step 7: (Optional) Get Real Dataset

### To use the official Circa dataset:

1. **Download Circa:**
   - Visit: https://github.com/google-research-datasets/circa
   - Download: `circa-data-v1.0.tsv`
   - Save to: `C:\Users\vaibhav\Desktop\CL PROJECT\data\circa.tsv`

2. **Set environment variable:**

   **Option A: Temporary (this session only):**
   ```powershell
   $env:CIRCA_PATH="C:\Users\vaibhav\Desktop\CL PROJECT\data\circa.tsv"
   ```

   **Option B: Permanent (Windows):**
   - Search "Environment Variables" in Windows
   - Add new System Variable:
     - Name: `CIRCA_PATH`
     - Value: `C:\Users\vaibhav\Desktop\CL PROJECT\data\circa.tsv`

3. **Restart backend** (Ctrl+C then re-run uvicorn command)

4. **Train on Circa:**
   - Go to Experiments page
   - Select "Circa" dataset
   - Train model
   - See real research metrics! 🎓

---

## Step 8: Push to GitHub (Recommended)

1. **Create GitHub repo:**
   - Go to https://github.com/new
   - Name: `pragmatic-inference-research` (or your choice)
   - Make it **Public** or **Private**
   - Don't initialize with README (you already have one!)

2. **Push your code:**
   ```powershell
   cd "C:\Users\vaibhav\Desktop\CL PROJECT"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

3. **Verify:** Visit your GitHub repo to see all your code online! 🎉

---

## 🆘 Common Issues & Solutions

### Backend won't start:
```powershell
# Reinstall dependencies
cd backend
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

### Frontend won't start:
```powershell
# Reinstall dependencies
cd frontend
npm install
```

### "Module not found" errors:
- Make sure you're in the correct directory
- Make sure virtual environment is activated (backend)
- Try closing and reopening terminals

### Tests failing:
```powershell
cd backend
.\.venv\Scripts\activate
pytest -v
```
All 22 tests should pass!

---

## 📚 Next Steps for Your Project

### For Academic Use:
- ✅ Demonstrate the working application to your professor
- ✅ Show training on synthetic data
- ✅ Explain the TF-IDF + Logistic Regression implementation
- ✅ Discuss context window experiments
- ✅ Show the clean architecture (backend/frontend separation)

### For Further Development:
- 🔬 Download and use Circa dataset for real experiments
- 🤖 Implement transformer models (Milestone 7)
- 🔍 Add advanced evidence diagnostics (Milestone 5)
- 📊 Add more visualizations
- 🚀 Deploy to production (Vercel + Render)

---

## 💡 Pro Tips

1. **Keep both terminals open** while working
2. **Use Ctrl+C** to stop servers (backend or frontend)
3. **Check http://localhost:8000/docs** for API documentation
4. **Look at the test files** in `backend/tests/` to understand the code
5. **Read `docs/METHODOLOGY.md`** for research context
6. **Check `docs/ARCHITECTURE.md`** for system design

---

## ✅ Checklist

Before your presentation/demo:
- [ ] Backend running without errors
- [ ] Frontend accessible at localhost:3000
- [ ] Can train a model successfully
- [ ] Can run inference on sample conversations
- [ ] Understand what each page does
- [ ] Read README.md and know how to explain the project
- [ ] (Optional) Trained on Circa dataset
- [ ] (Optional) Pushed to GitHub

---

## 🎓 You're Ready!

Your professional NLP research platform is complete and functional!

**Need help?** Check the documentation:
- README.md - Project overview
- docs/ARCHITECTURE.md - System design
- docs/METHODOLOGY.md - Research approach
- docs/DEPLOYMENT.md - Deployment options

Good luck with your Computational Linguistics project! 🚀
