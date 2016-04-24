var Visualization = React.createClass({
  componentDidMount: function() {
    var days = Array.from(this.props.set);
    var source = this.props.data.ID_Source;
    c3.generate({
      data: {
        url: 'api/visualizations/chart.json/',
        mimeType: 'json',
        selection: {
          enabled: true
        },
        keys: {
          x: 'day',
          value: ['events']
        },
        names: {
          events: 'Iptables Events'
        },
        onclick: function (d, element){
          console.log("DAY ACTUAL",days[d.index]);
          var events_per_day = "api/events/day/" + source + "/" + days[d.index];
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
                    <EventsList data={this.state.data} key={this.props.id}/>
                    </div>
                );
              }
            });

            var EventsList = React.createClass({
              render: function(){
                //console.log(this.props.data[0]);
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
          ReactDOM.render(
              <EventsComponent url={events_per_day} pollInterval={60000} />,
              document.getElementById('sub-content')
            );
        },
        type: 'area-spline'
      },
      subchart: {
        show: true
      },
      axis: {
        x: {
          type: 'category'
        }
      }
    });
  },
  render: function() {
    return(<div className="c3-chart"></div>);
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
        <VisualizationsList data={this.state.data} key={this.state.id}/>
        </div>
    );
  }
});

var VisualizationsList = React.createClass({
  render: function(){
    var my_set = new Set();
    var visualizationNodes = this.props.data.map(function(visualization){
      return (
        my_set.add(visualization.Date),
          <Visualization data={visualization} set={my_set} key={visualization.id}/>
        //<Visualization Date={visualization.Date} Day={visualization.Name_Day} ID_Source={visualization.ID_Source} Hour={visualization.Hour} Events={visualization.Process_Events} key={visualization.id} />
      );
    });
    return (
        <div className="visualizationsList">
        {visualizationNodes}
        </div>
    );
  }
});



ReactDOM.render(
  //<EventsComponent url="api/events/" pollInterval={10000} />,
    <VisualizationsComponent url="api/visualizations/week/" pollInterval={60000} />,
  document.getElementById('content')
);
