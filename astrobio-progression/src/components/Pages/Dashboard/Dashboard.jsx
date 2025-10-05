import BarGraph from "./BarGraph/BarGraph.jsx";
import Heatmap from "./Heatmap/Heatmap.jsx";
import WordGraph from "./WordGraph/WordGraph.jsx";
import Consensus from "./Consensus/Consensus.jsx";
import NavBar from "./NavBar/DashboardNavBar.jsx";
import "./Dashboard.css"

function Dashboard() {
    return (
        <div className="dashboard-container">
            <NavBar />
            <main className="graphs-container">
                <BarGraph />
                <Heatmap />
                <WordGraph />
                <Consensus />
            </main>
        </div>
    );
}
export default Dashboard;