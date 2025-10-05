import { Routes, Route } from "react-router-dom";
import HomePage from "./Pages/Home/HomePage.jsx";
import Dashboard from "./Pages/Dashboard/Dashboard.jsx";
// import LifeSupport from "./studycategories/LifeSupport.jsx";
// import Agriculture from "./studycategories/Agriculture.jsx";
// import SpaceHabitation from "./studycategories/SpaceHabitation.jsx";
import "./App.css"

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  );
}

export default App;