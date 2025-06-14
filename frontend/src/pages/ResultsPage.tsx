import React from 'react';
import styled from '@emotion/styled';
import { useLocation, Link } from 'react-router-dom';
import type { Quiz } from '../types';

const ResultsContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.l};
  text-align: center;
  background-color: ${({ theme }) => theme.colors.surface};
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    padding: ${({ theme }) => theme.spacing.m};
  }
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
`;

const Score = styled.p`
  font-size: 3rem;
  font-weight: bold;
  color: ${({ theme }) => theme.colors.secondary};
  margin: ${({ theme }) => theme.spacing.m} 0;
`;

const Message = styled.p`
  font-size: 1.2rem;
  margin-bottom: ${({ theme }) => theme.spacing.xl};
`;

const ScoreDetail = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: 1.2rem;
  padding: ${({ theme }) => theme.spacing.m} 0;
  border-bottom: 1px solid #eee;

  &:last-of-type {
    border-bottom: none;
  }
`;

const TryAgainButton = styled(Link)`
  display: inline-block;
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.onSecondary};
  border: none;
  padding: ${({ theme }) => theme.spacing.m} ${({ theme }) => theme.spacing.l};
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  transition: transform 0.2s;

  &:hover {
    transform: scale(1.05);
  }
`;

const ResultsPage: React.FC = () => {
  const location = useLocation();
  // For this single-player mock, we'll just show a pre-canned result.
  // The state passing from the old QuizPage is no longer relevant.
  const { quiz } = (location.state as { quiz: Quiz }) || { quiz: { title: 'React Basics' } };

  const finalScore = 3500; // Mock final score
  const bluffingPoints = 1500;
  const guessingPoints = 2000;

  return (
    <ResultsContainer>
      <Title>Final Score for {quiz.title}</Title>
      <Score>
        {finalScore} Points
      </Score>
      <Message>Here's how you did:</Message>
      <ScoreDetail>
        <span>Points from Guessing Correctly:</span>
        <span>{guessingPoints}</span>
      </ScoreDetail>
      <ScoreDetail>
        <span>Points from Tricking Others:</span>
        <span>{bluffingPoints}</span>
      </ScoreDetail>
      <TryAgainButton to="/">Play Another Quiz</TryAgainButton>
    </ResultsContainer>
  );
};

export default ResultsPage;