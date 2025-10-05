import { Routes, Route } from "react-router-dom";
import HomePage from "./Pages/Home/HomePage.jsx";
import Dashboard from "./Pages/Dashboard/Dashboard.jsx";
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dashboard/:category" element={<Dashboard />} />   {/* parameters!! */}
      <Route path="*" element={<div>Not Found</div>} /> {/* not found page */}
    </Routes>
  );
}

export default App;
