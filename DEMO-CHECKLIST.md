# 🎬 Demo Checklist for Your Presentation

Use this checklist to prepare for demonstrating your project!

---

## 🔧 Pre-Demo Setup (30 minutes before)

### 1. Test Everything Works
- [ ] Open 2 terminals
- [ ] Start backend (see QUICKSTART.md Step 2)
- [ ] Start frontend (see QUICKSTART.md Step 3)
- [ ] Visit http://localhost:3000 - homepage loads
- [ ] Visit http://localhost:8000/docs - API docs load

### 2. Prepare Sample Conversations
Copy these to a text file for quick demo:

**Example 1: Indirect Refusal**
```
Speaker X: "Can you pick me up from the airport tonight?"
Speaker Y: "I have a very important meeting at that time."
```
Expected: Should predict "no" or conditional negative

**Example 2: Indirect Agreement**
```
Speaker X: "Do you want to join us for dinner?"
Speaker Y: "I love Italian food!"
```
Expected: Should predict "yes" or positive

**Example 3: Conditional Response**
```
Speaker X: "Can you help me move this weekend?"
Speaker Y: "I can help if it doesn't rain."
```
Expected: Should predict "yes_conditional"

### 3. Train a Model (One-Time Setup)
- [ ] Go to Experiments page
- [ ] Train TF-IDF model on synthetic data
- [ ] Wait for "Training Complete" message
- [ ] Verify metrics appear

---

## 🎯 Demo Flow (Suggested Order)

### 1. Homepage Introduction (2 minutes)
**Show:** http://localhost:3000

**Say:**
> "This is a research platform for pragmatic inference - understanding what speakers really mean beyond their literal words. The system analyzes multi-turn conversations to predict implied speaker intent."

**Point out:**
- Research hypothesis
- System pipeline (4 steps)
- Model list with implementation status

---

### 2. Dataset Explorer (2 minutes)
**Show:** http://localhost:3000/datasets

**Say:**
> "The platform uses the Circa dataset from EMNLP 2020 for pragmatic label prediction. Here you can see the dataset statistics, label distribution, and proper citation information."

**Point out:**
- Synthetic data is available (10 examples for testing)
- Circa is the real academic dataset
- License and attribution information
- Data validation features

---

### 3. Model Training (3 minutes)
**Show:** http://localhost:3000/experiments

**Say:**
> "Let me show you how the system trains machine learning models. I'll train a TF-IDF + Logistic Regression baseline."

**Do:**
1. Select "Synthetic Fixture" dataset
2. Select "TF-IDF + Logistic Regression" model
3. Select "Previous 1 Turn" context window
4. Click "Train Model"
5. Wait ~5 seconds

**Explain while training:**
> "The system is:
> - Loading the dataset
> - Creating group-aware splits to prevent data leakage
> - Training a TF-IDF vectorizer on the training data only
> - Training a logistic regression classifier
> - Evaluating on the held-out test set"

**Point out results:**
- Training/test set sizes
- Accuracy and Macro F1 scores
- Per-class precision, recall, F1
- Confusion matrix
- Warning that synthetic data has low metrics (expected!)

---

### 4. Pragmatic Inference Workbench (5 minutes) ⭐
**Show:** http://localhost:3000/workbench

**Say:**
> "This is the core of the platform - the Analysis Workbench where we can run pragmatic inference on actual conversations."

**Demo 1: Simple Case**
1. Clear existing conversation
2. Enter Example 1 (airport pickup)
3. Set target to last turn
4. Keep model as "TF-IDF + Logistic Regression"
5. Click "Run Pragmatic Inference"

**Point out:**
- Literal utterance vs. predicted interpretation
- Probability distribution across classes
- Context text that was fed to the model
- Evidence spans highlighting relevant parts
- Limitations section (transparency!)

**Demo 2: Context Comparison**
1. Add a situation: "X and Y are close friends"
2. Change context window to "Situation + Previous 1"
3. Run inference again
4. Show how probabilities change with more context

**Demo 3: Multi-turn Context**
1. Add more conversation turns
2. Show context window options (target only vs. multiple turns)
3. Explain the hypothesis: more context should help

---

### 5. Technical Implementation (2 minutes)
**Show:** Backend terminal or code editor

**Say:**
> "The system has a clean architecture with separation of concerns."

**Point out:**
- Python FastAPI backend for ML models
- Next.js React frontend for UI
- Pydantic schemas for data validation
- Automated tests (22 tests passing)
- Docker configuration for deployment

**Optional - Show a test:**
```powershell
cd backend
pytest tests/test_tfidf_baseline.py -v
```

---

### 6. Research Methodology (2 minutes)
**Show:** docs/METHODOLOGY.md (open in editor)

**Say:**
> "The project follows rigorous research practices."

**Point out:**
- Clear hypothesis statement (not claiming it's proven)
- Group-aware data splits prevent leakage
- Context window ablations for comparison
- No fabricated metrics - everything is measured
- Documented limitations

---

### 7. Future Work & Conclusion (1 minute)

**Say:**
> "Current status:
> - ✅ Working TF-IDF baseline with context experiments
> - ✅ Professional web interface
> - ✅ End-to-end pipeline from data to inference
> - ⚠️ Transformer models planned but not implemented
> - ⚠️ Evidence faithfulness evaluation planned
>
> The platform is ready for real experiments with the Circa dataset, and demonstrates clean software engineering for NLP research."

---

## 🎤 Key Talking Points

### What Makes This Project Good?

1. **Real Implementation**
   - Not a mockup or prototype
   - Actual ML models that train and predict
   - Real data validation and splitting

2. **Research Integrity**
   - No fake metrics
   - Clear distinction between hypothesis and results
   - Documented limitations
   - Proper dataset attribution

3. **Professional Quality**
   - Clean code architecture
   - Automated tests
   - Type hints and validation
   - Docker deployment ready
   - Comprehensive documentation

4. **Academic Rigor**
   - Based on EMNLP 2020 paper (Circa)
   - Group-aware splits (prevent leakage)
   - Ablation studies (context windows)
   - Evidence generation

---

## ❓ Anticipated Questions & Answers

### Q: "Why are the metrics so low?"
**A:** "The synthetic fixture has only 10 examples (6 train, 4 test) and is designed for testing the pipeline, not achieving high accuracy. With the full Circa dataset (~34,000 examples), we would see metrics in the 75-85% range similar to the original paper."

### Q: "What's novel about this approach?"
**A:** "The novelty is in the integration: combining multi-turn context with explainable evidence generation in a single pipeline. Most prior work either does classification without explanations, or only looks at single utterances."

### Q: "Why TF-IDF and not transformers?"
**A:** "TF-IDF + Logistic Regression is a strong interpretable baseline. Transformer models are planned (Milestone 7) but not implemented yet. Starting with baselines is standard research practice."

### Q: "How do you prevent data leakage?"
**A:** "I use group-aware splitting - examples that share the same question are kept together in the same split. This prevents the model from seeing similar questions at training and test time."

### Q: "Can this be deployed?"
**A:** "Yes! The project includes Docker configuration and deployment documentation. The backend can go to Render/Railway, frontend to Vercel. I've documented free tier and paid hosting options."

### Q: "How do you know the evidence is faithful?"
**A:** "Currently, evidence is rule-based (highlighting the target utterance). Milestone 5 plans sufficiency and necessity tests - removing evidence and checking if predictions change. This is an open research problem."

---

## 💡 Demo Tips

### DO:
- ✅ Practice the demo flow once before presenting
- ✅ Have terminals open and ready
- ✅ Keep a timer - stay within your time limit
- ✅ Show confidence in your implementation
- ✅ Be honest about what's implemented vs. planned
- ✅ Use the working features effectively

### DON'T:
- ❌ Claim you achieved novel research results (it's a hypothesis)
- ❌ Say "this is perfect" (acknowledge limitations)
- ❌ Try to implement new features during the demo
- ❌ Apologize for using synthetic data (it's for testing)
- ❌ Hide the code (show you understand it)

---

## 🆘 Emergency Backup Plan

If something breaks during demo:

### Plan A: Show API Docs
- Go to http://localhost:8000/docs
- Show the API endpoints
- Explain the request/response schemas

### Plan B: Show Tests
```powershell
cd backend
pytest -v
```
- All 22 tests passing shows working implementation

### Plan C: Show Code
- Open `backend/nlp/models/tfidf_lr.py`
- Walk through the training function
- Show you understand the implementation

### Plan D: Show Documentation
- Open README.md
- Show architecture diagram in docs/ARCHITECTURE.md
- Demonstrate planning and documentation skills

---

## ✅ Final Check 5 Minutes Before Demo

- [ ] Backend running (http://localhost:8000/health returns OK)
- [ ] Frontend running (http://localhost:3000 loads)
- [ ] Model is trained (check Experiments page)
- [ ] Sample conversations ready to paste
- [ ] Browser tabs open: homepage, workbench, experiments, datasets
- [ ] Terminals visible and clean (not too many error messages)
- [ ] You've read this checklist!
- [ ] Deep breath - you got this! 💪

---

## 🎓 You're Ready to Shine!

Remember: This is a **professional, working implementation** of an NLP research platform. You built something real, not just slides. Be proud and confident!

Good luck! 🚀
