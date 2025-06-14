import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styled from '@emotion/styled';
import type { Quiz } from '../types';

// Mock data that we would normally get from the API
const MOCK_QUIZZES: Quiz[] = [
  { id: 1, title: 'React Basics', questions: [] },
  { id: 2, title: 'Advanced TypeScript', questions: [] },
  { id: 3, title: 'Django Fundamentals', questions: [] },
];

const PageContainer = styled.div`
  padding: ${({ theme }) => theme.spacing.l};
  max-width: 800px;
  margin: 0 auto;

  @media (max-width: ${({ theme }) => theme.breakpoints.mobile}) {
    padding: ${({ theme }) => theme.spacing.m};
  }
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
`;

const QuizList = styled.ul`
  list-style: none;
  padding: 0;
`;

const QuizListItem = styled.li`
  background-color: ${({ theme }) => theme.colors.surface};
  border: 1px solid #ddd;
  padding: ${({ theme }) => theme.spacing.m};
  margin-bottom: ${({ theme }) => theme.spacing.m};
  border-radius: 4px;
  transition: box-shadow 0.2s;

  &:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
`;

const QuizLink = styled(Link)`
  text-decoration: none;
  color: ${({ theme }) => theme.colors.onSurface};
  font-weight: 500;
  font-size: 1.2rem;
`;

const LoadingMessage = styled.div`
  font-size: 1.2rem;
  color: #666;
`;

const QuizListPage: React.FC = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, you'd fetch this data from an API.
    // Here, we're simulating a network request with a timeout.
    const timer = setTimeout(() => {
      setQuizzes(MOCK_QUIZZES);
      setLoading(false);
    }, 500); // simulate 500ms network delay

    return () => clearTimeout(timer); // cleanup timer on unmount
  }, []);

  if (loading) {
    return (
      <PageContainer>
        <LoadingMessage>Loading quizzes...</LoadingMessage>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Title>Available Quizzes</Title>
      <QuizList>
        {quizzes.map(quiz => (
          <QuizListItem key={quiz.id}>
            <QuizLink to={`/quiz/${quiz.id}`}>{quiz.title}</QuizLink>
          </QuizListItem>
        ))}
      </QuizList>
    </PageContainer>
  );
};

export default QuizListPage; 