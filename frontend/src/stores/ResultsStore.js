import { makeAutoObservable } from 'mobx';
import {
  getSubmissions,
  getSubmissionDetail,
  deleteSubmission,
} from '../api/surveyApi';

class ResultsStore {
  submissions = [];
  selectedSubmission = null;
  searchQuery = '';
  sortBy = 'date_desc'; // 'date_asc' or 'date_desc'
  isLoading = false;
  isDeleting = false;
  error = null;
  message = '';

  constructor() {
    makeAutoObservable(this);
  }

  /**
   * Fetch all submissions with optional search and sort
   */
  async fetchSubmissions() {
    this.isLoading = true;
    this.error = null;
    try {
      const data = await getSubmissions(this.searchQuery || null, this.sortBy);
      this.submissions = data;
      console.log(`Loaded ${data.length} submissions`);
    } catch (err) {
      this.error = err.message || 'Failed to load submissions';
      console.error('Error fetching submissions:', err);
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Select a submission to view details
   */
  async selectSubmission(submissionId) {
    this.isLoading = true;
    this.error = null;
    try {
      const data = await getSubmissionDetail(submissionId);
      this.selectedSubmission = data;
      console.log('Loaded submission details:', data);
    } catch (err) {
      this.error = err.message || 'Failed to load submission details';
      console.error('Error fetching submission detail:', err);
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Clear selected submission (go back to list)
   */
  clearSelectedSubmission() {
    this.selectedSubmission = null;
    this.error = null;
  }

  /**
   * Update search query
   */
  setSearchQuery(query) {
    this.searchQuery = query;
  }

  /**
   * Update sort order
   */
  setSortBy(sort) {
    this.sortBy = sort;
  }

  /**
   * Delete a submission by ID
   */
  async deleteSubmissionById(submissionId) {
    this.isDeleting = true;
    this.error = null;
    this.message = '';
    
    try {
      const response = await deleteSubmission(submissionId);
      if (response.success) {
        this.message = `Submission ${submissionId} deleted successfully`;
        // Remove from list
        this.submissions = this.submissions.filter((s) => s.id !== submissionId);
        // Clear selection if it was the deleted one
        if (this.selectedSubmission?.id === submissionId) {
          this.selectedSubmission = null;
        }
        console.log('Submission deleted:', submissionId);
      }
    } catch (err) {
      this.error = err.message || 'Failed to delete submission';
      console.error('Error deleting submission:', err);
    } finally {
      this.isDeleting = false;
    }
  }

  /**
   * Reset store to initial state
   */
  reset() {
    this.submissions = [];
    this.selectedSubmission = null;
    this.searchQuery = '';
    this.sortBy = 'date_desc';
    this.isLoading = false;
    this.isDeleting = false;
    this.error = null;
    this.message = '';
  }
}

export default new ResultsStore();
