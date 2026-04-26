# Quick Start Guide - Mini-Survey Application

This guide will get you running the application in 5 minutes.

## Prerequisites

- Python 3.12+ (`python --version`)
- Node.js 18+ (`node --version`)
- npm 9+ or yarn (`npm --version`)

## 🚀 Quick Start (Two Terminals)

### Terminal 1 - Backend

```bash
cd /workspaces/otus-AI/backend
pip install -r requirements.txt
python main.py
```

**Expected Output:**
```
✓ Database (SQLite) tables created successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2 - Frontend

```bash
cd /workspaces/otus-AI/frontend
npm install
npm start
```

**Expected Output:**
```
webpack compiled successfully
Local:            http://localhost:3000
```

Browser will open automatically to http://localhost:3000

---

## ✅ Testing the Application

### 1. Test Backend API

```bash
# In a third terminal, test the API
curl http://localhost:8000/api/questions | python -m json.tool

# Test submitting answers
curl -X POST http://localhost:8000/api/answers \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_id": 1, "answer_value": "John"},
      {"question_id": 2, "answer_value": "Developer"},
      {"question_id": 3, "answer_value": "5+ лет"},
      {"question_id": 4, "answer_value": "Python"},
      {"question_id": 5, "answer_value": "Backend"}
    ]
  }'
```

### 2. Test Frontend UI

1. Go to http://localhost:3000 (should already be open)
2. Fill in all questions
3. Click "Отправить" (Submit)
4. See "Спасибо!" (Thank you!) message
5. Click "Заполнить анкету снова" to reset

---

## 📚 Documentation

For detailed information, see:
- **README.md** - Comprehensive documentation
- **prompts.md** - All AI prompts used
- **API Docs** - http://localhost:8000/docs (Swagger UI)

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

**ModuleNotFoundError:**
```bash
pip install -r requirements.txt  # Reinstall dependencies
```

### Frontend Issues

**Port 3000 already in use:**
```bash
lsof -i :3000
kill -9 <PID>
```

**Package errors:**
```bash
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**CORS errors in console:**
- Backend must be running on port 8000
- Frontend must be on port 3000
- Check backend logs for errors

---

## 🏗️ Project Structure

```
backend/
├── main.py              ← FastAPI app
├── models.py            ← Database models
├── routers/survey.py    ← API endpoints
└── survey.db            ← SQLite database (auto-created)

frontend/
├── src/
│   ├── components/      ← React components
│   ├── stores/          ← MobX store
│   └── api/             ← API client
└── node_modules/        ← npm packages
```

---

## 📝 Environment Variables

These are already configured by default:

**Backend** (`backend/.env`):
```env
DATABASE_URL=sqlite:///./survey.db
DEBUG=True
```

**Frontend** (`frontend/.env`):
```env
REACT_APP_API_URL=http://localhost:8000
```

To use PostgreSQL instead, modify `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mini_survey_db
```

---

## 🧪 Manual Verification

After starting both servers, verify:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] http://localhost:8000 responds (health check)
- [ ] http://localhost:3000 loads (survey form)
- [ ] Can fill and submit form
- [ ] "Спасибо!" message appears
- [ ] No errors in browser console (F12)

---

## 🔗 Useful Links

- **Swagger API Docs:** http://localhost:8000/docs
- **ReDoc API Docs:** http://localhost:8000/redoc
- **Frontend:** http://localhost:3000

---

Done! 🎉 Your survey application is running locally.

For more details, see **README.md** or **prompts.md**.
