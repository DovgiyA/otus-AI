import React from 'react';
import { observer } from 'mobx-react-lite';
import ResultsStore from '../stores/ResultsStore';
import '../styles/Results.css';

/**
 * Participants list table component.
 * Displays all submissions with search, sort, and action buttons.
 */
const ParticipantsList = observer(() => {
  const handleSearchChange = (e) => {
    ResultsStore.setSearchQuery(e.target.value);
  };

  const handleSearch = () => {
    ResultsStore.fetchSubmissions();
  };

  const handleSortChange = (e) => {
    ResultsStore.setSortBy(e.target.value);
    ResultsStore.fetchSubmissions();
  };

  const handleViewDetails = (submissionId) => {
    ResultsStore.selectSubmission(submissionId);
  };

  const handleDelete = (submissionId, name) => {
    if (
      window.confirm(
        `Are you sure you want to delete the submission from ${name}?`
      )
    ) {
      ResultsStore.deleteSubmissionById(submissionId);
    }
  };

  return (
    <div className="participants-list">
      <div className="list-header">
        <h2>Результаты опроса</h2>
        <p>Всего записей: {ResultsStore.submissions.length}</p>
      </div>

      {/* Search and Filter Section */}
      <div className="search-section">
        <div className="search-group">
          <input
            type="text"
            placeholder="Поиск по имени или email..."
            value={ResultsStore.searchQuery}
            onChange={handleSearchChange}
            disabled={ResultsStore.isLoading}
          />
          <button
            className="btn btn-secondary"
            onClick={handleSearch}
            disabled={ResultsStore.isLoading}
          >
            {ResultsStore.isLoading ? 'Поиск...' : 'Поиск'}
          </button>
        </div>

        <div className="sort-group">
          <label htmlFor="sort">Сортировать по:</label>
          <select
            id="sort"
            value={ResultsStore.sortBy}
            onChange={handleSortChange}
            disabled={ResultsStore.isLoading}
          >
            <option value="date_desc">Новые первыми</option>
            <option value="date_asc">Старые первыми</option>
          </select>
        </div>
      </div>

      {ResultsStore.error && (
        <div className="error-message">{ResultsStore.error}</div>
      )}

      {ResultsStore.message && (
        <div className="success-message">{ResultsStore.message}</div>
      )}

      {/* Submissions Table */}
      {ResultsStore.submissions.length === 0 ? (
        <div className="no-data">
          <p>Нет записей для отображения</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="submissions-table">
            <thead>
              <tr>
                <th>№</th>
                <th>Имя</th>
                <th>Email</th>
                <th>Дата прохождения</th>
                <th># Ответов</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {ResultsStore.submissions.map((sub, index) => (
                <tr key={sub.id}>
                  <td>{index + 1}</td>
                  <td>{sub.participant_name}</td>
                  <td>{sub.participant_email}</td>
                  <td>
                    {new Date(sub.submitted_at).toLocaleDateString('ru-RU', {
                      year: 'numeric',
                      month: '2-digit',
                      day: '2-digit',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </td>
                  <td className="center">{sub.answer_count}</td>
                  <td className="actions">
                    <button
                      className="btn btn-sm btn-info"
                      onClick={() => handleViewDetails(sub.id)}
                      disabled={ResultsStore.isLoading}
                      title="Просмотреть ответы"
                    >
                      📖 Просмотр
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() =>
                        handleDelete(sub.id, sub.participant_name)
                      }
                      disabled={ResultsStore.isDeleting}
                      title="Удалить запись"
                    >
                      🗑️ Удалить
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
});

export default ParticipantsList;
