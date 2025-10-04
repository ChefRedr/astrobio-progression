import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ProgressBar from "./components/ProgressBar/ProgressBar.jsx";

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <ProgressBar label="Putting the article in an LLM" progress={3}/>
      <ProgressBar label="Putting the article in an LLM" progress={3}/>
      <ProgressBar label="Putting the article in an LLM" progress={3}/>
      <ProgressBar label="Putting the article in an LLM" progress={3}/>
    </div>
  )
}

export default App
