import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import PagLogin from './components/Pag_login.jsx';
import Home from './Pages/Home.jsx';
import Listas from './pages/Listas.jsx';
import Metricas from './Pages/Metricas.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<PagLogin />} />
        <Route path="/home" element={<Home />} />
        <Route path="/listas" element={<Listas />} />
        <Route path="/metricas" element={<Metricas />} />

      </Routes>
    </BrowserRouter>
  );
}
