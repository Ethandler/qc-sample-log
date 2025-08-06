// frontend/src/Samples.jsx
import React, { useEffect, useState } from 'react';
import { getAllSamples } from './api';

export default function Samples() {
  const [samples, setSamples] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getAllSamples()
      .then(setSamples)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h2>All Samples</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {samples.length === 0 ? (
        <p>No samples found.</p>
      ) : (
        <table border="1" cellPadding="6">
          <thead>
            <tr>
              <th>#</th>
              <th>Sample ID</th>
              <th>Material</th>
              <th>Job #</th>
              <th>Job Name</th>
            </tr>
          </thead>
          <tbody>
            {samples.map((s, i) => (
              <tr key={s.sample_id}>
                <td>{i + 1}</td>
                <td>{s.sample_id}</td>
                <td>{s.material}</td>
                <td>{s.job_number}</td>
                <td>{s.job_name}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
