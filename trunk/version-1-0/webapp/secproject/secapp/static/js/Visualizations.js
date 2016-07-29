/* --- Extra functions --- */
function format ( d ){
  var rows = '';

  d.Additional.forEach(function (item, index, array) {

    var packet_information = '<tr><td>Tag:</td><td>'+item['Tag']+'</td><td>Description:</td><td>'+item['Description']+'</td><td>Value:</td><td>'+item['Value']+'</td></tr>';
    rows = rows + packet_information;
  });
  console.log("ROW: ",rows);
  return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;" width=100%>'+
    rows+
    '</table>';
}
/* ---                 --- */

var Info = React.createClass({
  render: function() {
    return (
        <div className="info">
        <p>Tag: {this.props.data.Tag} Value: {this.props.data.Value} Description: {this.props.data.Description}</p>
        </div>
    );
  }
});

var InfoComponent = React.createClass({
  loadInfoFromServer: function(){
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
    this.loadInfoFromServer();
    setInterval(this.loadInfoFromServer, this.props.pollInterval);
  },
  render: function(){
    return (
        <div className="infoComponent">
        <h1>Info</h1>
        <p>ID: {this.props.data.id}</p>
        <InfoList key={this.props.id} data={this.state.data}/>
        </div>
    );
  }
});

var InfoList = React.createClass({
  render: function(){
    var infoNodes = this.props.data.map(function(event){
      return (
          <li><Info key={event.id} data={event} /></li>
      );
    });
    return (
        <div className="infoList">
        <ol>
        {infoNodes}
      </ol>
        </div>
    );
  }
});

var Event = React.createClass({
  handleClick: function(event){
    console.log("ON CLICK");
    console.log("Timestamp: ", this.props.data.Local_Timestamp);
    console.log("ID: ", this.props.data.id);
    var additional_info = "api/events/" + this.props.data.id + "/additional";

    ReactDOM.unmountComponentAtNode(document.getElementById('infoComponent'));
    ReactDOM.render(
        <InfoComponent url={additional_info} data={this.props.data} pollInterval={60000} />,
      document.getElementById('infoComponent')
    );


  },
  render: function() {
    return (
        <div className="event">
        <a onClick={this.handleClick}><u><p className="event-description"> ID-Event: {this.props.data.id} - Timestamp: {this.props.data.Local_Timestamp} - Comment: {this.props.data.Comment} </p></u></a>
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
        console.log("IS-MOUNTED: ", this.isMounted());
        if(this.isMounted())
        {
          console.log("HERE");
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
          <li><div><Event key={event.id} data={event} /></div></li>
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


var Visualization = React.createClass({
  componentDidMount: function() {
    var days = Array.from(this.props.set);
    var source = this.props.data.ID_Source;
    var auxiliar_d;
    var auxiliar_element;
    c3.generate({
      data: {
        url: 'api/visualizations/1/chart_all.json/',
        mimeType: 'json',
        selection: {
          enabled: true
        },
        keys: {
          x: 'Date',
          value: ['Events']
        },
        names: {
          Events: 'Iptables Events'
        },
        onclick: function (d, element){
          var events_per_day = "api/packets/" + source + "/" + days[d.index];

          ReactDOM.unmountComponentAtNode(document.getElementById('eventComponent'));
          ReactDOM.unmountComponentAtNode(document.getElementById('infoComponent'));

          $(document).ready(function() {
            var show_events_button = this.getElementById("update-events");
            var show_events_table = this.getElementById("events-table");
            show_events_button.style.display = "flex";
            show_events_table.style.display = "table";

            var table = $('#events-table').DataTable({
              retrieve: true,
              order: [[1, 'asc']],
              ajax:{
                url: events_per_day,
                dataSrc: ''
              },
              columns: [
                {
                  className: 'details-control',
                  data: 'id',
                  render: "[, ]",
                  defaulContent: null
                },
                { data: 'id' },
                { data: 'Local_Timestamp' },
                { data: 'Comment'}
              ]
            });
            table.ajax.url( events_per_day ).load();

            $("#update-events-button").on( "click", function( event ){
              var $glyphicon = $(this).find(".glyphicon.glyphicon-refresh"),
                  animateClass = "glyphicon-refresh-animate";

              $glyphicon.addClass( animateClass );
              // Se establece el Timeout para indicar que sea asincrona
              window.setTimeout( function(){
                $glyphicon.removeClass( animateClass );
                table.ajax.url( events_per_day ).load();
              }, 2000 );

            });

            $('#events-table tbody').on('click', 'td.details-control', function(){
              var tr = $(this).closest('tr');
              var row = table.row( tr );

              if ( row.child.isShown() ){
                row.child.hide();
                tr.removeClass('shown');
              }
              else{
                row.child( format(row.data()) ).show();
                tr.addClass('shown');
              }
            })

          } );

        },
        type: 'area-spline'
      },
      subchart: {
        show: true
      },
      axis: {
        x: {
          type: 'category',
          tick: {
            rotate: -80,
            multiline: false
          },
          height: 68
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
        else{
          ReactDOM.unmountComponentAtNode(document.getElementById('visualizationsComponent'));
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
    <VisualizationsComponent url="api/visualizations/1/chart_all/" pollInterval={60000} />,
  document.getElementById('content')
);
