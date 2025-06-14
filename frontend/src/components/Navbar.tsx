import React from 'react';
import { Link } from 'react-router-dom';
import styled from '@emotion/styled';

const NavContainer = styled.nav`
  background-color: ${({ theme }) => theme.colors.primary};
  padding: ${({ theme }) => theme.spacing.m};
  display: flex;
  align-items: center;
`;

const Title = styled.h1`
  margin: 0;
  font-size: 1.5rem;
`;

const StyledLink = styled(Link)`
  text-decoration: none;
  color: ${({ theme }) => theme.colors.onPrimary};

  &:hover {
    text-decoration: underline;
  }
`;

const Navbar: React.FC = () => {
  return (
    <NavContainer>
      <StyledLink to="/">
        <Title>Fobbage</Title>
      </StyledLink>
    </NavContainer>
  );
};

export default Navbar; 