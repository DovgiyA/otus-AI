# AI Prompts Used During Development

This document records all AI prompts and instructions used to generate code for the Mini-Survey Application. This is done as per project requirements to maintain transparency in AI-assisted development.

---

## Table of Contents

1. [Project Planning & Architecture](#project-planning--architecture)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [Documentation](#documentation)

---

## Project Planning & Architecture

### Prompt 1: Initial Project Scoping

**Request:**
> Generiraj jednostavnu web aplikaciju "Mini-anketa" za dobijanje konfiguracije ankete i slanje odgovora.
> 
> Cilj:
> 1. stvoriti minimalno full-stack aplikaciju (backend + frontend);
> 2. backend na python FastAPI Stack + postgres;
> 3. Backend predostavlja dva API: GET /questions, POST /answers;
> 4. Frontend react + mobX;
> 5. Aplikacija mora biti la lokalno;
> 6. README.md sa detaljnim instrukcijama;
> 7. Sačuvaj sve prompts.

**AI Completion:** Generated comprehensive project plan with:
- Technology stack selection (FastAPI, React, MobX, PostgreSQL/SQLite)
- Project directory structure
- Implementation phases (backend, database, frontend, integration, documentation)
- Architecture decisions (monorepo layout, global MobX store, etc.)

---

## Backend Development

### Prompt 2: Backend Requirements Configuration

**Request:**
> Create backend configuration file that loads environment variables with database URL support for both PostgreSQL and SQLite. Include fallback to SQLite for local development.

**AI Completion (config.py):**
- Pydantic BaseSettings for environment configuration
- DATABASE_URL parameter with SQLite fallback
- CORS origins list for development
- Settings class with Config for .env file support

### Prompt 3: Database Setup with SQLAlchemy

**Request:**
> Create database.py file that initializes SQLAlchemy engine, session factory, and declarative base. It should support both PostgreSQL and SQLite, with proper connection pooling and initialization function.

**AI Completion (database.py):**
- SQLAlchemy engine creation with conditional parameters
- SessionLocal factory for dependency injection
- Base declarative class for ORM models
- get_db() dependency function for FastAPI routes
- init_db() function to create all tables

### Prompt 4: SQLAlchemy ORM Models

**Request:**
> Create SQLAlchemy models for Question and Answer entities. Question should have id, text, type (text/radio), options (JSON for radio choices), and order. Answer should have id, question_id (FK), answer_value, and created_at timestamp.

**AI Completion (models.py):**
```python
- Question model with:
  - id (primary key)
  - text (String, 500 chars, not null)
  - type (String, 50 chars, "text" or "radio")
  - options (JSON, nullable for radio choices)
  - order (Integer, default 0)
  - relationship to answers with cascade delete

- Answer model with:
  - id (primary key)
  - question_id (foreign key to questions)
  - answer_value (String, 1000 chars)
  - created_at (DateTime, defaults to UTC now)
  - relationship back to question
```

### Prompt 5: Pydantic Request/Response Schemas

**Request:**
> Create Pydantic validation schemas for:
> 1. QuestionResponse - for returning questions
> 2. AnswerSubmit - for single answer in request
> 3. AnswersRequest - for batch answer submission
> 4. AnswerResponse - for saved answer
> 5. SuccessResponse - generic success response

**AI Completion (schemas.py):**
- QuestionResponse with from_attributes for ORM
- AnswerSubmit for nested array validation
- AnswersRequest wrapper for answer collection
- AnswerResponse with datetime field
- SuccessResponse with optional data field

### Prompt 6: FastAPI Routes - GET /questions and POST /answers

**Request:**
> Create FastAPI router for survey endpoints:
> 
> GET /api/questions - return hardcoded 3-5 survey questions:
> - Q1: Text input (name)
> - Q2: Radio (job title)
> - Q3: Radio (years in IT)
> - Q4: Text input (programming languages)
> - Q5: Radio (specialization)
> 
> POST /api/answers - accept and save answers to database, validate question_id exists, return success message.
> 
> Seed questions on first run if DB empty.

**AI Completion (routers/survey.py):**
- Hardcoded INITIAL_QUESTIONS constant with 5 questions in Russian
- GET /questions endpoint with auto-seeding logic
- seed_questions() helper function
- POST /answers endpoint with:
  - Request validation (not empty)
  - Question existence check
  - Database transaction handling
  - Error handling with rollback
  - Success response with count

### Prompt 7: FastAPI Application Entry Point

**Request:**
> Create main.py that:
> 1. Initializes FastAPI app
> 2. Adds CORS middleware for localhost:3000
> 3. Includes survey router at /api
> 4. Has health check at /
> 5. Initializes database on startup
> 6. Runs with uvicorn on port 8000

**AI Completion (main.py):**
- FastAPI app factory with title and description
- CORSMiddleware configuration
- Router inclusion with prefix
- Health check endpoint
- db initialization with error handling
- uvicorn run configuration

---

## Frontend Development

### Prompt 8: React Project Setup

**Request:**
> Create frontend package.json with dependencies:
> - react 18.2.0
> - mobx 6.10.2
> - mobx-react-lite 4.0.5
> - axios 1.6.2
> - react-scripts 5.0.1
> 
> Include npm scripts for start, build, test, eject.

**AI Completion (package.json):**
- Complete package.json with exact versions
- Standard npm scripts
- eslint config
- Browser list for production/development

### Prompt 9: Public HTML Entry Point

**Request:**
> Create public/index.html for React app entry point with necessary meta tags and root div.

**AI Completion (public/index.html):**
- DOCTYPE and lang="en"
- Meta tags for charset and viewport
- Root element for React
- Script reference

### Prompt 10: MobX Store for Survey State

**Request:**
> Create MobX store (SurveyStore.js) that manages:
> 1. questions array (loaded from API)
> 2. answers object (question_id → answer_value mapping)
> 3. isLoading boolean
> 4. isSubmitted boolean
> 5. error string
> 
> Actions:
> - fetchQuestions() - GET /api/questions
> - setAnswer(questionId, value) - update answer
> - submitAnswers() - POST /api/answers with validation
> - reset() - clear form state

**AI Completion (src/stores/SurveyStore.js):**
```javascript
- makeAutoObservable for automatic observable binding
- fetchQuestions() with try-catch and state updates
- setAnswer() for reactive answer updates
- submitAnswers() with:
  - Answer validation (all answered)
  - Formatting for API
  - Loading and error states
  - Success flag
- reset() to clear form
- Singleton instance export
```

### Prompt 11: Axios API Client

**Request:**
> Create api/surveyApi.js that provides:
> 1. getQuestions() - GET /api/questions
> 2. postAnswers(payload) - POST /api/answers
> 
> Use axios with base URL from REACT_APP_API_URL environment variable.

**AI Completion (src/api/surveyApi.js):**
- Axios instance with baseURL from env
- getQuestions() with error handling
- postAnswers() with request formatting
- Proper error messaging

### Prompt 12: Reusable QuestionField Component

**Request:**
> Create QuestionField.jsx component that renders:
> - For type "text": <input type="text" />
> - For type "radio": <fieldset> with radio options
> 
> Props: question object, value, onChange callback.

**AI Completion (src/components/QuestionField.jsx):**
- Conditional rendering based on question.type
- Radio group with unique IDs
- Label associations
- onChange handler calling parent callback

### Prompt 13: Main SurveyForm Component

**Request:**
> Create SurveyForm.jsx component with observer() wrapper that:
> 1. Loads questions on mount
> 2. Renders QuestionField for each question
> 3. Shows loading spinner while fetching
> 4. Shows "Спасибо!" after submission
> 5. Has Submit and Clear buttons
> 6. Shows progress: "X/Y вопросов заполнено"
> 7. Shows error messages if any
> 
> Connect to MobX store for state management.

**AI Completion (src/components/SurveyForm.jsx):**
```javascript
- observer() HOC for reactivity
- useEffect to fetch questions
- Loading state rendering
- Success state rendering with reset option
- Form with QuestionField components
- Submit/Clear buttons with disabling
- Progress indicator at bottom
- Error message display
```

### Prompt 14: App Component

**Request:**
> Create App.jsx that simply imports and renders SurveyForm component.

**AI Completion (src/App.jsx):**
- Simple wrapper component
- Imports SurveyForm
- Returns div with app class

### Prompt 15: React Entry Point

**Request:**
> Create src/index.js that initializes React app with ReactDOM.createRoot() and renders App component.

**AI Completion (src/index.js):**
- Import statements
- createRoot(document.getElementById('root'))
- Render App in StrictMode

### Prompt 16: Global Styles

**Request:**
> Create src/index.css with global styles:
> - Gradient background (purple gradient)
> - Flexbox centered layout
> - Font family settings
> - Remove default margins/padding

**AI Completion (src/index.css):**
- Font stack definition
- Gradient background
- Min-height 100vh with flex centering
- Anti-aliasing settings

### Prompt 17: Form Styling

**Request:**
> Create src/styles/App.css with comprehensive form styling:
> 1. Container with rounded corners and shadow
> 2. Header with title and description
> 3. Input fields with focus states
> 4. Radio button groups
> 5. Submit/Clear buttons with hover effects
> 6. Success message styling
> 7. Error message styling
> 8. Loading and progress indicators
> 9. Responsive design for mobile

**AI Completion (src/styles/App.css):**
```css
- Animation for slide-in effect
- Gradient buttons with shadows
- Focus states with color and glow
- Radio button custom styling
- Success message with emoji
- Error message box with border
- Mobile breakpoint (max-width: 600px)
- Form actions flex layout
- Question count indicator
```

### Prompt 18: Frontend Environment Variables

**Request:**
> Create frontend/.env with REACT_APP_API_URL pointing to localhost:8000.

**AI Completion (frontend/.env):**
- REACT_APP_API_URL=http://localhost:8000

---

## Documentation

### Prompt 19: Comprehensive README

**Request:**
> Create detailed README.md with:
> 1. Project overview and features
> 2. Technology stack with versions
> 3. Prerequisites
> 4. Step-by-step setup instructions for backend and frontend
> 5. API endpoint documentation with examples
> 6. Project structure explanation
> 7. Architecture diagrams and descriptions
> 8. Database schema
> 9. Full workflow example
> 10. Testing instructions
> 11. Troubleshooting guide
> 12. Useful commands
> 13. Checklist for running locally

**AI Completion (README.md):**
- Comprehensive guide covering all aspects
- Code examples for testing
- Troubleshooting section
- Environment variables documentation
- Production considerations
- Additional resources section

### Prompt 20: Prompts Documentation

**Request:**
> Create prompts.md that documents all AI prompts and instructions used to generate the code, organized by development phase, with request and completion summary for each.

**AI Completion (prompts.md):**
- This file
- Organized by section (planning, backend, frontend, docs)
- Each prompt with request and completion summary
- Code snippets where relevant

---

## Environment Files

### Prompt 21: Backend Environment Configuration

**Request:**
> Create backend/.env file for local development with SQLite database by default.

**AI Completion (backend/.env):**
```
DATABASE_URL=sqlite:///./survey.db
DEBUG=True
```

---

## Summary

**Total Prompts:** 21 main development prompts  
**Python Version:** Updated for Python 3.12+
**Dependency Versions:** Updated for Python 3.12 compatibility
**Sections:**
- Project Planning: 1 prompt
- Backend Development: 7 prompts
- Frontend Development: 9 prompts
- Documentation: 3 prompts
- Configuration: 1 prompt

**Code Files Generated:**
- Backend: 8 files (main.py, config.py, database.py, models.py, schemas.py, routers/survey.py, .env, requirements.txt)
- Frontend: 10 files (package.json, .env, public/index.html, src/index.js, src/App.jsx, src/stores/SurveyStore.js, src/api/surveyApi.js, src/components/SurveyForm.jsx, src/components/QuestionField.jsx, src/styles/App.css, src/index.css)
- Documentation: 3 files (README.md, prompts.md, .gitignore)

**Total Lines of Code Generated:** ~2,000+ lines (including comments and documentation)

---

## AI Model Used

**Model:** GitHub Copilot (Claude Haiku 4.5)  
**Provider:** Anthropic / Microsoft GitHub  
**Version:** As of April 26, 2026

---

## Development Approach

The development followed an iterative, structured approach:

1. **Phase 1 - Planning**: Clarify requirements and create architectural plan
2. **Phase 2 - Backend**: Implement FastAPI app, database models, API routes
3. **Phase 3 - Frontend**: Build React components with MobX state management
4. **Phase 4 - Testing**: Verify all components work end-to-end
5. **Phase 5 - Documentation**: Write comprehensive guides and prompt documentation

Each phase built upon previous work, with continuous verification of functionality.

---

## Key Decisions & Rationale

### Database: SQLite by Default + PostgreSQL Support
- **Rationale**: SQLite for easier local development without installing PostgreSQL
- **Implementation**: Conditional connection parameters in database.py
- **Benefit**: Works immediately; can switch to PostgreSQL for production

### State Management: MobX with Global Store
- **Rationale**: Simpler than Redux; per requirements; good for forms
- **Implementation**: Singleton SurveyStore with observer wrapper
- **Benefit**: Reactive UI updates without boilerplate

### Mixed Question Types
- **Rationale**: Demonstrate flexibility in form handling
- **Implementation**: type property determines rendering (text input vs radio group)
- **Benefit**: Shows framework extensibility for future question types

### Monorepo Structure
- **Rationale**: Simpler deployment; related code together; easier testing
- **Implementation**: /backend and /frontend in single git repo
- **Benefit**: Single clone, single documentation, shared .gitignore

---

## Future Enhancements

Based on this foundation, potential additions:

1. **Authentication**: User authentication and account management
2. **Question Types**: Checkboxes, dropdowns, date pickers, file uploads
3. **Survey Analytics**: Charts, statistics, export to CSV/PDF
4. **Admin Panel**: Survey creation, editing, response management
5. **Email Notifications**: Send confirmation emails
6. **Conditional Logic**: Show/hide questions based on previous answers
7. **Multiple Surveys**: Support multiple survey templates
8. **Internationalization**: Multi-language support (already started with Russian)

---

**Document Created:** April 26, 2026  
**Last Updated:** April 26, 2026  
**Status:** Complete - Ready for reference
