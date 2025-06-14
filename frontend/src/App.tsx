import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import QuizListPage from './pages/QuizListPage';
import QuizPage from './pages/QuizPage';
import ResultsPage from './pages/ResultsPage';
import BluffingPage from './pages/BluffingPage';
import AnswerRundownPage from './pages/AnswerRundownPage';
import RoundScoreboardPage from './pages/RoundScoreboardPage';

function App() {
  return (
    <Router>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<QuizListPage />} />
          <Route path="/quiz/:id" element={<BluffingPage />} />
          <Route path="/quiz/:id/guess" element={<QuizPage />} />
          <Route path="/quiz/:id/rundown" element={<AnswerRundownPage />} />
          <Route path="/quiz/:id/scores" element={<RoundScoreboardPage />} />
          <Route path="/quiz/:id/results" element={<ResultsPage />} />
        </Routes>
      </main>
    </Router>
  )
}

export default App
