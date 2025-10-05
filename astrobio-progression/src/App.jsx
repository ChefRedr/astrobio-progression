import { Routes, Route } from "react-router-dom";
import HomePage from "./components/Pages/Home/HomePage.jsx";
// import LifeSupport from "./studycategories/LifeSupport.jsx";
// import Agriculture from "./studycategories/Agriculture.jsx";
// import SpaceHabitation from "./studycategories/SpaceHabitation.jsx";
import "./App.css"

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
    </Routes>
  );
}

export default App;