import React, { useEffect } from 'react';

const Maze = () => {
    useEffect(() => {
        fetch('/mnt/data/maze.html')
            .then(response => response.text())
            .then(html => {
                const script = document.createElement('script');
                script.innerHTML = html;
                document.getElementById('maze-container').appendChild(script);
            });
    }, []);

    return <div id="maze-container"></div>;
};

export default Maze;
