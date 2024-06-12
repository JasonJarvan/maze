import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [mazeHtml, setMazeHtml] = useState(null);
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [pathLength, setPathLength] = useState('');
  const [message, setMessage] = useState('');
  const [hint, setHint] = useState(null);

  useEffect(() => {
    generateMaze();
  }, []);

  useEffect(() => {
    if (mazeHtml && mazeHtml.script) {
      const script = document.createElement('script');
      script.type = 'text/javascript';
      script.text = mazeHtml.script;
      document.body.appendChild(script);
      return () => {
        document.body.removeChild(script);
      };
    }
  }, [mazeHtml]);

  const generateMaze = async () => {
    try {
      const response = await axios.get('http://localhost:50190/generate_maze');
      setMazeHtml({ script: response.data.script, div: response.data.div });
      setStart(response.data.start);
      setEnd(response.data.end);
      setPathLength('');
      setMessage('');
      setHint(null);
    } catch (error) {
      console.error("Error generating maze:", error);
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:50190/solve_maze', {
        maze: mazeHtml.div,
        start,
        end,
        path_length: parseInt(pathLength, 10),
      });
      setMessage(response.data.message);
      if (response.data.correct) {
        generateMaze();
      }
    } catch (error) {
      console.error("Error submitting solution:", error);
    }
  };

  const getHint = async () => {
    try {
      const response = await axios.post('http://localhost:50190/get_hint', {
        maze: mazeHtml.div,
        start,
        end,
      });
      setHint(response.data.path);
    } catch (error) {
      console.error("Error getting hint:", error);
    }
  };

  return (
    <div>
      <h1>Maze Solver</h1>
      <div
        id="maze-container"
        dangerouslySetInnerHTML={{ __html: mazeHtml?.div }}
      />
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
