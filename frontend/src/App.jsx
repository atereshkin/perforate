import React, { Component } from 'react';

import './App.css';

import axios from 'axios';

import { AreaClosed } from '@vx/shape';
import { Group } from '@vx/group';
import { scaleTime, scaleLinear } from '@vx/scale';
import { AxisLeft, AxisBottom } from '@vx/axis';
import { LinearGradient } from '@vx/gradient';
import { extent, max } from 'd3-array';

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


class IndicatorWithHistory extends Component {
  render() {
    const width = 500;
    const height = 200;
    const margin = {
      top: 10,
      bottom: 40,
      left: 40,
      right: 10,
    };
    const xMax = width - margin.left - margin.right;
    const yMax = height - margin.top - margin.bottom;
    const x = d => d.timestamp; 
    const y = d => d.value;
    const xScale = scaleTime({
      range: [0, xMax],
      domain: extent(this.props.history, x)
    });
    const yScale = scaleLinear({
      range: [yMax, 0],
      domain: [0, max(this.props.history, y)],
    });
    return (
      <div className="metric-with-history">
        <svg width={width} height={height} className="history-chart">
          <Group top={margin.top} left={margin.left}>
            <AxisLeft
               scale={yScale}
               top={0}
               left={0}
               stroke={'#1b1a1e'}
               tickTextFill={'#1b1a1e'}
               />
            <AxisBottom
               scale={xScale}
               top={yMax}

               stroke={'#1b1a1e'}
               tickTextFill={'#1b1a1e'}
               />
            <LinearGradient
               from='#fbc2eb'
               to='#a6c1ee'
               id='gradient'
               />            
            <AreaClosed
               data={this.props.history}
               xScale={xScale}
               yScale={yScale}
               x={x}
               y={y}
               fill={"url(#gradient)"}
               stroke={""}
               />
          </Group>
        </svg>
        <SimpleIndicator title={this.props.title} value={this.props.value}/>
      </div>
    );
  }  
}

class EventIndicator extends Component {
  constructor (props) {
    super(props);
    this.state = {value : 0, data : []};
    this.socket = new WebSocket(
      //      'ws://' + window.location.host +
         'ws://localhost:8000' +
        '/ws/events/'+this.props.eventclass+'/' + this.props.updateEvery +'/');
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
    const title=this.props.title+'/second';
    return (      
        <IndicatorWithHistory title={title} history={this.state.data} value={this.state.value}/>
    );
  }
}

class MetricIndicator extends Component {
  constructor (props) {
    super(props);
    this.state = {value : 0, data : []};
    this.socket = new WebSocket(
      //      'ws://' + window.location.host +
         'ws://localhost:8000' +
        '/ws/metrics/'+this.props.label+'/' + this.props.updateEvery +'/');
    this.socket.onmessage = this.handleMessage.bind(this);
  }
  handleMessage (message) {
    const val = JSON.parse(message.data);
    const dataPoints = this.props.showPrevious / this.props.updateEvery;
    
    this.setState(prevState => ({value : val.value,
                                 data : prevState.data.slice(prevState.data.length - dataPoints, prevState.data.length).concat([{
                                   'timestamp' : new Date(val.timestamp * 1000),//.toUTCString(),
                                   'value' : val.value
                                 }])}));
  }
  render() {
    return (      
        <IndicatorWithHistory title={this.props.title} history={this.state.data} value={this.state.value}/>
    );
  }
}


class Dashboard extends Component {
  constructor (props) {
    super(props);
    this.state = {'eventclasses':[], 'metrics':[]};
    
  }
  componentDidMount () {
    axios.get('/dash/eventclasses.json')
      .then(response => {
        console.log(response);
        const ecs = [];
        for (let i=0, l=response.data.length; i<l; i++){
          ecs.push(response.data[i]); //TODO
        }
        this.setState({'eventclasses' : ecs});
      });
    axios.get('/dash/metrics.json')
      .then(response => {
        console.log(response);
        const ms = [];
        for (let i=0, l=response.data.length; i<l; i++){
          ms.push(response.data[i]); //TODO
        }
        this.setState({'metrics' : ms});
      });

  }
  
  render() {
    const indicators = [];
    const ecs = this.state.eventclasses;
    for (let i=0; i<ecs.length; i++){
      indicators.push(<EventIndicator updateEvery={1} showPrevious={30} title={ecs[i].name} eventclass={ecs[i].label}/>);
    }
    const ms = this.state.metrics;
    for (let i=0; i<ms.length; i++){
      indicators.push(<MetricIndicator updateEvery={1} showPrevious={30} title={ms[i].name} label={ms[i].label}/>);
    }
    
    return (
      <div className="dashboard">
        {indicators}
      </div>
    );
  }
}

export default Dashboard;
