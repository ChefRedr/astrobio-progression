import ProgressBar from "../../ProgressBar/ProgressBar.jsx";
import { useNavigate } from "react-router-dom";
import "./BarContainer.css"

function BarContainer() {
    const navigate = useNavigate();

    return (
        <div>
            <ProgressBar
                label="Sustaining Life Support Systems"
                progress={42}
                onClick={() => navigate("/studies/life-support")}
            />
            <ProgressBar
                label="Growing Food on Mars"
                progress={68}
                onClick={() => navigate("/studies/agriculture")}
            />
            <ProgressBar
                label="Building Habitable Space Environments"
                progress={25}
                onClick={() => navigate("/studies/space-habitation")}
            />
        </div>
    )

}
export default BarContainer;
