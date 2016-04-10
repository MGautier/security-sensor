var chart = c3.generate({
    bindto: '#chart',
    data: {
      columns: [
        ['data1', 30, 200, 100, 400, 150, 250],
        ['data2', 50, 20, 10, 40, 15, 25]
      ],
      axes: {
        data2: 'y2' // ADD
      }
    },
    axis: {
      y2: {
        show: true // ADD
      }
    }
});



var Visualization = React.createClass({
  render: function() {
    return (
        <div className="visualization">
        <div className="visualizationDate">
        {this.props.Date}
      </div>
        <div className="visualizationDay">
        {this.props.Day}
      </div>
        <div className="visualizationHour">
        {this.props.Hour}
      </div>
        <div className="visualizationEvents">
        {this.props.Events}
      </div>
        </div>
    );
  }
});

var VisualizationsComponent = React.createClass({
  loadVisualizationsFromServer: function(){
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function(){
    return {data: []};
  },
  componentDidMount: function(){
    this.loadVisualizationsFromServer();
    setInterval(this.loadVisualizationsFromServer, this.props.pollInterval);
  },
  render: function(){
    var testStyle = { fontSize: '18px', marginRight: '20px' };
    return (
        <div className="visualizationsComponent" style={testStyle}>
        <h1>Visualizations</h1>
        <VisualizationsList data={this.state.data}/>
        </div>
    );
  }
});

var VisualizationsList = React.createClass({
  render: function(){
    var visualizationNodes = this.props.data.map(function(visualization){
      return (
          <li><Visualization Date={visualization.Date} Day={visualization.Name_Day} Hour={visualization.Hour} Events={visualization.Process_Events} key={visualization.id} /></li>
      );
    });
    return (
        <div className="visualizationsList">
        <ul>
        {visualizationNodes}
      </ul>
        </div>
    );
  }
});

var Event = React.createClass({
  render: function() {
    return (
        <div className="event">
        <div className="eventTimestamp">
        {this.props.Timestamp}
      </div>
        <div className="eventComment">
        {this.props.Comment}
      </div>
        </div>
    );
  }
});

var EventsComponent = React.createClass({
  loadEventsFromServer: function(){
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  getInitialState: function(){
    return {data: []};
  },
  componentDidMount: function(){
    this.loadEventsFromServer();
    setInterval(this.loadEventsFromServer, this.props.pollInterval);
  },
  render: function(){
    var testStyle = { fontSize: '18px', marginRight: '20px' };
    return (
        <div className="eventsComponent" style={testStyle}>
        <h1>Events</h1>
        <EventsList data={this.state.data}/>
        </div>
    );
  }
});

var EventsList = React.createClass({
  render: function(){
    var eventNodes = this.props.data.map(function(event){
      return (
          <li><Event Timestamp={event.Local_Timestamp} Comment={event.Comment} key={event.id} /></li>
      );
    });
    return (
        <div className="eventsList">
        <ul>
        {eventNodes}
      </ul>
        </div>
    );
  }
});

React.render(
    //<EventsComponent url="api/events/" pollInterval={10000} />,
    <VisualizationsComponent url="api/visualizations/week" pollInterval={10000} />,
  document.getElementById('content')
);
