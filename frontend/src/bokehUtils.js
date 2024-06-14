import { embed } from '@bokeh/bokehjs';

export const showBokeh = (item) => {
  document.getElementById('maze-container').innerHTML = '';
  embed.embed_item(item, 'https://cdn.bokeh.org/bokeh/release/bokeh-2.4.2.min.js');
};
