import React from 'react';
import { observer } from 'mobx-react-lite';
import ResultsStore from '../stores/ResultsStore';
import '../styles/Results.css';

/**
 * Submission detail view component.
 * Displays full submission info and all answers for a participant.
 */
const SubmissionDetail = observer(() => {
  const { selectedSubmission } = ResultsStore;

  if (!selectedSubmission) {
    return null;
  }

  const handleBack = () => {
    ResultsStore.clearSelectedSubmission();
  };

  const handleDelete = () => {
    if (
      window.confirm(
        `Are you sure you want to delete this submission from ${selectedSubmission.participant_name}?`
      )
    ) {
      ResultsStore.deleteSubmissionById(selectedSubmission.id);
      if (!ResultsStore.error) {
        handleBack();
      }
    }
  };

  return (
    <div className="submission-detail">
      <div className="detail-header">
        <button
          className="btn btn-secondary"
          onClick={handleBack}
          disabled={ResultsStore.isLoading}
        >
          ← Назад к списку
        </button>
        <h2>Детали ответов</h2>
      </div>

      {ResultsStore.error && (
        <div className="error-message">{ResultsStore.error}</div>
      )}

      {ResultsStore.isLoading ? (
        <div className="loading">Loading submission details...</div>
      ) : (
        <div className="detail-content">
          {/* Participant Information */}
          <div className="participant-card">
            <h3>Информация об участнике</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Имя:</label>
                <p>{selectedSubmission.participant_name}</p>
              </div>
              <div className="info-item">
                <label>Email:</label>
                <p>{selectedSubmission.participant_email}</p>
              </div>
              <div className="info-item">
                <label>Дата прохождения:</label>
                <p>
                  {new Date(selectedSubmission.submitted_at).toLocaleDateString(
                    'ru-RU',
                    {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                      second: '2-digit',
                    }
                  )}
                </p>
              </div>
              <div className="info-item">
                <label>ID Записи:</label>
                <p>#{selectedSubmission.id}</p>
              </div>
            </div>
          </div>

          {/* Answers */}
          <div className="answers-section">
            <h3>Ответы на вопросы ({selectedSubmission.answers.length})</h3>
            <div className="answers-list">
              {selectedSubmission.answers.map((answer, index) => (
                <div key={answer.question_id} className="answer-item">
                  <div className="answer-number">{index + 1}</div>
                  <div className="answer-content">
                    <h4 className="question-text">{answer.question_text}</h4>
                    <p className="answer-text">{answer.answer_value}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="detail-actions">
            <button
              className="btn btn-secondary"
              onClick={handleBack}
              disabled={ResultsStore.isLoading}
            >
              Назад к списку
            </button>
            <button
              className="btn btn-danger"
              onClick={handleDelete}
              disabled={ResultsStore.isDeleting}
            >
              {ResultsStore.isDeleting ? 'Удаление...' : '🗑️ Удалить эту запись'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
});

export default SubmissionDetail;
