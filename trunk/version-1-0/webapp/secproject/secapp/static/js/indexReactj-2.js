var Parent = React.createClass({
              render: function() {
                return (
                    <EventsComponent source={this.props.ID_Source} date={this.props.Date} url={web + this.props.ID_Source + "/" + this.props.Date} key={this.props.id} pollInterval={60000} />
                  /*  <div className="parent">
                    <div className="parentDate">
                    {this.props.Date}
                  </div>
                    <div className="parentEvents">
                    {this.props.Events}
                  </div>
                    <div className="parentDay">
                    {this.props.Day}
                  </div>
                   </div>*/
                );
              }
            });

            var ParentComponent = React.createClass({
              loadParentFromServer: function(){
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
                this.loadParentFromServer();
                setInterval(this.loadParentFromServer, this.props.pollInterval);
              },
              render: function(){
                var testStyle = { fontSize: '18px', marginRight: '20px' };
                return (
                    <div className="parentComponent" style={testStyle}>
                    <h1>Parent</h1>
                    <ParentList data={this.state.data} key={this.state.id}/>
                    </div>
                );
              }
            });

            var ParentList = React.createClass({
              render: function(){
                console.log("ENTRO POR AQUÍ");
                var count = 0;
                var parentNodes = this.props.data.map(function(parent){
                    return (<li><Parent ID_Source={parent.id_source} Date={parent.date} Events={parent.events} Day={parent.day} key={parent.id} /></li>);
                });
                console.log("PARENT NODES", parentNodes);
                return (
                    <div className="parentList">
                    <ul>
                    {parentNodes}
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
                    console.error(web + this.props.day + "/"+ this.props.date, status, err.toString());
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
                    <EventsList data={this.state.data} key={this.state.id}/>
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
                <ParentComponent url="api/visualizations/chart/" pollInterval={60000} />,
                //<EventsComponent url="api/events/" pollInterval={10000} />,
              document.getElementById('sub-content')
            );
