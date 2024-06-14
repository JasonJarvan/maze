import React, { useState } from 'react';

const MazeSolver = () => {
    const [length, setLength] = useState('');
    const [result, setResult] = useState('');

    const validatePath = () => {
        fetch('/validate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ length: parseInt(length) })
        })
        .then(response => response.json())
        .then(data => setResult(data.result));
    };

    return (
        <div>
            <input
                type="number"
                value={length}
                onChange={(e) => setLength(e.target.value)}
                placeholder="Enter path length"
            />
            <button onClick={validatePath}>Validate Path</button>
            <p>{result}</p>
        </div>
    );
};

export default MazeSolver;
