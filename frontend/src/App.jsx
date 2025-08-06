// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Samples from './Samples';

export default function App() {
  return (
    <Router>
      <div>
        <h1>📒 QC Sample Logbook</h1>
        <ul>
          <li><Link to="/samples">View Samples</Link></li>
          <li><a href="/docs">Swagger Docs</a></li>
          <li><a href="/export_pdf">Export PDF</a></li>
          <li><a href="/export_csv">Export CSV</a></li>
        </ul>

        <Routes>
          <Route path="/samples" element={<Samples />} />
        </Routes>
      </div>
    </Router>
  );
}
