import React, { useEffect } from 'react';
import { observer } from 'mobx-react-lite';
import ResultsStore from '../stores/ResultsStore';
import ParticipantsList from './ParticipantsList';
import SubmissionDetail from './SubmissionDetail';
import '../styles/Results.css';

/**
 * Results page container component.
 * Manages switching between participants list view and submission detail view.
 */
const ResultsPage = observer(() => {
  useEffect(() => {
    // Load submissions on component mount
    ResultsStore.fetchSubmissions();
  }, []);

  return (
    <div className="results-page">
      <div className="results-container">
        {/* Show detail view if a submission is selected, otherwise show list view */}
        {ResultsStore.selectedSubmission ? (
          <SubmissionDetail />
        ) : (
          <ParticipantsList />
        )}
      </div>
    </div>
  );
});

export default ResultsPage;
