import { makeAutoObservable } from 'mobx';
import { getQuestions, postAnswers } from '../api/surveyApi';

class SurveyStore {
  questions = [];
  answers = {};
  isLoading = false;
  isSubmitted = false;
  submissionMessage = '';
  error = null;

  constructor() {
    makeAutoObservable(this);
  }

  /**
   * Fetch questions from the backend API
   */
  async fetchQuestions() {
    this.isLoading = true;
    this.error = null;
    try {
      const data = await getQuestions();
      this.questions = data;
      // Initialize empty answers object
      this.answers = {};
      data.forEach((q) => {
        this.answers[q.id] = '';
      });
    } catch (err) {
      this.error = err.message || 'Failed to load questions';
      console.error('Error fetching questions:', err);
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Update answer for a specific question
   */
  setAnswer(questionId, value) {
    this.answers[questionId] = value;
  }

  /**
   * Submit all answers to the backend
   */
  async submitAnswers() {
    this.isLoading = true;
    this.error = null;
    
    try {
      // Validate that all questions have answers
      const allAnswered = this.questions.every((q) => this.answers[q.id]?.trim() !== '');
      if (!allAnswered) {
        this.error = 'Please answer all questions';
        return;
      }

      // Format answers for submission
      const answersArray = Object.entries(this.answers).map(([questionId, value]) => ({
        question_id: parseInt(questionId),
        answer_value: value,
      }));

      // Post to backend
      const response = await postAnswers({ answers: answersArray });
      
      if (response.success) {
        this.isSubmitted = true;
        this.submissionMessage = response.message;
        console.log('Answers submitted successfully!');
      }
    } catch (err) {
      this.error = err.message || 'Failed to submit answers';
      console.error('Error submitting answers:', err);
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Reset the form to initial state
   */
  reset() {
    this.answers = {};
    this.isSubmitted = false;
    this.submissionMessage = '';
    this.error = null;
    this.questions.forEach((q) => {
      this.answers[q.id] = '';
    });
  }
}

export default new SurveyStore();
