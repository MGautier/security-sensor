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

//React.render(
//    <EventsComponent url="api/events/" pollInterval={10000} />,
//  document.getElementById('content')
//);
