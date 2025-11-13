import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PagLogin from './components/Pag_login.jsx';
import Home from './Pages/Home.jsx';
import Listas from './pages/Listas.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PagLogin />} />
        <Route path="/home" element={<Home />} />
        <Route path="/listas" element={<Listas />} />

      </Routes>
    </BrowserRouter>
  );
}
