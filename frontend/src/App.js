import React, { Component } from 'react';
import BokehChart from './BokehChart';
import './App.css';

class App extends Component {
  state = {
    length: '',
    result: '',
    hint: ''
  };

  validatePath = () => {
    fetch('http://localhost:50190/validate_path', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ length: this.state.length })
    })
      .then(response => response.json())
      .then(data => {
        this.setState({ result: data.result ? 'Correct' : 'Incorrect' });
      });
  };

  getHint = () => {
    fetch('http://localhost:50190/get_hint')
      .then(response => response.json())
      .then(data => {
        this.setState({ hint: data.hint });
      });
  };

  render() {
    return (
      <div className="App">
        <h1>生成迷宫 & 解迷宫</h1>
        <BokehChart />
        <input
          type="number"
          value={this.state.length}
          onChange={e => this.setState({ length: e.target.value })}
          placeholder="输入最短路径长度"
        />
        <button onClick={this.validatePath}>验证路径</button>
        <p>{this.state.result}</p>
        <button onClick={this.getHint}>获取提示</button>
        <p>{this.state.hint}</p>
      </div>
    );
  }
}

export default App;
