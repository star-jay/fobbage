# Pillar 2: Modern Frontend with React

This plan details the steps to build a new, responsive user interface as a single-page application (SPA) using React, served by the Django backend.

### Part 0: Remove old Vue frontend

Goal: Completely remove the old Vue.js frontend to prepare for the new React application.

- [ ] Delete the Vue source code directory: `src/`.
- [ ] Delete the Vue public assets directory: `public/`.
- [ ] Delete Vue-specific configuration files from the root: `vue.config.js`, `babel.config.js`, `postcss.config.js`, `.browserslistrc`, `.eslintrc.js`.
- [ ] Delete the old Javascript dependencies and lock file from the root: `package.json`, `package-lock.json`.
- [ ] Delete the installed node modules directory: `node_modules/`.
- [ ] Delete the old build output directory inside the Django app: `fobbage/dist/`.
- [ ] In `fobbage/settings.py`, find the `STATICFILES_DIRS` tuple and remove the line `os.path.join(BASE_DIR, 'fobbage/dist')`. This will be replaced in Part 1.

### Part 1: Project Setup & Backend Configuration

Goal: Initialize a new React project and configure the backend for standalone frontend development.

- [x] Create a `frontend` directory in the project root.
- [x] Initialize a new React project inside `frontend/` using Vite with the TypeScript template (`npm create vite@latest frontend -- --template react-ts`).
- [x] Clean up the default Vite boilerplate files (e.g., `App.css`, `logo.svg`).
- [x] In `vite.config.ts`, configure a proxy to the Django backend API (e.g., `http://localhost:8000/api`) to handle API requests during development.
- [x] In Django's `settings.py`, configure `CORS_ALLOWED_ORIGINS` to allow requests from your frontend development server (e.g., `http://localhost:5173` for Vite). `CORS_ORIGIN_ALLOW_ALL = True` can be used for initial development but should be locked down for production.

### Part 2: API Endpoints for the Frontend

Goal: Create the necessary Django REST Framework endpoints for the quiz functionality.

- [x] Add `djangorestframework` to the backend `requirements.in` and install it.
- [x] In the `quizes` app, create a `serializers.py` file.
- [x] Create serializers for the `Quiz`, `Question`, and `Answer` models. Ensure nested serialization for questions within a quiz.
- [x] In the `quizes` app, create API views in `views.py`.
    - [x] Create a view to list all available quizzes.
    - [x] Create a view to retrieve a single quiz, including all its questions and their possible answers.
    - [x] Create a view to receive a user's submitted answers and calculate the score.
- [x] Create a `urls.py` in the `quizes` app and wire up the views.
- [x] Include the `quizes.urls` in the root `fobbage/urls.py` under the `/api/` prefix.

### Part 3: Core React Component Development

Goal: Build the fundamental UI components and application structure.

- [x] Install essential frontend libraries: `react-router-dom` for routing and `axios` for data fetching.
- [x] Set up the basic file structure in `frontend/src/`:
    - [x] `components/` (reusable UI components)
    - [x] `pages/` (top-level page components)
    - [x] `services/` (for API calls)
- [x] Create an API service module (`src/services/api.ts`) to encapsulate all `axios` calls to the backend.
- [x] Set up client-side routing in `App.tsx` using `react-router-dom`.
    - [x] Route for the quiz selection page (`/`).
    - [x] Route for taking a specific quiz (`/quiz/:id`).
    - [x] Route for the results page (`/quiz/:id/results`).
- [x] Develop page components:
    - [x] `QuizListPage.tsx`: Fetches and displays a list of quizzes.
    - [x] `QuizPage.tsx`: Manages the state for an active quiz session.
    - [x] `ResultsPage.tsx`: Displays the final score.
- [x] Develop reusable UI components:
    - [x] `QuestionDisplay.tsx`: Renders the text for a single question.
    - [x] `AnswerOptions.tsx`: Renders the choices for a question and handles click events.
    - [x] `Navbar.tsx`: A simple navigation bar for the app.

### Part 4: Styling and Finalization

Goal: Apply a modern design system using Emotion and ensure the application is responsive.

- [ ] Install Emotion libraries: `@emotion/react` for the core functionality and `@emotion/styled` for the `styled` component API.
- [ ] Create a `theme.ts` file to define a design system (colors, spacing, fonts) that can be used across the application.
- [ ] Wrap the main `App` component with Emotion's `<ThemeProvider>` and provide the theme to all child components.
- [ ] Refactor the existing placeholder components (`Navbar`, `QuizListPage`, etc.) to use the `styled()` API from Emotion for styling.
- [ ] Ensure the layout is responsive (e.g., using media queries within your styled components) and works well on both desktop and mobile devices.
- [ ] Perform a final round of testing to ensure all components are styled correctly and the application is visually consistent.

### Part 5: Implementing Fobbage Gameplay (Single-Player)

Goal: Refactor the frontend to support the two-phase (Bluffing and Guessing) gameplay loop for a single-player Fobbage experience.

- [x] **State Management:**
    - [x] Utilize React's built-in state management (`useState`, `useReducer`, `useContext`) to handle the game state throughout the quiz lifecycle (e.g., current phase, round, player submissions).
- [x] **New Page & Component Structure:**
    - [x] **Bluffing Page (`/quiz/:id/round/:roundNum/bluff`):**
        - [x] Displays the current question.
        - [x] Provides a text input field for the player to submit their bluff.
        - [x] Transitions to the guessing phase after submission.
    - [x] **Guessing Page (`/quiz/:id/round/:roundNum/guess`):**
        - [x] Modify the existing `QuizPage` to serve this purpose.
        - [x] Displays the question and a list of multiple-choice answers (the real one, the player's bluff, and mock bluffs).
        - [x] Allows the player to select one answer as their guess.
        - [x] Add a "Like" button next to each answer (except the player's own).
    - [x] **Answer Rundown Page (`/quiz/:id/round/:roundNum/rundown`):**
        - [x] Displayed after the player guesses for a question.
        - [x] Shows the list of answers, revealing the correct answer and the origin of each bluff.
        - [x] Highlights the correct answer and updates the score visually.
    - [x] **Round Scoreboard Page (`/quiz/:id/round/:roundNum/scores`):**
        - [x] Displayed after a full round is complete.
        - [x] Shows scores for the round and the updated total score.
- [x] **Routing & Component Refactoring:**
    - [x] **`App.tsx`:** Add new routes for the bluffing, rundown, and scoreboard pages. The route for `/quiz/:id` should now lead to the start of the Fobbage game loop (e.g., the first bluffing page).
    - [x] **Refactor `api.ts`:** Ensure API calls for submitting bluffs and guesses are defined (even if mocked initially).
    - [x] **Create New Components:** Implement the new pages: `BluffingPage`, `AnswerRundownPage`, and `RoundScoreboardPage`.
    - [x] **Refactor `QuizListPage`:** Update links on this page to direct to the new Fobbage game flow instead of the old `QuizPage`.
    - [x] **Refactor `ResultsPage`:** Enhance it to display the final score in a summary table.

### Part 6: Deployment

Goal: Deploy the frontend and backend applications independently.

- [ ] **Frontend Deployment:**
    - [ ] Configure the build script in `frontend/package.json` to build the static assets.
    - [ ] Set up a new site on a static hosting provider like Netlify or Vercel, pointing to the `frontend` directory in your monorepo.
    - [ ] Configure environment variables in the hosting provider's UI (e.g., `VITE_API_BASE_URL=https://your-backend-api.com`) to point the frontend to the live backend.
    - [ ] In the React app, use the environment variable (`import.meta.env.VITE_API_BASE_URL`) when making API calls.
- [ ] **Backend Deployment:**
    - [ ] Deploy the Django application to a service like Heroku or a cloud VM.
    - [ ] In the production Django settings, update `CORS_ALLOWED_ORIGINS` to include the URL of your deployed frontend (e.g., `https://your-frontend-app.netlify.app`). 