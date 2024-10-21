import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Summary from './pages/Summary';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/summary" element={<Summary />} />
    </Routes>
  );
};

export default App;
