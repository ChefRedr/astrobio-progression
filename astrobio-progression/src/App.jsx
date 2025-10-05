import { Routes, Route } from "react-router-dom";
import HomePage from "./Pages/Home/HomePage.jsx";
import Dashboard from "./Pages/Dashboard/Dashboard.jsx";
import TopicPage from "./Pages/Topic/TopicPage.jsx";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dashboard/:category" element={<Dashboard />} />
      <Route path="/topic/:topic" element={<TopicPage />} />
    </Routes>
  );
}

export default App;
