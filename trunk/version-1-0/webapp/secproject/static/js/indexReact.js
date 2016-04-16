/*setTimeout(function () {
 c3.generate({
 data: {
 url: 'api/visualizations/week.json',
 mimeType: 'json',
 keys: {
 x: 'Name_Day',
 value: ['Process_Events']
 }
 },
 axis: {
 x: {
 type: 'category'
 }
 }
 });
 }, 1000);*/

/*var chart = c3.generate({
 data: {
 url: [
 ['data1', 300, 350, 300, 0, 0, 0],
 ['data2', 130, 100, 140, 200, 150, 50]
 ],
 types: {
 data1: 'area',
 data2: 'area-spline'
 }
 }
 });*/


/*var Visualization = React.createClass({
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
 });*/

var Visualization = React.createClass({
  render: function() {
    return(
      c3.generate({
        data: {
          url: 'api/visualizations/chart.json/',
          mimeType: 'json',
          selection: {
            enabled: true
          },
          onclick: function (d, data, element){

            var JSON = React.createClass({
              render: function() {
                return (<Event url="api/visualizations/chart.json"/>);
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

            ReactDOM.render(
              console.log("ON-RENDER",d),
                <EventsComponent url="api/events/" pollInterval={10000} />,
              document.getElementById('sub-content')
            );
          },
          keys: {
            x: 'day',
            value: ['events']
          },
          names: {
            events: 'Iptables Events'
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
      })
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



ReactDOM.render(
  //<EventsComponent url="api/events/" pollInterval={10000} />,
    <VisualizationsComponent url="api/visualizations/week/" pollInterval={60000} />,
  document.getElementById('content')
);
