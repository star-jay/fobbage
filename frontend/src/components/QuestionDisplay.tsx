import React from 'react';
import styled from '@emotion/styled';

interface QuestionDisplayProps {
  questionText: string;
}

const QuestionContainer = styled.div`
  margin-bottom: ${({ theme }) => theme.spacing.l};
`;

const QuestionText = styled.h2`
  font-size: 1.5rem;
  font-weight: 500;
  color: ${({ theme }) => theme.colors.onSurface};
  line-height: 1.4;
`;

const QuestionDisplay: React.FC<QuestionDisplayProps> = ({ questionText }) => {
  return (
    <QuestionContainer>
      <QuestionText>{questionText}</QuestionText>
    </QuestionContainer>
  );
};

export default QuestionDisplay; 