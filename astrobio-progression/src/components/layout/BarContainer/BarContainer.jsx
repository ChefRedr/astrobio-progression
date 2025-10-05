import { useNavigate } from "react-router-dom";
import ProgressBar from "../../ProgressBar/ProgressBar.jsx";
import { categories } from "./categories.js";
import "./BarContainer.css";

function BarContainer() {
  const navigate = useNavigate();

  // Helper function to handle navigation to the topic page
  const handleNavigate = (topic) => {
    navigate(`/topic/${topic}`);
  };

    return (
        <div>
            {categories.map(cat => (
                <ProgressBar
                    key={cat.param}
                    label={cat.label}
                    progress={cat.progress}
                    onClick={() => navigate(`/dashboard/${cat.param}`)}
                />
            ))}
        </div>
    );
}

export default BarContainer;