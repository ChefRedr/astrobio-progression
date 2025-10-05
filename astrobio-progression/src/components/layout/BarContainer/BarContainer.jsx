import { useNavigate } from "react-router-dom";
import ProgressBar from "../../ProgressBar/ProgressBar.jsx";
import { categories } from "./categories.js";
import "./BarContainer.css";

export default function BarContainer() {
    const navigate = useNavigate();

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
