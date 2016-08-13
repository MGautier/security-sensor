/* --- Extra functions --- */
function format ( d ){
  var rows = '';

  d.forEach(function (item, index, array) {

    var packet_information = '<tr><td><b>Tag</b>:</td><td>'+item['Tag']+'</td><td><b>Description</b>:</td><td>'+item['Description']+'</td><td><b>Value</b>:</td><td>'+item['Value']+'</td></tr>';
    rows = rows + packet_information;
  });

  return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;" width=100%>'+
    rows+
    '</table>';
}
/* ---                 --- */

var VisualizationsComponent = React.createClass({
  getInitialState: function(){
    //console.log("InitialState");
    return {data: [], mounted: true};
  },
  getDefaultProps: function(){
    //console.log("DefaultProps", this.props);
  },
  loadVisualizationsFromServer: function(){
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        if (this.isMounted()){
          this.setState({data: data});
          var ajax_data = this.state.data;
          var chart_data = []; // [Timestamp, Events, index, ID_Source, Date(YYYY-MM-DD)]
          var index_chart_data = []; // [Timestamp] - Usado para indexar la posicion de la abscisa (x)
          var normalize_char_data = []; // [Timestamp, Events]
          var it = 0;
          ajax_data.forEach(function (item, index, list) {
            chart_data.push([Date.UTC(item.Year,item.Month-1,item.Day),item.Events,it,item.ID_Source,item.Date]);
            index_chart_data.push(Date.UTC(item.Year,item.Month-1,item.Day));
            normalize_char_data.push([Date.UTC(item.Year,item.Month-1,item.Day),item.Events]);
            it++;
          });

          $(document).ready(function () {

            /**
             * Sand-Signika theme for Highcharts JS
             * @author Torstein Honsi
             */

            // Load the fonts
            Highcharts.createElement('link', {
              href: 'https://fonts.googleapis.com/css?family=Signika:400,700',
              rel: 'stylesheet',
              type: 'text/css'
            }, null, document.getElementsByTagName('head')[0]);

            // Add the background image to the container
            Highcharts.wrap(Highcharts.Chart.prototype, 'getContainer', function (proceed) {
              proceed.call(this);
            });


            Highcharts.theme = {
              colors: ["#f45b5b", "#8085e9", "#8d4654", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
                       "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
              chart: {
                backgroundColor: null,
                style: {
                  fontFamily: "Signika, serif"
                }
              },
              title: {
                style: {
                  color: 'black',
                  fontSize: '16px',
                  fontWeight: 'bold'
                }
              },
              subtitle: {
                style: {
                  color: 'black'
                }
              },
              tooltip: {
                borderWidth: 0
              },
              legend: {
                itemStyle: {
                  fontWeight: 'bold',
                  fontSize: '13px'
                }
              },
              xAxis: {
                labels: {
                  style: {
                    color: '#6e6e70'
                  }
                }
              },
              yAxis: {
                labels: {
                  style: {
                    color: '#6e6e70'
                  }
                }
              },
              plotOptions: {
                series: {
                  shadow: true
                },
                candlestick: {
                  lineColor: '#404048'
                },
                map: {
                  shadow: false
                }
              },

              // Highstock specific
              navigator: {
                xAxis: {
                  gridLineColor: '#D0D0D8'
                }
              },
              rangeSelector: {
                buttonTheme: {
                  fill: 'white',
                  stroke: '#C0C0C8',
                  'stroke-width': 1,
                  states: {
                    select: {
                      fill: '#D0D0D8'
                    }
                  }
                }
              },
              scrollbar: {
                trackBorderColor: '#C0C0C8'
              },

              // General
              background2: '#E0E0E8'

            };

            // Apply the theme
            Highcharts.setOptions(Highcharts.theme);

            $('#container').highcharts({
              chart: {
                zoomType: 'x',
                plotShadow: true
              },
              title: {
                text: 'Events processing by source'
              },
              subtitle: {
                text: document.ontouchstart === undefined ?
                  'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
              },
              xAxis: {
                type: 'datetime'
              },
              yAxis: {
                title: {
                  text: 'Events'
                }
              },
              legend: {
                enabled: true,
                align: 'right',
                layout: 'vertical',
                verticalAlign: 'middle',
                borderWidth: 0
              },
              plotOptions: {
                area: {
                  fillColor: {
                    linearGradient: {
                      x1: 0,
                      y1: 0,
                      x2: 0,
                      y2: 1
                    },
                    stops: [
                      [0, Highcharts.getOptions().colors[0]],
                      [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                  },
                  marker: {
                    radius: 2
                  },
                  lineWidth: 1,
                  states: {
                    hover: {
                      lineWidth: 1
                    }
                  },
                  threshold: null
                },
                series: {
                  allowPointSelect: true
                }
              },
              series: [
                {
                  name: 'Events iptables',
                  data: normalize_char_data,
                  point: {
                    events: {
                      select: function(event)
                      {
                        var index = index_chart_data.indexOf(this.x);

                        var events_per_day = "api/packets/"+chart_data[index][3]+"/"+chart_data[index][4];
                        var stadistics_per_day = "api/stadistics/"+chart_data[index][3]+"/"+chart_data[index][4];
                        console.log("STADISTICS-DAY: ", stadistics_per_day);

                        var ajax_stadistics = [];

                        $(document).ready(function() {
                          var show_events_button = this.getElementById("update-events");
                          var show_events_table = this.getElementById("events-table");
                          var show_stadistics = this.getElementById("interaction");
                          var get_select = this.getElementById("stadistics-select");

                          $('#stadistics').highcharts({
                            title: {
                              text: 'Stadistics packets - '+chart_data[index][4]
                            }
                          });


                          /*---           Visualizaciones        ---*/
                          show_events_button.style.display = "none";
                          show_events_table.style.display = "none";
                          show_stadistics.style.display = "none";

                          show_events_button.style.display = "flex";
                          show_events_table.style.display = "table";
                          show_stadistics.style.display = "";
                          /*---                                  ---*/
                          /*---           Asignaciones           ---*/


                          /*---                                  ---*/
                          /*---           Estadisticas           ---*/

                          $("#stadistics-show-button").on( "click", function( event ){
                            var $glyphicon = $(this).find(".glyphicon.glyphicon-repeat"),
                                animateClass = "glyphicon-refresh-animate";

                            var option_selected = get_select.options[get_select.selectedIndex].value;


                            $glyphicon.addClass( animateClass );
                            // Se establece el Timeout para indicar que sea asincrona
                            console.log("SOURCE: ", chart_data[index][3]);
                            console.log("DAY: ", chart_data[index][4]);
                            console.log("STADISTICS-2: ", stadistics_per_day);
                            $.ajax({
                              url: stadistics_per_day,
                              dataType: 'json',
                              cache: false,
                              success: function(data) {
                                console.log("SOURCE-2: ", chart_data[index][3]);
                                console.log("DAY-2: ", chart_data[index][4]);

                                if (option_selected != '-')
                                {
                                  ajax_stadistics = [];
                                  var array_stadistics = data[option_selected];
                                  var hits_or_frequency = 'Hits';

                                  if (option_selected == 'Timestamps')
                                  {
                                    hits_or_frequency = 'Frequency';
                                  }

                                  var size = array_stadistics.length;

                                  var value = [];
                                  if (size == 1)
                                  {
                                    value.push(100.0);
                                  }
                                  else
                                  {
                                    if (size > 1)
                                    {
                                      var sum = 0;
                                      array_stadistics.forEach(function (item, index, array){
                                        sum = sum + item[hits_or_frequency];
                                      });

                                      array_stadistics.forEach(function (item, index, array){
                                        var operation = (item[hits_or_frequency] * 100) / sum;

                                        value.push(operation.toFixed(2));
                                      });
                                    }
                                  }

                                  if (option_selected == 'Timestamps')
                                  {
                                    array_stadistics.forEach(function (item, index, array) {
                                      ajax_stadistics.push([
                                        'Hour: '+item['Hour']+' - '+hits_or_frequency+': '+item[hits_or_frequency],
                                        parseFloat(value[index])
                                      ]);
                                    });
                                  }
                                  else
                                  {
                                    array_stadistics.forEach(function (item, index, array) {
                                      ajax_stadistics.push([
                                        option_selected+': '+item[option_selected]+' - '+hits_or_frequency+': '+item[hits_or_frequency],
                                        parseFloat(value[index])
                                      ]);
                                    });
                                  }

                                  console.log("AJAX-STADISTICS: ", ajax_stadistics);
                                }
                              }.bind(this),
                              error: function(xhr, status, err){
                                console.error(stadistics_per_day, status, err.toString());
                              }.bind(this)
                            });

                            window.setTimeout( function(){
                              $glyphicon.removeClass( animateClass );

                              $('#stadistics').highcharts({
                                chart: {
                                  type: 'pie',
                                  options3d: {
                                    enabled: true,
                                    alpha: 45,
                                    beta: 0
                                  }
                                },
                                title: {
                                  text: 'Stadistics packets - '+chart_data[index][4]
                                },
                                tooltip: {
                                  pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                                },
                                plotOptions: {
                                  pie: {
                                    allowPointSelect: true,
                                    cursor: 'pointer',
                                    depth: 35,
                                    dataLabels: {
                                      enabled: true,
                                      format: '{point.name}'
                                    }
                                  }
                                },
                                series: [{
                                  type: 'pie',
                                  name: 'Percentage',
                                  data: ajax_stadistics
                                }]
                              });

                            }, 7000 );

                          });

                          /*---                                 ---*/

                          var table = $('#events-table').DataTable({
                            retrieve: true,
                            order: [[1, 'asc']],
                            ajax:{
                              url: events_per_day,
                              dataSrc: ''
                            },
                            scrollY: "650px",
                            scrollX: true,
                            scrollCollapse: true,
                            columns: [
                              {
                                className: "details-control",
                                data: 'id',
                                render: "[, ]",
                                defaulContent: null
                              },
                              { data: 'id' },
                              { data: 'Local_Timestamp' },
                              { data: 'Comment' },
                              { data: 'IP_Source' },
                              { data: 'IP_Destination' },
                              { data: 'Port_Source' },
                              { data: 'Port_Destination' },
                              { data: 'Protocol' },
                              { data: 'MAC_Source' },
                              { data: 'MAC_Destination' },
                              { data: 'TAG' }

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


                          $('#events-table tbody').on('click', 'tr td.details-control', function(){
                            var tr = $(this).closest('tr');
                            var row = table.row( tr );
                            $.ajax({
                              url: "api/events/"+row.data().id+"/additional",
                              dataType: 'json',
                              cache: false,
                              success: function(data) {
                                tr.addClass('shown');
                                row.child( format(data) ).show();
                              }.bind(this),
                              error: function(xhr, status, err){
                                console.error(this.props.url, status, err.toString());
                              }.bind(this)
                            });

                          });
                          $('#events-table tbody').on('dblclick', 'tr td.details-control', function(){
                            var tr = $(this).closest('tr');
                            var row = table.row( tr );
                            $.ajax({
                              url: "api/events/"+row.data().id+"/additional",
                              dataType: 'json',
                              cache: false,
                              success: function(data) {
                                tr.removeClass('shown');
                                row.child.hide();
                              }.bind(this),
                              error: function(xhr, status, err){
                                console.error(this.props.url, status, err.toString());
                              }.bind(this)
                            });

                          });

                        } );

                      },
                      unselect: function(event) {
                        var p = this.series.chart.getSelectedPoints();

                        if(p.length > 0 && p[0].x == this.x) {
                          //console.log('point unselected');
                        }
                      }
                    }
                  }
                }
              ]
            });
          });
        }
      }.bind(this),
      error: function(xhr, status, err){
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  update: function(){
    //console.log("update");
  },
  render: function(){
    //console.log("render");
    return (
        <div className="visualizationsComponent">
        <h1>Visualizations</h1>
        </div>
    );
  },
  componentWillMount: function() {
    //console.log("WillMount");
  },
  componentDidMount: function(){
    //console.log("DidMount");
    this.loadVisualizationsFromServer();
    setInterval(this.loadVisualizationsFromServer, this.props.pollInterval);
  },
  shouldComponentUpdate: function(nextProps, nextState){
    //console.log("shouldComponentUpdate", nextProps);
    //console.log("shouldComponentUpdate2", nextState);
    return true;
  },
  componentWillReceieveProps: function(nextProps){
    //console.log("willReceiveProps: ", nextProps);
  },
  componentWillUpdate: function(nextProps, nextState){
    //console.log("willUpdate", nextProps);
    //console.log("willUpdate2", nextState);
    //this.unmountComponentAtNode(document.getElementById('content'));
  },
  componentDidUpdate: function(prevProps, prevState){
    //console.log("DidUpdate", prevProps);
    //console.log("DidUpdate2", prevState);
  },
  componentWillUnmount: function(){
    //console.log("WillUnmount");
  }

});

ReactDOM.render(
    <VisualizationsComponent url="api/visualizations/1/chart_all/" pollInterval={90000} />,
  document.getElementById('content')
);
// 90000 -> 2 min 30 sec
