import React, { Component } from 'react';
import { embed } from 'bokehjs';

class BokehChart extends Component {
  componentDidMount() {
    fetch('http://localhost:50190/generate_maze')
      .then(response => response.json())
      .then(data => {
        const chartDiv = document.getElementById('bokeh-chart');
        embed.embed_item(data.plot, 'https://cdn.bokeh.org/bokeh/release/bokeh-2.4.2.min.js');
      });
  }

  render() {
    return <div id="bokeh-chart"></div>;
  }
}

export default BokehChart;
