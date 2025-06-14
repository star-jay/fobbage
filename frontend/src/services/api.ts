import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // The vite proxy will handle rewriting this to the backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Submits a bluff for a given question.
 * @param quizId - The ID of the quiz.
 * @param questionId - The ID of the question.
 * @param bluffText - The user's bluff.
 * @returns A promise that resolves when the submission is successful.
 */
export const submitBluff = (quizId: number, questionId: number, bluffText: string): Promise<void> => {
  console.log(`Submitting bluff for quiz ${quizId}, question ${questionId}: "${bluffText}"`);
  // In a real app, this would be:
  // return api.post(`/quizzes/${quizId}/questions/${questionId}/bluff/`, { text: bluffText });
  return Promise.resolve();
};

/**
 * Submits a guess for a given question.
 * @param quizId - The ID of the quiz.
 * @param questionId - The ID of the question.
 * @param answerId - The ID of the chosen answer.
 * @returns A promise that resolves when the submission is successful.
 */
export const submitGuess = (quizId: number, questionId: number, answerId: number): Promise<void> => {
  console.log(`Submitting guess for quiz ${quizId}, question ${questionId}: answer ${answerId}`);
  // In a real app, this would be:
  // return api.post(`/quizzes/${quizId}/questions/${questionId}/guess/`, { answer_id: answerId });
  return Promise.resolve();
};

export default api; 