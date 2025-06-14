import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { submitBluff } from '../services/api';
import QuestionDisplay from '../components/QuestionDisplay';
import { MOCK_QUIZ } from '../mockData'; // We'll move mock data to its own file

const BluffingContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: ${({ theme }) => theme.spacing.l};
  text-align: center;
`;

const Title = styled.h1`
  color: ${({ theme }) => theme.colors.primary};
`;

const BluffInput = styled.input`
  width: 100%;
  padding: ${({ theme }) => theme.spacing.m};
  font-size: 1.2rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-top: ${({ theme }) => theme.spacing.xl};
`;

const SubmitButton = styled.button`
  background-color: ${({ theme }) => theme.colors.secondary};
  color: ${({ theme }) => theme.colors.onSecondary};
  border: none;
  padding: ${({ theme }) => theme.spacing.m} ${({ theme }) => theme.spacing.l};
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  margin-top: ${({ theme }) => theme.spacing.l};

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const BluffingPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [bluff, setBluff] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // For now, we'll just use the first question of our mock quiz.
  // A real implementation would track rounds and questions.
  const currentQuestion = MOCK_QUIZ.questions[0];
  const quizId = Number(id);

  const handleSubmit = async () => {
    if (!bluff.trim()) return;

    setIsSubmitting(true);
    try {
      await submitBluff(quizId, currentQuestion.id, bluff);
      // Navigate to the guessing page, passing the bluff along in the state.
      navigate(`/quiz/${id}/guess`, { state: { playerBluff: bluff } });
    } catch (error) {
      console.error('Failed to submit bluff:', error);
      // Handle error state in UI
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <BluffingContainer>
      <Title>What's the answer?</Title>
      <QuestionDisplay questionText={currentQuestion.question_text} />
      <BluffInput
        type="text"
        placeholder="Enter your most believable bluff..."
        value={bluff}
        onChange={(e) => setBluff(e.target.value)}
        disabled={isSubmitting}
      />
      <SubmitButton onClick={handleSubmit} disabled={!bluff.trim() || isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit Bluff'}
      </SubmitButton>
    </BluffingContainer>
  );
};

export default BluffingPage; 