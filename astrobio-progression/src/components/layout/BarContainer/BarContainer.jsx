import { useNavigate } from "react-router-dom";
import ProgressBar from "../../ProgressBar/ProgressBar.jsx";
import "./BarContainer.css";

function BarContainer() {
  const navigate = useNavigate();

  // Helper function to handle navigation to the topic page
  const handleNavigate = (topic) => {
    navigate(`/topic/${topic}`);
  };

  return (
    <div className="bar-container">
      <ProgressBar
        label="Sustaining Life Support Systems"
        progress={42}
        onClick={() => handleNavigate("life-support")}
      />
      <ProgressBar
        label="Growing Food on Mars"
        progress={68}
        onClick={() => handleNavigate("agriculture")}
      />
      <ProgressBar
        label="Building Habitable Space Environments"
        progress={25}
        onClick={() => handleNavigate("space-habitation")}
      />
    </div>
  );
}

export default BarContainer;