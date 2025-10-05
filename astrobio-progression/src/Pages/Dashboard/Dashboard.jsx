import BarGraph from "../../components/charts/BarGraph/BarGraph.jsx";
import Heatmap from "../../components/charts/Heatmap/Heatmap.jsx";
import WordGraph from "../../components/charts/WordGraph/WordGraph.jsx";
import Consensus from "../../components/charts/Consensus/Consensus.jsx";
import NavBar from "../../components/layout/DashboardNavBar/DashboardNavBar.jsx";
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