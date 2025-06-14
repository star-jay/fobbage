import type { Quiz } from './types';

export const MOCK_QUIZ: Quiz = {
  id: 1,
  title: 'React Basics',
  questions: [
    {
      id: 1,
      question_text: 'What is JSX?',
      answers: [
        { id: 1, text: 'A syntax extension for JavaScript' },
        { id: 2, text: 'A templating language' },
        { id: 3, text: 'A CSS preprocessor' },
      ],
    },
    {
      id: 2,
      question_text: 'What is the virtual DOM?',
      answers: [
        { id: 4, text: 'A direct representation of the DOM' },
        { id: 5, text: 'A copy of the DOM in memory' },
        { id: 6, text: 'A new browser feature' },
      ],
    },
  ],
}; 