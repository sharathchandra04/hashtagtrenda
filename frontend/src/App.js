import React from 'react';
import { Routes, Route, BrowserRouter as Router } from 'react-router-dom';  // Update for React Router v7
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import UploadPage from './pages/UploadPage';
import FoldersPage from './pages/FolderPage';
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <div>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/home" element={<UploadPage />} />
      </Routes>
    </Router>
    </div>
  );
}

export default App;
