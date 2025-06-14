import { Global, css } from '@emotion/react';
import type { ThemeType } from './theme';

const styles = (theme: ThemeType) => css`
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Roboto:wght@400;500&display=swap');

  body {
    margin: 0;
    padding: 0;
    background-color: ${theme.colors.background};
    font-family: ${theme.fonts.body};
    color: ${theme.colors.onBackground};
  }

  * {
    box-sizing: border-box;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-family: ${theme.fonts.heading};
  }
`;

const GlobalStyles = () => {
  return <Global styles={styles} />;
};

export default GlobalStyles; 