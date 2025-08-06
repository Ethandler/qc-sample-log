// frontend/src/api.js

export async function getAllSamples() {
    const res = await fetch('/samples');
    if (!res.ok) throw new Error("Failed to fetch samples");
    return res.json();
  }
  