var Visualization = React.createClass({
  componentDidMount: function() {
    var days = Array.from(this.props.set);
    var source = this.props.data.ID_Source;
    var auxiliar_d;
    var auxiliar_element;
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
        onmouseover: function (d, element){
          var events_per_day = "api/events/day/" + source + "/" + days[d.index];
          var Event = React.createClass({
            handleClick: function(event){
              console.log("ON CLICK");
            },
            render: function() {
              return (
                  <div className="event">
                  <p onClick={this.handleClick} >ID-Event: {this.props.data.id} - Timestamp: {this.props.data.Local_Timestamp} - Comment: {this.props.data.Comment} </p>
                  </div>
              );
            }
          });

          var EventsComponent = React.createClass({
            loadEventsFromServer: function(){
              $.ajax({
                url: this.props.url,
                dataType: 'json',
                cache: true,
                success: function(data) {
                  if(this.isMounted())
                  {
                    this.setState({data: data});

                  }
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
              return (
                  <div className="eventsComponent">
                  <h1>Events</h1>
                  <EventsList key={this.props.id} data={this.state.data}/>
                  </div>
              );
            }
          });

          var EventsList = React.createClass({
            render: function(){
              var eventNodes = this.props.data.map(function(event){
                return (
                    <li><a href="#"><Event key={event.id} data={event} /></a></li>
                );
              });
              return (
                  <div className="eventsList">
                  <ol className="rectangle-list">
                  {eventNodes}
                </ol>
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
  getInitialState: function(){
    console.log("InitialState");
    return {data: [], mounted: true};
  },
  getDefaultProps: function(){
    console.log("DefaultProps", this.props);
  },
  loadVisualizationsFromServer: function(){
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        if (this.isMounted()){
          this.setState({data: data});
        }
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  update: function(){
    console.log("update");
  },
  render: function(){
    console.log("render");
    var testStyle = { fontSize: '18px', marginRight: '20px' };
    return (
        <div className="visualizationsComponent" style={testStyle}>
        <h1>Visualizations</h1>
        <VisualizationsList data={this.state.data} key={this.state.id}/>
        </div>
    );
  },
  componentWillMount: function() {
    console.log("WillMount");
  },
  componentDidMount: function(){
    console.log("DidMount");
    this.loadVisualizationsFromServer();
    setInterval(this.loadVisualizationsFromServer, this.props.pollInterval);
  },
  shouldComponentUpdate: function(nextProps, nextState){
    console.log("shouldComponentUpdate", nextProps);
    console.log("shouldComponentUpdate2", nextState);
    return true;
  },
  componentWillReceieveProps: function(nextProps){
    console.log("willReceiveProps: ", nextProps);
  },
  componentWillUpdate: function(nextProps, nextState){
    console.log("willUpdate", nextProps);
    console.log("willUpdate2", nextState);
    //this.unmountComponentAtNode(document.getElementById('content'));

  },
  componentDidUpdate: function(prevProps, prevState){
    console.log("DidUpdate", prevProps);
    console.log("DidUpdate2", prevState);
  },
  componentWillUnmount: function(){
    console.log("WillUnmount");
  }

});

var VisualizationsList = React.createClass({
  render: function(){
    var my_set = new Set();
    var visualizationNodes = this.props.data.map(function(visualization){
      return (
        my_set.add(visualization.Date),
          <Visualization data={visualization} set={my_set} key={visualization.id}/>
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
    <VisualizationsComponent url="api/visualizations/week/" pollInterval={60000} />,
  document.getElementById('content')
);
