import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { showBokeh } from './bokehUtils';

const Maze = () => {
  const [mazeData, setMazeData] = useState(null);
  const [inputPathLength, setInputPathLength] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [hint, setHint] = useState('');

  useEffect(() => {
    generateMaze();
  }, []);

  const generateMaze = async () => {
    try {
      const response = await axios.get('/generate_maze');
      setMazeData(response.data);
      showBokeh(response.data.maze);
    } catch (error) {
      console.error('Error generating maze:', error);
    }
  };

  const validatePath = async () => {
    if (!mazeData) return;
    try {
      const response = await axios.post('/validate_path', {
        maze: mazeData.maze,
        start: mazeData.start,
        end: mazeData.end,
        path_length: parseInt(inputPathLength, 10)
      });
      setValidationMessage(response.data.correct ? 'Correct!' : 'Incorrect.');
    } catch (error) {
      console.error('Error validating path:', error);
    }
  };

  const getHint = async () => {
    if (!mazeData) return;
    try {
      const response = await axios.post('/get_hint', {
        maze: mazeData.maze,
        start: mazeData.start,
        end: mazeData.end
      });
      setHint(`Hint path: ${response.data.path}, Length: ${response.data.length}`);
    } catch (error) {
      console.error('Error getting hint:', error);
    }
  };

  return (
    <div>
      <h1>Maze Solver</h1>
      <div id="maze-container"></div>
      <input
        type="text"
        placeholder="Enter shortest path length"
        value={inputPathLength}
        onChange={(e) => setInputPathLength(e.target.value)}
      />
      <button onClick={validatePath}>Submit Path Length</button>
      <button onClick={getHint}>Get Hint</button>
      <p>{validationMessage}</p>
      <p>{hint}</p>
      <button onClick={generateMaze}>Next Maze</button>
    </div>
  );
};

export default Maze;
