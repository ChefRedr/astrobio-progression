import { useNavigate } from "react-router-dom";
import BarContainer from "./BarContainer/BarContainer.jsx";
import NavBar from "./NavBar/HomeNavBar.jsx";
import "./HomePage.css"

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      {/* <h1 className="page-title">Space Research Progress</h1> */}
      <NavBar />
      <BarContainer />
    </div>
  );
}

export default HomePage;