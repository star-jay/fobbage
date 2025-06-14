import React from 'react';
import styled from '@emotion/styled';

interface Answer {
  id: number;
  text: string;
}

interface AnswerOptionsProps {
  answers: Answer[];
  onSelectAnswer: (answerId: number) => void;
  selectedAnswer: number | null;
}

const OptionsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${({ theme }) => theme.spacing.s};
`;

const AnswerButton = styled.button<{ isSelected: boolean }>`
  background-color: ${({ theme, isSelected }) =>
    isSelected ? theme.colors.primary : theme.colors.surface};
  color: ${({ theme, isSelected }) =>
    isSelected ? theme.colors.onPrimary : theme.colors.onSurface};
  border: 1px solid ${({ theme }) => theme.colors.primary};
  padding: ${({ theme }) => theme.spacing.m};
  border-radius: 4px;
  cursor: pointer;
  text-align: left;
  font-size: 1rem;
  transition: background-color 0.2s, color 0.2s;

  &:hover {
    background-color: ${({ theme }) => theme.colors.primary};
    color: ${({ theme }) => theme.colors.onPrimary};
  }

  &:disabled {
    cursor: not-allowed;
    opacity: 0.7;
  }
`;

const AnswerOptions: React.FC<AnswerOptionsProps> = ({
  answers,
  onSelectAnswer,
  selectedAnswer,
}) => {
  return (
    <OptionsContainer>
      {answers.map(answer => (
        <AnswerButton
          key={answer.id}
          onClick={() => onSelectAnswer(answer.id)}
          isSelected={selectedAnswer === answer.id}
        >
          {answer.text}
        </AnswerButton>
      ))}
    </OptionsContainer>
  );
};

export default AnswerOptions; 