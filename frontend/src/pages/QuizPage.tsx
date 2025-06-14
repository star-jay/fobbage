import React, { useState, useMemo } from 'react';
import styled from '@emotion/styled';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import QuestionDisplay from '../components/QuestionDisplay';
import AnswerOptions from '../components/AnswerOptions';
import type { Quiz, Answer } from '../types';
import { MOCK_QUIZ } from '../mockData';

const QuizContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.l};

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    padding: ${({ theme }) => theme.spacing.m};
  }
`;

const QuizTitle = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
  margin-bottom: ${({ theme }) => theme.spacing.xl};
`;

const NextButton = styled.button`
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.onSecondary};
  border: none;
  padding: ${({ theme }) => theme.spacing.m} ${({ theme }) => theme.spacing.l};
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  margin-top: ${({ theme }) => theme.spacing.l};
  float: right;

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const QuizPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();

  const { playerBluff } = (location.state as { playerBluff: string }) || {};

  const [quiz] = useState<Quiz>(MOCK_QUIZ);
  const [currentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, number>>({});

  const currentQuestion = quiz.questions[currentQuestionIndex];

  const answerOptions = useMemo(() => {
    const options: Answer[] = [...currentQuestion.answers];
    if (playerBluff) {
      options.push({ id: 99, text: playerBluff }); // Add player's bluff
    }
    // Add other mock bluffs
    options.push({ id: 100, text: 'A type of cheese' });
    options.push({ id: 101, text: 'The capital of Mongolia' });

    // Shuffle the options
    return options.sort(() => Math.random() - 0.5);
  }, [currentQuestion, playerBluff]);

  const handleSelectAnswer = (questionId: number, answerId: number) => {
    setSelectedAnswers(prev => ({ ...prev, [questionId]: answerId }));
  };

  const handleNextQuestion = () => {
    const selectedAnswer = selectedAnswers[currentQuestion.id];
    navigate(`/quiz/${id}/rundown`, { state: { guess: selectedAnswer, questionId: currentQuestion.id } });
  };

  const selectedAnswerForCurrentQuestion = selectedAnswers[currentQuestion.id] || null;

  return (
    <QuizContainer>
      <QuizTitle>{quiz.title} - Guess!</QuizTitle>
      <QuestionDisplay questionText={currentQuestion.question_text} />
      <AnswerOptions
        answers={answerOptions}
        selectedAnswer={selectedAnswerForCurrentQuestion}
        onSelectAnswer={answerId => handleSelectAnswer(currentQuestion.id, answerId)}
      />
      <NextButton onClick={handleNextQuestion} disabled={!selectedAnswerForCurrentQuestion}>
        Submit Guess
      </NextButton>
    </QuizContainer>
  );
};

export default QuizPage; 