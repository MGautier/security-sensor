'use strict';

var React = require('react');
var d3 = require('d3');
var Arc = require('./Arc');


module.exports = React.createClass({

  displayName: 'DataSeries',

  propTypes: {
    transform: React.PropTypes.string,
    data: React.PropTypes.array,
    innerRadius: React.PropTypes.number,
    radius: React.PropTypes.number,
    colors: React.PropTypes.func
  },

  getDefaultProps() {
    return {
      innerRadius: 0,
      data: [],
      colors: d3.scale.category20c()
    };
  },

  render() {

    var props = this.props;

    var pie = d3.layout
      .pie()
      .sort(null);

    var arcData = pie(props.data);

    var arcs = arcData.map((arc, idx) => {
      return (
        <Arc
          startAngle={arc.startAngle}
          endAngle={arc.endAngle}
          outerRadius={props.radius}
          innerRadius={props.innerRadius}
          labelTextFill={props.labelTextFill}
          valueTextFill={props.valueTextFill}
          valueTextFormatter={props.valueTextFormatter}
          fill={props.colors(idx)}
          label={props.labels[idx]}
          value={props.data[idx]}
          key={idx}
          width={props.width}
        />
      );
    });
    return (
      <g className='rd3-piechart-pie' transform={props.transform} >{arcs}</g>
    );
  }
});
