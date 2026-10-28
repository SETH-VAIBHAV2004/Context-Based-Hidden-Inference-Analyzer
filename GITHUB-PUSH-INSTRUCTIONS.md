# 🚀 GitHub Push Instructions

## Step-by-Step Guide to Push Your Project

---

## Method 1: Using Personal Access Token (Recommended for Windows)

### Step 1: Create GitHub Personal Access Token

1. **Token page opened automatically** or go to: https://github.com/settings/tokens/new

2. **Fill in:**
   - Description: `Context-Based-Inference-Analyzer`
   - Expiration: `90 days` (or your choice)
   - Scopes: ✅ Check **`repo`** (full control of private repositories)

3. **Click "Generate token"** at the bottom

4. **COPY THE TOKEN** - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **You can only see it once!** Copy it now!

### Step 2: Configure Git to Use Token

Open PowerShell in your project folder and run:

```powershell
cd "C:\Users\vaibhav\Desktop\CL PROJECT"

# Remove old remote (if exists)
git remote remove origin

# Add new remote with token embedded
git remote add origin https://ghp_YOUR_TOKEN_HERE@github.com/SETH-VAIBHAV2004/Context-Based-Hidden-Inference-Analyzer.git

# Push to GitHub
git push -u origin main
```

**Replace `ghp_YOUR_TOKEN_HERE` with your actual token!**

### Step 3: Verify Success

If successful, you'll see:
```
Enumerating objects: 100, done.
Counting objects: 100% (100/100), done.
Writing objects: 100% (100/100), done.
Total 100 (delta 0), reused 0 (delta 0)
To https://github.com/SETH-VAIBHAV2004/Context-Based-Hidden-Inference-Analyzer.git
 * [new branch]      main -> main
```

---

## Method 2: Using GitHub CLI (Easier but requires installation)

### Step 1: Install GitHub CLI

Download from: https://cli.github.com/

Or with winget:
```powershell
winget install --id GitHub.cli
```

### Step 2: Authenticate

```powershell
gh auth login
```

Follow the prompts:
- Account: `GitHub.com`
- Protocol: `HTTPS`
- Authenticate: `Login with a web browser`
- Copy the code and paste in browser

### Step 3: Push

```powershell
cd "C:\Users\vaibhav\Desktop\CL PROJECT"
git push -u origin main
```

---

## Method 3: Using GitHub Desktop (Visual)

### Step 1: Install GitHub Desktop

Download from: https://desktop.github.com/

### Step 2: Open Your Repository

1. Open GitHub Desktop
2. File → Add Local Repository
3. Choose: `C:\Users\vaibhav\Desktop\CL PROJECT`
4. Sign in to GitHub when prompted

### Step 3: Push

1. Click "Publish repository" or "Push origin"
2. Done!

---

## Troubleshooting

### Error: "Authentication failed"
→ Your token is wrong or expired. Create a new one.

### Error: "Repository not found"
→ Check the repository URL is correct.

### Error: "Permission denied"
→ Make sure your token has `repo` scope checked.

### Error: "Updates were rejected"
→ The remote has content. Use:
```powershell
git push -u origin main --force
```
⚠️ This will overwrite remote content!

---

## After Successful Push

Visit your repository:
https://github.com/SETH-VAIBHAV2004/Context-Based-Hidden-Inference-Analyzer

You should see:
- ✅ All your code files
- ✅ README.md displayed
- ✅ Documentation folder
- ✅ Frontend and backend folders
- ✅ Your commits in history

---

## What to Do Next

1. **Add Repository Description**
   - Click "About" gear icon
   - Add: "NLP Research Platform for Context-Aware Pragmatic Inference"
   - Add topics: `nlp`, `machine-learning`, `pragmatics`, `research`, `nextjs`, `fastapi`

2. **Check README Displays Correctly**
   - Should show your project overview on the main page

3. **Optional: Add a Banner Image**
   - Take a screenshot of your frontend
   - Add to README: `![Screenshot](screenshot.png)`

4. **Share Your Work!**
   - Add to your resume/portfolio
   - Share with classmates
   - Reference in presentations

---

## Security Notes

⚠️ **Never commit:**
- Personal Access Tokens
- API keys
- Passwords
- `.env` files with secrets
- The Circa dataset (too large)
- Trained models (too large)

✅ **These are already in .gitignore:**
- `backend/.env`
- `artifacts/`
- `data/circa.tsv`
- `node_modules/`
- `.venv/`

---

## Quick Reference

**Repository URL:**
https://github.com/SETH-VAIBHAV2004/Context-Based-Hidden-Inference-Analyzer

**Clone command (for others):**
```bash
git clone https://github.com/SETH-VAIBHAV2004/Context-Based-Hidden-Inference-Analyzer.git
```

**Update after local changes:**
```bash
git add .
git commit -m "Your commit message"
git push
```

---

Good luck! 🚀
