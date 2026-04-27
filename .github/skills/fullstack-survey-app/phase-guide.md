# Phase Quick Reference Guide

Use this one-page reference during implementation.

## Phase 1: Planning & Architecture (30 min)

**Goal**: Clarify requirements, plan system

**Clarify with user:**
- Number of questions? (recommend: 3-10)
- Types of questions? (text, radio, checkboxes?)
- Database? (SQLite: no setup; PostgreSQL: need local PG)
- Single-page form or multi-step?
- Any authentication needed?

**Create document with:**
- Architecture diagram (monorepo)
- Tech stack list (Python 3.12+, Node 18+, React, MobX, FastAPI)
- Database schema (2 tables: questions, answers)
- Data flow (browser → API → DB)
- File checklist (18 files total)

**Success gate:**
- Architecture plan approved ✓
- Tech stack confirmed ✓
- File structure understood ✓

---

## Phase 2: Backend (45 min)

**Tech**: FastAPI, SQLAlchemy, Pydantic

**Step 1: Setup**
```bash
mkdir backend && cd backend
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
```

**Step 2: Core files**
- `config.py` — Settings, DATABASE_URL, CORS_ORIGINS
- `database.py` — SQLAlchemy engine, SessionLocal, Base
- `models.py` — Question (id, text, type, options, order), Answer (id, question_id, answer_value, created_at)
- `schemas.py` — Pydantic: QuestionResponse, AnswersRequest, SuccessResponse

**Step 3: Routes**
- `routers/survey.py` — GET /api/questions, POST /api/answers
  - Seed questions if DB empty
  - Validate request payloads
  - Handle errors

**Step 4: Entry point**
- `main.py` — FastAPI app, CORS middleware, database init

**Step 5: Test**
```bash
python main.py  # Should start with "✓ Database created"
curl http://localhost:8000/api/questions | jq  # Should return JSON
```

**Success gate:**
- Backend runs without errors ✓
- GET /api/questions returns valid JSON ✓
- POST /api/answers accepts JSON ✓

---

## Phase 3: Frontend (60 min)

**Tech**: React, MobX, Axios

**Step 1: Setup**
```bash
npx create-react-app frontend --template cra-template
cd frontend
npm install mobx mobx-react-lite axios
```

**Step 2: State Management**
- `src/stores/SurveyStore.js` (MobX)
  - Observable: questions, answers, isLoading, isSubmitted
  - Actions: fetchQuestions(), setAnswer(), submitAnswers(), reset()

**Step 3: API Client**
- `src/api/surveyApi.js` (Axios)
  - getQuestions() — GET /api/questions
  - postAnswers(payload) — POST /api/answers

**Step 4: Components**
- `src/index.js` — React init
- `src/App.jsx` — Root
- `src/components/SurveyForm.jsx` — Main form with observer()
- `src/components/QuestionField.jsx` — Question renderer (text vs radio)

**Step 5: Styling**
- `src/styles/App.css` — Form layout, buttons, animations
- `src/index.css` — Global (gradient bg, flex centering)

**Step 6: Test**
```bash
npm start  # Browser opens to localhost:3000
# Form should be visible and interactive
```

**Success gate:**
- Frontend builds ✓
- Form renders without errors ✓
- Can interact with form fields ✓

---

## Phase 4: Integration (30 min)

**Goal**: Verify end-to-end workflow

**Start servers:**
```bash
Terminal 1: cd backend && python main.py
Terminal 2: cd frontend && npm start
```

**Manual tests:**
1. Load http://localhost:3000
2. Fill in all questions
3. Click "Отправить"
4. Verify "Спасибо!" message
5. Check database: `SELECT * FROM answers;`

**API tests:**
```bash
curl http://localhost:8000/api/questions | jq
curl -X POST http://localhost:8000/api/answers \
  -H "Content-Type: application/json" \
  -d '{"answers": [{"question_id": 1, "answer_value": "Test"}]}'
```

**Success gate:**
- Full workflow works ✓
- Answers saved to DB ✓
- No console errors ✓
- No CORS errors ✓

---

## Phase 5: Documentation (45 min)

**Create 4 files:**

1. **README.md** (550+ lines)
   - Overview, features, tech stack
   - Setup instructions (backend, frontend, DB)
   - API documentation with examples
   - Database schema
   - Troubleshooting guide
   - Architecture diagrams

2. **QUICKSTART.md** (200+ lines)
   - 5-minute setup
   - Prerequisites
   - Command-by-command startup
   - Testing procedures

3. **prompts.md** (500+ lines)
   - Document every AI prompt used
   - Organize by phase
   - For each: request, completion, code highlights

4. **COMPLETION.md**
   - Checklist (all ✓)
   - Feature list
   - Test results
   - Statistics

**Success gate:**
- README complete ✓
- All prompts archived ✓
- QUICKSTART tested ✓
- COMPLETION signed off ✓

---

## File Checklist

```
Backend (8 files):
☐ main.py              FastAPI entry point
☐ config.py            Settings, env vars
☐ database.py          SQLAlchemy setup
☐ models.py            ORM models
☐ schemas.py           Pydantic validators
☐ routers/survey.py    API routes
☐ requirements.txt     Dependencies
☐ .env                 Config file

Frontend (10 files):
☐ package.json         npm dependencies
☐ .env                 REACT_APP_API_URL
☐ public/index.html    HTML entry
☐ src/index.js         React init
☐ src/App.jsx          Root component
☐ src/components/SurveyForm.jsx      Main form
☐ src/components/QuestionField.jsx   Question renderer
☐ src/stores/SurveyStore.js          MobX store
☐ src/api/surveyApi.js               Axios client
☐ src/styles/App.css                 Form styling

Docs (4 files):
☐ README.md            Comprehensive guide
☐ QUICKSTART.md        5-minute setup
☐ prompts.md           All prompts archived
☐ COMPLETION.md        Project summary
```

---

## Verification Checklist

**Before Phase 2:**
- [ ] Python 3.12+ installed
- [ ] Project structure created
- [ ] Tech stack decided

**Before Phase 3:**
- [ ] Backend starts without errors
- [ ] `GET /api/questions` returns JSON
- [ ] `POST /api/answers` accepts requests

**Before Phase 4:**
- [ ] Frontend builds without errors
- [ ] React components render
- [ ] Form fields are interactive
- [ ] MobX store initialized

**Before Phase 5:**
- [ ] Full workflow: load → fill → submit → success
- [ ] Answers saved in database
- [ ] No CORS errors
- [ ] All integration tests pass

**Before Final Delivery:**
- [ ] README completed
- [ ] All prompts documented
- [ ] Git repository ready
- [ ] COMPLETION checklist done ✓

---

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `Port 8000 already in use` | `lsof -i :8000 \| kill -9 <PID>` |
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `CORS error in console` | Verify backend running, check CORS_ORIGINS |
| `npm ERR!` | `rm -rf node_modules && npm install --legacy-peer-deps` |
| `Database locked` | Close other connections, delete survey.db |
| `Form won't submit` | Check browser console (F12), check backend logs |

---

**Time Estimate**: 2-3 hours total  
**Questions per app**: 3-10 (MVP)  
**Files to create**: 18-20  
**Total lines of code**: 2,000+
