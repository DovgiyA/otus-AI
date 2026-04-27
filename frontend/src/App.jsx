import React, { useState } from 'react';
import SurveyForm from './components/SurveyForm';
import ResultsPage from './components/ResultsPage';
import './styles/App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('survey');

  return (
    <div className="app">
      <nav className="app-nav">
        <div className="nav-container">
          <h1 className="app-title">📋 IT Опрос</h1>
          <div className="nav-links">
            <button
              className={`nav-link ${currentPage === 'survey' ? 'active' : ''}`}
              onClick={() => setCurrentPage('survey')}
            >
              📝 Анкета
            </button>
            <button
              className={`nav-link ${currentPage === 'results' ? 'active' : ''}`}
              onClick={() => setCurrentPage('results')}
            >
              📊 Результаты
            </button>
          </div>
        </div>
      </nav>

      <main className="app-main">
        {currentPage === 'survey' && <SurveyForm />}
        {currentPage === 'results' && <ResultsPage />}
      </main>
    </div>
  );
}

export default App;
