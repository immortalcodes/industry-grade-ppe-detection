// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import ZonePage from './ZonePage';
import CameraPage from './CameraPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} exact />
        <Route path="/zone/:id" element={<ZonePage />} />
        <Route path="/zone/:zoneId/camera/:cameraId" element={<CameraPage />} />
      </Routes>
    </Router>
  );
}

export default App;

