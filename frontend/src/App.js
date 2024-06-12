import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';
import BokehChart from './BokehChart';

function App() {
  const [plot, setPlot] = useState(null);
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [pathLength, setPathLength] = useState('');
  const [message, setMessage] = useState('');
  const [hint, setHint] = useState(null);

  useEffect(() => {
    generateMaze();
  }, []);

  const generateMaze = async () => {
    const response = await axios.get('http://localhost:50190/generate_maze');
    setPlot(response.data.plot);
    setStart(response.data.start);
    setEnd(response.data.end);
    setPathLength('');
    setMessage('');
    setHint(null);
  };

  const handleSubmit = async () => {
    const response = await axios.post('http://localhost:50190/solve_maze', {
      maze: plot,
      start,
      end,
      path_length: parseInt(pathLength, 10),
    });
    setMessage(response.data.message);
    if (response.data.correct) {
      generateMaze();
    }
  };

  const getHint = async () => {
    const response = await axios.post('http://localhost:50190/get_hint', {
      maze: plot,
      start,
      end,
    });
    setHint(response.data.path);
  };

  return (
    <div>
      <h1>Maze Solver</h1>
      <BokehChart plot={plot} />
      <input
        type="number"
        value={pathLength}
        onChange={(e) => setPathLength(e.target.value)}
        placeholder="Enter path length"
      />
      <button onClick={handleSubmit}>Submit</button>
      <button onClick={getHint}>Hint</button>
      <p>{message}</p>
      {hint && <p>Hint: {hint}</p>}
    </div>
  );
}

export default App;
