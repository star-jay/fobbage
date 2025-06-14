import React from 'react';
import { useLocation, useNavigate, useParams, Navigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { MOCK_QUIZ } from '../mockData';

const RundownContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.l};
  text-align: center;
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
  margin-bottom: ${({ theme }) => theme.spacing.xl};
`;

const AnswerList = styled.ul`
  list-style: none;
  padding: 0;
  margin-top: ${({ theme }) => theme.spacing.l};
`;

const AnswerItem = styled.li<{ isCorrect: boolean; isPlayerGuess: boolean }>`
  background-color: ${({ theme, isCorrect, isPlayerGuess }) => {
    if (isCorrect) return '#4caf50'; // Green for correct
    if (isPlayerGuess) return theme.colors.error; // Red for incorrect guess
    return theme.colors.surface;
  }};
  color: ${({ theme, isCorrect, isPlayerGuess }) => {
    if (isCorrect || isPlayerGuess) return theme.colors.onPrimary;
    return theme.colors.onSurface;
  }};
  border: 1px solid #ddd;
  padding: ${({ theme }) => theme.spacing.m};
  margin-bottom: ${({ theme }) => theme.spacing.m};
  border-radius: 4px;
  font-weight: 500;
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
`;

const AnswerRundownPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();
  const navigate = useNavigate();

  const { guess, questionId } = (location.state as { guess: number; questionId: number }) || {};

  if (!guess || !questionId) {
    // If we don't have the necessary state, we can't show the page.
    return <Navigate to={`/quiz/${id}`} />;
  }

  // Find the question and the correct answer from our mock data
  const question = MOCK_QUIZ.questions.find(q => q.id === questionId);
  const correctAnswer = question?.answers.find(a => a.id === 1); // Mock correct answer

  const handleNext = () => {
    // In a full implementation, this would check if there are more questions
    // in the round, or if the round/quiz is over.
    // For now, it will just go to the round scoreboard.
    navigate(`/quiz/${id}/scores`);
  };

  return (
    <RundownContainer>
      <Title>Who Guessed What?</Title>
      <AnswerList>
        {question?.answers.map(answer => (
          <AnswerItem
            key={answer.id}
            isCorrect={answer.id === correctAnswer?.id}
            isPlayerGuess={answer.id === guess}
          >
            {answer.text}
            {answer.id === correctAnswer?.id && ' (Correct Answer)'}
          </AnswerItem>
        ))}
      </AnswerList>
      <NextButton onClick={handleNext}>Continue</NextButton>
    </RundownContainer>
  );
};

export default AnswerRundownPage; 