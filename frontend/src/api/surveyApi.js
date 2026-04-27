import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch survey questions from GET /api/questions
 */
export async function getQuestions() {
  try {
    const response = await client.get('/api/questions');
    return response.data;
  } catch (error) {
    console.error('API Error (getQuestions):', error);
    throw new Error(error.response?.data?.detail || error.message);
  }
}

/**
 * Submit survey answers to POST /api/answers (LEGACY)
 */
export async function postAnswers(payload) {
  try {
    const response = await client.post('/api/answers', payload);
    return response.data;
  } catch (error) {
    console.error('API Error (postAnswers):', error);
    throw new Error(error.response?.data?.detail || error.message);
  }
}

/**
 * Create a new submission with participant info and answers
 * POST /api/submissions
 */
export async function createSubmission(payload) {
  try {
    const response = await client.post('/api/submissions', payload);
    return response.data;
  } catch (error) {
    console.error('API Error (createSubmission):', error);
    throw new Error(error.response?.data?.detail || error.message);
  }
}

/**
 * Fetch list of all submissions
 * GET /api/submissions?search=...&sort=...
 */
export async function getSubmissions(search = null, sort = 'date_desc') {
  try {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    params.append('sort', sort);
    
    const response = await client.get(`/api/submissions?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('API Error (getSubmissions):', error);
    throw new Error(error.response?.data?.detail || error.message);
  }
}

/**
 * Fetch detailed submission info
 * GET /api/submissions/{id}
 */
export async function getSubmissionDetail(submissionId) {
  try {
    const response = await client.get(`/api/submissions/${submissionId}`);
    return response.data;
  } catch (error) {
    console.error('API Error (getSubmissionDetail):', error);
    throw new Error(error.response?.data?.detail || error.message);
  }
}

/**
 * Delete a submission
 * DELETE /api/submissions/{id}
 */
export async function deleteSubmission(submissionId) {
  try {
    const response = await client.delete(`/api/submissions/${submissionId}`);
    return response.data;
  } catch (error) {
    console.error('API Error (deleteSubmission):', error);
    throw new Error(error.response?.data?.detail || error.message);
  }
}
