import React, { useEffect } from 'react';
import { observer } from 'mobx-react-lite';
import SurveyStore from '../stores/SurveyStore';
import QuestionField from './QuestionField';
import '../styles/App.css';

/**
 * Main survey form component.
 * Displays participant info fields, questions, handles user input, and submits answers.
 * Wrapped with observer() to react to MobX state changes.
 */
const SurveyForm = observer(() => {
  useEffect(() => {
    // Load questions on component mount
    SurveyStore.fetchQuestions();
  }, []);

  const handleNameChange = (e) => {
    SurveyStore.setParticipantName(e.target.value);
  };

  const handleEmailChange = (e) => {
    SurveyStore.setParticipantEmail(e.target.value);
  };

  const handleAnswerChange = (questionId, value) => {
    SurveyStore.setAnswer(questionId, value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    SurveyStore.submitAnswers();
  };

  const handleReset = () => {
    SurveyStore.reset();
  };

  // Loading state
  if (SurveyStore.isLoading && SurveyStore.questions.length === 0) {
    return (
      <div className="survey-container">
        <div className="loading">Loading survey...</div>
      </div>
    );
  }

  // Success state
  if (SurveyStore.isSubmitted) {
    return (
      <div className="survey-container">
        <div className="success-message">
          <h2>🎉 Спасибо!</h2>
          <p>{SurveyStore.submissionMessage}</p>
          <p>Бланк {SurveyStore.participantName} ({SurveyStore.participantEmail}) был успешно записан.</p>
          <button className="btn btn-primary" onClick={handleReset}>
            Заполнить анкету снова
          </button>
        </div>
      </div>
    );
  }

  // Form state
  return (
    <div className="survey-container">
      <div className="survey-header">
        <h1>Мини-анкета</h1>
        <p>Пожалуйста, ответьте на следующие вопросы:</p>
      </div>

      {SurveyStore.error && (
        <div className="error-message">{SurveyStore.error}</div>
      )}

      <form onSubmit={handleSubmit} className="survey-form">
        {/* Participant Information Section */}
        <div className="form-section participant-info">
          <h3>Ваши данные</h3>
          
          <div className="form-group">
            <label htmlFor="name">
              Ваше имя <span className="required">*</span>
            </label>
            <input
              id="name"
              type="text"
              placeholder="Введите ваше имя"
              value={SurveyStore.participantName}
              onChange={handleNameChange}
              disabled={SurveyStore.isLoading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">
              Ваш email <span className="required">*</span>
            </label>
            <input
              id="email"
              type="email"
              placeholder="Введите ваш email"
              value={SurveyStore.participantEmail}
              onChange={handleEmailChange}
              disabled={SurveyStore.isLoading}
              required
            />
          </div>
        </div>

        {/* Survey Questions Section */}
        <div className="form-section questions">
          <h3>Вопросы опроса</h3>
          {SurveyStore.questions.map((question) => (
            <QuestionField
              key={question.id}
              question={question}
              value={SurveyStore.answers[question.id] || ''}
              onChange={handleAnswerChange}
            />
          ))}
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={SurveyStore.isLoading}
          >
            {SurveyStore.isLoading ? 'Отправка...' : 'Отправить'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={handleReset}
            disabled={SurveyStore.isLoading}
          >
            Очистить
          </button>
        </div>
      </form>

      <div className="question-count">
        {Object.values(SurveyStore.answers).filter((a) => a).length}/
        {SurveyStore.questions.length} вопросов заполнено
      </div>
    </div>
  );
});

export default SurveyForm;
