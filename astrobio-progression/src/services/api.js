// src/services/api.js
const BASE_URL = "http://127.0.0.1:5000/api";

export async function fetchArticles(topic) {
  const res = await fetch(`${BASE_URL}/articles?topic=${topic}`);
  if (!res.ok) throw new Error("Failed to fetch articles");
  return res.json();
}

export async function fetchKeywords(topic) {
  const res = await fetch(`${BASE_URL}/keywords?topic=${topic}`);
  return res.json();
}

export async function fetchAgreement(topic) {
  const res = await fetch(`${BASE_URL}/agreement?topic=${topic}`);
  return res.json();
}

export async function fetchCorrelation(topic) {
  const res = await fetch(`${BASE_URL}/correlation?topic=${topic}`);
  return res.json();
}