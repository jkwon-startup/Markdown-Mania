import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from './pages/MainPage';
import StagePage from './pages/StagePage';
import ResultPage from './pages/ResultPage';
import FinalPage from './pages/FinalPage';
import HelpPage from './pages/HelpPage';
import SettingsPage from './pages/SettingsPage';
import { GameProvider } from './context/GameContext';

function App() {
  return (
    <GameProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/stage/:id" element={<StagePage />} />
          <Route path="/result/:id" element={<ResultPage />} />
          <Route path="/final" element={<FinalPage />} />
          <Route path="/help" element={<HelpPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Router>
    </GameProvider>
  );
}

export default App; 