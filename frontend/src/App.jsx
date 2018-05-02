import React, { Component } from 'react';

import './App.css';

import { AreaClosed } from '@vx/shape';

class SimpleIndicator extends Component {
  render() {
    return (
      <div className="simple-indicator">
        <div className="indicator-value">
          {this.props.value}
        </div>
        <div className="indicator-title">
          {this.props.title}
        </div>       
      </div>
    );
  }
}

class RequestsIndicator extends Component {
  constructor (props) {
    super(props);
    this.state = {value : 0, data : []};
    this.socket = new WebSocket(
      //      'ws://' + window.location.host +
         'ws://localhost:8000' +
        '/ws/events/http_request/' + this.props.updateEvery +'/');
    this.socket.onmessage = this.handleMessage.bind(this);
  }
  handleMessage (message) {
    const val = JSON.parse(message.data);
    const dataPoints = this.props.showPrevious / this.props.updateEvery;
    
    this.setState(prevState => ({value : val.average,
                                 data : prevState.data.slice(prevState.data.length - dataPoints, prevState.data.length).concat([{
                                   'timestamp' : new Date(val.timestamp * 1000),//.toUTCString(),
                                   'value' : val.average
                                 }])}));
  }
  render() {
    return (
      <div>
        <svg width={300} height={300}>
          <Group top={margin.top} left={margin.left}>
            <AreaClosed
               data={this.state.data}
               xScale={xScale}
               yScale={yScale}
               x={x}
               y={y}
               fill={"red"}
        />
      </Group>
    </svg>        
        <SimpleIndicator title="Requests/second" value={this.state.value}/>
      </div>
    );
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <RequestsIndicator updateEvery={1} showPrevious={30}/>
      </div>
    );
  }
}

export default App;
