import React from 'react';
import styled from '@emotion/styled';
import { Link, useParams } from 'react-router-dom';

const ScoreboardContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.l};
  text-align: center;
  background-color: ${({ theme }) => theme.colors.surface};
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
`;

const ScoreDisplay = styled.p`
  font-size: 2rem;
  font-weight: 500;
  margin: ${({ theme }) => theme.spacing.xl} 0;
`;

const NextQuizButton = styled(Link)`
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

const RoundScoreboardPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();

  // In a real app, scores would be passed via state or fetched.
  const score = 1000; // Mock score
  const totalScore = 3500; // Mock total score

  return (
    <ScoreboardContainer>
      <Title>Round Over!</Title>
      <ScoreDisplay>
        You scored {score} points this round.
        <br />
        Your total score is now {totalScore}.
      </ScoreDisplay>
      <NextQuizButton to={`/quiz/${id}/results`}>
        Finish Quiz & See Final Results
      </NextQuizButton>
    </ScoreboardContainer>
  );
};

export default RoundScoreboardPage; 