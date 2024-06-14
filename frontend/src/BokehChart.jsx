import React, { useEffect } from 'react';
import { embed } from 'bokehjs';

const BokehChart = ({ plot }) => {
  useEffect(() => {
    if (plot) {
      embed.embed_item(plot, 'bokeh-chart');
    }
  }, [plot]);

  return <div id="bokeh-chart"></div>;
};

export default BokehChart;
