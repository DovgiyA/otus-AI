# Mini-Survey Application (Мини-анкета)

A minimal full-stack survey application built with FastAPI + PostgreSQL/SQLite backend and React + MobX frontend. Users can load survey questions, fill in answers, and submit responses to the backend.

## 🎯 Project Overview

This is a full-stack web application demonstrating modern development practices:

- **Backend**: Python FastAPI with SQLAlchemy ORM, PostgreSQL/SQLite database
- **Frontend**: React with MobX state management, modern UI
- **Architecture**: RESTful API, component-based frontend, centralized state management
- **Deployment**: Local native setup (no Docker required)

### Key Features

✅ Load survey questions from backend API  
✅ Display mixed question types (text input + radio buttons)  
✅ Global state management with MobX  
✅ Submit answers and persist to database  
✅ Show "Thank you!" confirmation message  
✅ Responsive, modern UI with gradient styling  
✅ Real-time form validation  
✅ Progress indicator (X/Y questions filled)  
✅ Error handling and loading states  

---

## 📋 Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0
- **ORM**: SQLAlchemy 2.0.23
- **Database**: SQLite (default) or PostgreSQL
- **Database Driver**: psycopg2-binary 2.9.9
- **Validation**: Pydantic 2.5.0
- **Configuration**: python-dotenv, pydantic-settings

### Frontend
- **Library**: React 18.2.0
- **State Management**: MobX 6.10.2 + mobx-react-lite 4.0.5
- **HTTP Client**: Axios 1.6.2
- **Build Tools**: Create React App (react-scripts 5.0.1)

### Tools
- **Python**: 3.12+
- **Node.js**: 18+ (LTS)
- **Package Manager**: npm 9+ or yarn 4+

---

## 🚀 Quick Start

### Prerequisites

Ensure you have installed:
- Python 3.12 or higher
- Node.js 18+ (LTS) and npm 9+
- Git

### Step 1: Clone Repository

```bash
cd /workspaces/otus-AI
git config user.email "you@example.com"
git config user.name "Your Name"
```

### Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional):**
   ```bash
   cat .env
   # DATABASE_URL is set to SQLite by default: sqlite:///./survey.db
   # For PostgreSQL: DATABASE_URL=postgresql://user:pass@localhost:5432/mini_survey_db
   ```

4. **Start backend server:**
   ```bash
   python main.py
   ```
   
   Expected output:
   ```
   ✓ Database (SQLite) tables created successfully
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

5. **Test backend in another terminal:**
   ```bash
   curl http://localhost:8000/api/questions
   ```

### Step 3: Frontend Setup

1. **In a new terminal, navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Verify environment configuration:**
   ```bash
   cat .env
   # REACT_APP_API_URL=http://localhost:8000
   ```

4. **Start development server:**
   ```bash
   npm start
   ```
   
   The browser should automatically open at `http://localhost:3000`

5. **Expected behavior:**
   - Survey form loads with 5 questions
   - Mix of text input and radio button questions
   - Fill in answers and click "Отправить" (Submit)
   - See "Спасибо!" (Thank you!) message after submission

---

## 📚 API Documentation

### Backend Endpoints

#### 1. GET `/api/questions`

Returns list of survey questions.

**Response:**
```json
[
  {
    "id": 1,
    "text": "Какое ваше имя?",
    "type": "text",
    "options": null,
    "order": 1
  },
  {
    "id": 2,
    "text": "Какова ваша должность?",
    "type": "radio",
    "options": ["Developer", "Designer", "Manager", "Other"],
    "order": 2
  }
]
```

**Question Types:**
- `"text"`: User enters free-form text
- `"radio"`: User selects one option from `options` array

---

#### 2. POST `/api/answers`

Accepts and saves user survey answers.

**Request:**
```json
{
  "answers": [
    {"question_id": 1, "answer_value": "John Doe"},
    {"question_id": 2, "answer_value": "Developer"},
    {"question_id": 3, "answer_value": "Python, JavaScript"},
    {"question_id": 4, "answer_value": "Backend"},
    {"question_id": 5, "answer_value": "5+ лет"}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully saved 5 answers",
  "data": {
    "count": 5
  }
}
```

---

#### 3. GET `/` (Health Check)

Basic health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Mini Survey API is running",
  "docs": "/docs"
}
```

---

#### Interactive API Docs

When running locally, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🏗️ Project Structure

```
otus-AI/
├── README.md                          ← You are here
├── prompts.md                         ← All AI prompts used during development
├── .gitignore
│
├── backend/
│   ├── main.py                        ← FastAPI app entry point
│   ├── config.py                      ← Settings & environment config
│   ├── database.py                    ← SQLAlchemy setup, session management
│   ├── models.py                      ← SQLAlchemy ORM models (Question, Answer)
│   ├── schemas.py                     ← Pydantic request/response validators
│   ├── .env                           ← Environment variables (default: SQLite)
│   ├── requirements.txt               ← Python dependencies
│   ├── setup_db.py                    ← Database initialization helper
│   ├── survey.db                      ← SQLite database (auto-created)
│   └── routers/
│       ├── __init__.py
│       └── survey.py                  ← API routes (/questions, /answers)
│
└── frontend/
    ├── package.json                   ← npm dependencies
    ├── .env                           ← React env vars (API_URL)
    ├── public/
    │   └── index.html                 ← HTML entry point
    ├── src/
    │   ├── index.js                   ← React app initialization
    │   ├── App.jsx                    ← Root component
    │   ├── stores/
    │   │   └── SurveyStore.js         ← MobX store (questions, answers, actions)
    │   ├── components/
    │   │   ├── SurveyForm.jsx         ← Main form component (with observer)
    │   │   └── QuestionField.jsx      ← Reusable question renderer
    │   ├── api/
    │   │   └── surveyApi.js           ← Axios client for API calls
    │   ├── styles/
    │   │   └── App.css                ← Form styling (gradient, animations)
    │   └── index.css                  ← Global styles
    └── node_modules/                  ← npm packages (auto-created)
```

---

## 🎨 Frontend Architecture

### Component Hierarchy

```
App
└── SurveyForm (observer)
    ├── QuestionField (x5 questions)
    │   ├── Text Input (for "text" type)
    │   └── Radio Group (for "radio" type)
    ├── Submit Button
    ├── Clear Button
    └── Progress Indicator
```

### State Management (MobX)

**SurveyStore** manages:
- `questions`: Array of question objects
- `answers`: Object mapping `{questionId: answerValue}`
- `isLoading`: Boolean for loading states
- `isSubmitted`: Boolean for success state
- `error`: String for error messages

**Actions:**
- `fetchQuestions()`: Load from `/api/questions`
- `setAnswer(questionId, value)`: Update answer
- `submitAnswers()`: POST to `/api/answers`
- `reset()`: Clear form

---

## 🗄️ Database Schema

### Questions Table
```sql
CREATE TABLE questions (
  id SERIAL PRIMARY KEY,
  text VARCHAR(500) NOT NULL,
  type VARCHAR(50) NOT NULL,        -- "text" or "radio"
  options JSON,                     -- ["Option 1", "Option 2", ...] for radio
  order INT DEFAULT 0
);
```

### Answers Table
```sql
CREATE TABLE answers (
  id SERIAL PRIMARY KEY,
  question_id INT NOT NULL REFERENCES questions(id),
  answer_value VARCHAR(1000) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Initial Questions (Seeded on Startup)

| ID | Question (RU) | Type | Options |
|----|---|---|---|
| 1 | Какое ваше имя? | text | — |
| 2 | Какова ваша должность? | radio | Developer, Designer, Manager, Other |
| 3 | Сколько лет вы работаете в IT? | radio | < 1 года, 1-3 года, 3-5 лет, 5+ лет |
| 4 | Какие языки программирования вы используете? | text | — |
| 5 | Какова ваша основная категория опыта? | radio | Backend, Frontend, Full-Stack, DevOps, Data Science |

---

## 🔄 Full Workflow Example

### 1. Browser Opens Frontend
```
http://localhost:3000 → SurveyForm loads
↓
SurveyStore.fetchQuestions() called
↓
GET http://localhost:8000/api/questions
↓
Questions displayed in UI
```

### 2. User Fills Form
```
User enters text answers and selects radio options
↓
Each change: SurveyStore.setAnswer(questionId, value)
↓
Progress indicator updates (e.g., "4/5 вопросов заполнено")
```

### 3. User Submits
```
Submit button clicked
↓
SurveyStore.submitAnswers() called
↓
POST http://localhost:8000/api/answers
{
  "answers": [
    {"question_id": 1, "answer_value": "Alice"},
    {"question_id": 2, "answer_value": "Developer"},
    ...
  ]
}
↓
Backend saves to database
↓
Response: {"success": true, "message": "..."}
↓
Frontend shows "🎉 Спасибо!"
↓
User can click "Заполнить анкету снова" to reset
```

### 4. Data Persistence
```sql
SELECT * FROM answers;
-- Shows all submitted responses with timestamps
```

---

## 🧪 Testing

### Manual Testing

1. **Test GET /api/questions:**
   ```bash
   curl http://localhost:8000/api/questions | jq
   ```

2. **Test POST /api/answers:**
   ```bash
   curl -X POST http://localhost:8000/api/answers \
     -H "Content-Type: application/json" \
     -d '{
       "answers": [
         {"question_id": 1, "answer_value": "Test User"},
         {"question_id": 2, "answer_value": "Developer"}
       ]
     }'
   ```

3. **View saved answers in database:**
   ```bash
   # For SQLite:
   python -c "
   import sqlite3
   conn = sqlite3.connect('survey.db')
   conn.row_factory = sqlite3.Row
   cursor = conn.execute('SELECT * FROM answers;')
   for row in cursor:
       print(dict(row))
   conn.close()
   "
   ```

### Browser Testing

1. Open http://localhost:3000
2. Fill in all 5 questions
3. Click "Отправить"
4. Verify "Спасибо!" message appears
5. Check browser console for any errors (F12 → Console)

---

## 🐛 Troubleshooting

### Backend doesn't start
```
Error: ModuleNotFoundError: No module named 'fastapi'
Solution: pip install -r requirements.txt
```

### Frontend won't connect to backend
```
Error: CORS error in browser console
Solution: 
- Check backend is running: curl http://localhost:8000
- Verify CORS_ORIGINS in backend/config.py includes http://localhost:3000
```

### Database connection fails
```
Error: sqlite3.DatabaseError or psycopg2 error
Solution (for SQLite):
- Delete survey.db and restart (will auto-recreate)
Solution (for PostgreSQL):
- Update DATABASE_URL in backend/.env with correct credentials
```

### Port already in use
```
Error: Address already in use :8000 or :3000
Solution:
Backend: lsof -i :8000 && kill -9 <PID>
Frontend: lsof -i :3000 && kill -9 <PID>
```

---

## 📝 Environment Variables

### Backend (.env)
```env
# Database URL (default: SQLite)
DATABASE_URL=sqlite:///./survey.db

# OR for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/mini_survey_db

DEBUG=True
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🚀 Production Considerations

For production deployment:

1. **Backend:**
   - Use PostgreSQL instead of SQLite
   - Set `DEBUG=False`
   - Use proper secrets management (.env doesn't load in prod)
   - Add authentication/authorization
   - Rate limiting and validation
   - Docker containerization

2. **Frontend:**
   - Run `npm run build` to create optimized bundle
   - Serve from CDN or static hosting
   - Add API request timeouts
   - Implement offline support

3. **General:**
   - Set up CI/CD pipeline
   - Add comprehensive logging
   - Database migrations
   - Performance monitoring

---

## 🔗 Useful Commands

### Backend
```bash
# Start development server
python main.py

# Start with auto-reload (already enabled by default)
# Reset database
rm survey.db && python main.py

# View API docs
# Open browser to http://localhost:8000/docs
```

### Frontend
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests (if any)
npm test
```

### Database
```bash
# SQLite: Access database
sqlite3 survey.db

# View tables
.tables

# View questions
SELECT * FROM questions;

# View answers
SELECT * FROM answers;
```

---

## 📋 Checklist - Running Locally

- [ ] Python 3.12+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Dependencies installed
  - Backend: `pip install -r requirements.txt`
  - Frontend: `npm install`
- [ ] Backend starts: `python main.py` (should see "Uvicorn running")
- [ ] Frontend starts: `npm start` (browser opens to localhost:3000)
- [ ] Can access http://localhost:8000/docs (Swagger UI)
- [ ] Can load survey form in browser
- [ ] Can submit answers and see success message
- [ ] Backend logs show no errors

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MobX Documentation](https://mobx.js.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 📄 License

This project is a learning exercise created for OTUS AI course.

---

## 👨‍💼 Author

Created with AI assistance (GitHub Copilot) as part of the OTUS AI program.

**AI Prompts Documentation**: See [prompts.md](./prompts.md) for all prompts used during development.

---

## Changelog

### v0.1.0 (2024-04-26)
- Initial release with backend API and frontend UI
- 5 hardcoded survey questions (mixed types)
- SQLite database with automatic schema creation
- MobX state management
- Responsive React UI with gradient styling
- CORS support for local development
- Complete API documentation

---

**Last Updated:** April 26, 2026  
**Status:** ✅ Ready for local development