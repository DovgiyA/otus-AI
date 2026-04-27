---
name: fullstack-survey-app
description: "WORKFLOW SKILL — Build minimal full-stack survey/form applications with structured methodology. USE WHEN: creating data collection apps, feedback forms, questionnaires with backend persistence and interactive frontend. Includes: requirements clarification, architecture planning, backend (FastAPI), frontend (React+MobX), database setup, integration testing, comprehensive documentation, and prompt archival. Delivers production-ready app in 5 phases with verified testing."
---

# Full-Stack Survey Application Builder

## Overview

This skill provides a **structured, repeatable methodology** for building full-stack data collection applications (surveys, forms, questionnaires) from concept to delivery.

**Result**: Minimal but complete full-stack application with:
- RESTful backend API (FastAPI)
- Interactive frontend (React + MobX)
- Persistent database (SQLite default, PostgreSQL ready)
- Comprehensive documentation
- All development prompts archived

**Time**: ~2-3 hours for a 5-question survey app  
**Scope**: Single developer; no Docker required for local development

---

## When to Use This Skill

✅ **Use when:**
- Building survey, form, or questionnaire application
- Need to collect user responses with backend persistence
- Want mixed question types (text input, radio buttons, checkboxes)
- Creating minimum viable product (MVP) for data collection
- Need full source code control and documented development process

❌ **Don't use for:**
- Simple frontend-only forms (no backend)
- Existing frameworks' form builders (e.g., Formik, React Hook Form)
- High-concurrency applications with complex business logic
- AI/ML model inference pipelines
- Real-time collaborative editing

---

## Architecture Decision Tree

```
START
  ↓
[Database Persistence?]
  ├─ No → Use memory/localStorage (STOP - not this skill)
  ├─ Yes → [SQLite or PostgreSQL?]
           ├─ SQLite (dev) → Works out of box ✓
           └─ PostgreSQL → Need local PG setup
  ↓
[Question Types?]
  ├─ Text only → Simple
  ├─ Radio/Checkboxes → Mixed (this skill)
  └─ Complex (conditionals, file upload, etc.) → Extend skill
  ↓
[Frontend Complexity?]
  ├─ Minimal (pure React hooks) → Simpler
  ├─ Forms with state mgmt (MobX/Redux) ← THIS SKILL
  └─ Advanced (real-time sync, offline-first) → Extend skill
  ↓
[Deployment?]
  ├─ Local only → Docker optional
  ├─ Cloud (AWS/Heroku) → Use Docker (add to Phase 1)
  └─ Serverless → Different architecture
```

---

## 5-Phase Implementation Workflow

### Phase 1: Planning & Architecture

**Goal**: Clarify requirements, design system, set dependencies

**Steps**:
1. **Clarify Requirements** (interact with user)
   - How many questions? (3-10 for MVP)
   - Question types? (text, radio, checkboxes, mixed?)
   - Data persistence? (SQLite/PostgreSQL/memory?)
   - View constraint? (single page form, multi-step wizard?)

2. **Create Architecture Plan**
   - Project structure (monorepo with /backend, /frontend)
   - Technology stack (FastAPI, React, MobX, SQLite)
   - Database schema sketch (Question, Answer tables)
   - Data flow diagram (browser → API → DB)

3. **Generate Checklist**
   - Technology versions (Python 3.12+, Node 18+)
   - Required files checklist (backend, frontend, docs)
   - Verification steps (unit, integration, E2E)

**Deliverables**: 
- Architecture plan document
- Tech stack selection
- Implementation checklist
- Project structure diagram

**Tools**: 
- `vscode_askQuestions` to clarify requirements
- `renderMermaidDiagram` for architecture diagrams

---

### Phase 2: Backend Setup

**Goal**: Create FastAPI application with database models and API endpoints

**Steps**:
1. **Initialize Backend**
   - Create `/backend` directory structure
   - Create `config.py` (settings, env vars, multi-DB support)
   - Create `requirements.txt` with dependencies

2. **Database Layer**
   - Create `database.py` (SQLAlchemy engine, session factory)
   - Create `models.py` (Question, Answer ORM models)
   - Create `schemas.py` (Pydantic request/response DTOs)

3. **API Routes**
   - Create `routers/survey.py`
     - `GET /api/questions` → return list of questions
     - `POST /api/answers` → accept and save answers
   - Implement question seeding logic
   - Add error handling and validation

4. **Application Entry Point**
   - Create `main.py` with FastAPI app
   - Add CORS middleware for frontend
   - Register routes and health checks
   - Configure database initialization

5. **Test Backend**
   - Start `python main.py` → should run without errors
   - Test `GET /api/questions` → returns JSON
   - Test `POST /api/answers` → accepts POST request
   - Verify database created with tables

**Deliverables**:
- FastAPI application running on :8000
- SQLite database with Question + Answer tables
- Two working API endpoints verified via curl

**Decision Points**:
- | PostgreSQL or SQLite? | → SQLite (easier for local dev, works immediately) |
- | Question seeding strategy? | → Auto-seed on startup if DB empty |
- | CORS origins? | → localhost:3000 for frontend dev |

---

### Phase 3: Frontend Setup

**Goal**: Create React interface with MobX state management

**Steps**:
1. **Initialize Frontend**
   - Create `/frontend` directory
   - Create `package.json` with dependencies (React, MobX, Axios)
   - Create `public/index.html` entry point
   - Create `.env` (API_URL=http://localhost:8000)

2. **State Management (MobX)**
   - Create `src/stores/SurveyStore.js`
     - Observable: questions, answers, isLoading, isSubmitted
     - Actions: fetchQuestions(), setAnswer(), submitAnswers(), reset()
   - Use `makeAutoObservable()` for automatic reactive bindings

3. **API Client**
   - Create `src/api/surveyApi.js`
   - Configure Axios with base URL
   - Implement getQuestions() and postAnswers() functions

4. **React Components**
   - Create `src/App.jsx` (root component)
   - Create `src/components/SurveyForm.jsx` (observer wrapper, form logic)
   - Create `src/components/QuestionField.jsx` (reusable question renderer)
     - Conditional: text input vs radio buttons
   - Create `src/index.js` (React initialization)

5. **Styling**
   - Create `src/styles/App.css` (form layout, buttons, animations)
   - Create `src/index.css` (global styles, gradient background)
   - Make responsive (mobile breakpoints)

6. **Test Frontend**
   - `npm install` → no errors
   - `npm start` → browser opens to localhost:3000
   - Form loads with questions visible
   - Can interact with form fields
   - No console errors

**Deliverables**:
- React app running on :3000
- Survey form visible
- Form fields interactive
- MobX store managing state

**Decision Points**:
- | Global MobX store or component state? | → Global (simpler for forms, single responsibility) |
- | Question type rendering? | → Conditional (type="text" vs type="radio") |
- | Submit validation? | → Validate all fields filled before POST |

---

### Phase 4: Integration & Testing

**Goal**: Verify end-to-end workflow and data persistence

**Steps**:
1. **Start Both Servers**
   ```bash
   Terminal 1: cd backend && python main.py
   Terminal 2: cd frontend && npm start
   ```

2. **Manual Testing**
   - Load http://localhost:3000
   - Verify questions display correctly
   - Fill in all form fields
   - Submit form
   - Verify "Thank you!" message appears
   - Check no console errors (F12 → Console)

3. **Database Verification**
   - Query SQLite: `SELECT * FROM answers;`
   - Verify submitted answers present with timestamps
   - Verify question_id foreign keys intact

4. **API Testing** (with curl)
   ```bash
   curl http://localhost:8000/api/questions | jq
   curl -X POST http://localhost:8000/api/answers \
     -H "Content-Type: application/json" \
     -d '{"answers": [...]}'
   ```

5. **Create Integration Test Script**
   - Check backend running (:8000)
   - Check frontend running (:3000)
   - Verify API responses valid JSON
   - Verify CORS headers correct
   - Validate database connectivity

**Deliverables**:
- Full end-to-end workflow verified
- Integration test script (Python with requests)
- Manual testing checklist completed
- No errors in browser console or backend logs

**Decision Points**:
- | Success state UI? | → Show "Спасибо!" message, offer reset button |
- | Error cases to handle? | → Network errors, validation failures, invalid question IDs |

---

### Phase 5: Documentation & Archival

**Goal**: Create comprehensive documentation and archive all development prompts

**Steps**:
1. **README.md** (550+ lines)
   - Project overview, features, tech stack
   - Step-by-step setup (backend, frontend, database)
   - API endpoint documentation with examples
   - Database schema and entity relationships
   - Troubleshooting guide (ports, dependencies, CORS)
   - Production deployment considerations
   - Architecture explanation (component hierarchy, state flow)

2. **QUICKSTART.md** (200+ lines)
   - 5-minute setup guide
   - Prerequisites checklist
   - Two-terminal startup commands
   - Manual test procedures
   - Common error solutions

3. **prompts.md** (500+ lines)
   - Document every AI prompt used
   - Organize by phase (Planning, Backend, Frontend, Docs)
   - For each prompt:
     - Request (what was asked)
     - Completion summary (what was delivered)
     - Code highlights
   - Include decision rationale
   - Suggest future enhancements

4. **COMPLETION.md**
   - Project completion summary
   - Requirements checklist (all ✓)
   - Feature highlights
   - Test results (all passing)
   - Statistics (files, lines of code, prompts used)

5. **Git & .gitignore**
   - Commit all source code
   - Exclude: node_modules/, __pycache__/, *.db, .env
   - .gitignore template in-place

**Deliverables**:
- 4 comprehensive documentation files
- All prompts archived with context
- Git repository ready for sharing
- COMPLETION checklist signed off

---

## File Checklist

### Backend (8 files)
- [ ] `backend/main.py` — FastAPI app, routes, initialization
- [ ] `backend/config.py` — Settings, environment variables
- [ ] `backend/database.py` — SQLAlchemy setup (engine, session)
- [ ] `backend/models.py` — ORM models (Question, Answer)
- [ ] `backend/schemas.py` — Pydantic validators
- [ ] `backend/routers/survey.py` — API endpoints
- [ ] `backend/requirements.txt` — Dependencies
- [ ] `backend/.env` — Config file (DATABASE_URL, DEBUG)

### Frontend (10 files)
- [ ] `frontend/package.json` — npm dependencies
- [ ] `frontend/.env` — API_URL
- [ ] `frontend/public/index.html` — HTML entry
- [ ] `frontend/src/index.js` — React init
- [ ] `frontend/src/App.jsx` — Root component
- [ ] `frontend/src/components/SurveyForm.jsx` — Main form with observer
- [ ] `frontend/src/components/QuestionField.jsx` — Question renderer
- [ ] `frontend/src/stores/SurveyStore.js` — MobX store
- [ ] `frontend/src/api/surveyApi.js` — Axios wrapper
- [ ] `frontend/src/styles/App.css` — Form styling

### Documentation (4+ files)
- [ ] `README.md` — Comprehensive guide
- [ ] `QUICKSTART.md` — 5-minute setup
- [ ] `prompts.md` — All prompts archived
- [ ] `COMPLETION.md` — Project summary
- [ ] `.gitignore` — Git exclusions
- [ ] `test_integration.py` — Integration test suite

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Database | SQLite (default) | No setup; works immediately; can swap to PostgreSQL later |
| State Management | MobX + Global Store | Simpler than Redux; fewer files; perfect for forms |
| Question Types | Mixed (text + radio) | Shows framework extensibility; easy to add more types |
| Project Layout | Monorepo (/backend, /frontend) | Single repo, shared docs, easier deployment |
| Frontend Framework | React + Hooks | Industry standard; large ecosystem; no build complexity |
| API Style | RESTful (simple GET/POST) | Predictable; minimal CRUD; easy to extend |
| Styling | Plain CSS (no Tailwind) | No dependency overhead; works in all browsers |
| Database Init | Auto-create on startup | Zero setup friction for local development |
| Validation | Pydantic + client-side checks | Both backend + frontend for UX |

---

## Quality Gates & Verification

**Before Phase 2 complete:**
- ✓ Backend starts without errors
- ✓ `GET /api/questions` returns valid JSON array
- ✓ `POST /api/answers` accepts JSON, returns success

**Before Phase 3 complete:**
- ✓ Frontend builds without errors
- ✓ React component tree renders without crashes
- ✓ MobX store actions fire without exceptions
- ✓ No console errors in browser

**Before Phase 4 complete:**
- ✓ Full workflow: load form → fill → submit → success
- ✓ Answers saved in database with correct question_id
- ✓ No CORS errors
- ✓ No network errors
- ✓ All integration tests passing

**Before Phase 5 complete:**
- ✓ README complete and accurate
- ✓ All prompts documented
- ✓ Git repository ready
- ✓ COMPLETION checklist signed off

---

## Troubleshooting Decision Tree

```
Problem: Backend won't start
├─ Port 8000 in use? → Kill process (lsof -i :8000)
├─ ModuleNotFoundError? → pip install -r requirements.txt
├─ Database error? → Delete survey.db, restart
└─ Config error? → Check DATABASE_URL in .env

Problem: Frontend won't load
├─ Port 3000 in use? → Kill process (lsof -i :3000)
├─ npm errors? → rm -rf node_modules && npm install
├─ Build errors? → Check Node version (18+)
└─ Module not found? → npm install (missing dependency)

Problem: Form doesn't submit
├─ CORS error in console? → Backend must be running
├─ API returns 404? → Check /api/answers spelling
├─ No success message? → Check browser console for JS errors
└─ Validation fails? → Verify all questions have answers

Problem: Data not saved
├─ Database error in backend log? → Check DATABASE_URL
├─ Foreign key error? → Verify question_id exists
├─ DB file not created? → Check file permissions in /backend
└─ SQLite locked? → Close other connections, restart
```

---

## Extension Points

**To extend this skill:**

1. **Add Authentication**
   - JWT tokens in FastAPI
   - Protected endpoints
   - User identity in answers

2. **Add Question Types**
   - Checkboxes (multiple select)
   - Date pickers
   - File uploads
   - Conditional logic (show Q5 if Q3="Option B")

3. **Add Analytics**
   - Response statistics dashboard
   - Charts (pie, bar, histogram)
   - Export to CSV/PDF

4. **Add Admin Panel**
   - Create/edit surveys
   - View responses
   - Delete answers
   - User management

5. **Dockerize**
   - Add Dockerfile for backend
   - Add docker-compose.yml
   - Ready for cloud deployment

6. **Add Real-Time**
   - WebSocket for live response count
   - Push notifications
   - Multi-user sync

---

## Example Prompts to Trigger This Skill

> "I need to build a customer feedback survey with questions about product satisfaction and features. Tech: Python backend, React frontend, SQLite database. Can you create a working MVP?"

> "Create a minimal survey tool that stores responses in a database. Need text and radio button questions, responsive UI, and documentation."

> "I want a data collection app for a questionnaire. Should have backend API, frontend form, and database persistence. Full-stack, local development."

---

## Related Skills & Next Steps

**After completing this skill:**
- **Admin Panel**: Create backend + frontend for survey management
- **Analytics**: Add dashboards with response statistics
- **Deployment**: Docker, GitHub Actions CI/CD, cloud hosting
- **Authentication**: JWT, user accounts, survey ownership
- **Advanced Forms**: Conditional branching, multi-step wizards

**See also:**
- `.github/prompts/fullstack-scaffold.prompt.md` — Parametrized version
- `COMPLETION.md` — Project completion checklist
- `prompts.md` — All archived development prompts

---

**Last Updated**: April 26, 2026  
**Status**: ✅ Skill documented and tested with Mini-Survey application  
**Python Version**: 3.12+  
**Node Version**: 18+ LTS
