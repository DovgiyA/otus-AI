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
 * Submit survey answers to POST /api/answers
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
