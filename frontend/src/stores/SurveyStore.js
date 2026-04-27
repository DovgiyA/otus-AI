import { makeAutoObservable } from 'mobx';
import { getQuestions, createSubmission } from '../api/surveyApi';

class SurveyStore {
  questions = [];
  participantName = '';
  participantEmail = '';
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
   * Update participant name
   */
  setParticipantName(name) {
    this.participantName = name;
  }

  /**
   * Update participant email
   */
  setParticipantEmail(email) {
    this.participantEmail = email;
  }

  /**
   * Update answer for a specific question
   */
  setAnswer(questionId, value) {
    this.answers[questionId] = value;
  }

  /**
   * Reset form to initial state
   */
  reset() {
    this.participantName = '';
    this.participantEmail = '';
    this.answers = {};
    this.isSubmitted = false;
    this.submissionMessage = '';
    this.error = null;
    this.questions.forEach((q) => {
      this.answers[q.id] = '';
    });
  }

  /**
   * Submit all answers to the backend
   */
  async submitAnswers() {
    this.isLoading = true;
    this.error = null;
    
    try {
      // Validate participant name
      if (!this.participantName.trim()) {
        this.error = 'Please enter your name';
        this.isLoading = false;
        return;
      }

      // Validate participant email
      if (!this.participantEmail.trim()) {
        this.error = 'Please enter your email';
        this.isLoading = false;
        return;
      }

      // Simple email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.participantEmail)) {
        this.error = 'Please enter a valid email address';
        this.isLoading = false;
        return;
      }

      // Validate that all questions have answers
      const allAnswered = this.questions.every((q) => this.answers[q.id]?.trim() !== '');
      if (!allAnswered) {
        this.error = 'Please answer all questions';
        this.isLoading = false;
        return;
      }

      // Format answers for submission
      const answersArray = Object.entries(this.answers).map(([questionId, value]) => ({
        question_id: parseInt(questionId),
        answer_value: value,
      }));

      // Post to backend
      const response = await createSubmission({
        participant_name: this.participantName.trim(),
        participant_email: this.participantEmail.trim(),
        answers: answersArray
      });
      
      if (response.success) {
        this.isSubmitted = true;
        this.submissionMessage = response.message;
        console.log('Submission created successfully!', response);
      }
    } catch (err) {
      this.error = err.message || 'Failed to submit survey';
      console.error('Error submitting survey:', err);
    } finally {
      this.isLoading = false;
    }
  }
}

export default new SurveyStore();
