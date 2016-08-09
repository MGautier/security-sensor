$(function () {

  var ajax_data = [];
  var SecondsComponent = React.createClass({
    getInitialState: function(){
      //console.log("InitialState");
      return {data: [], mounted: true};
    },
    getDefaultProps: function(){
      //console.log("DefaultProps", this.props);
    },
    loadSecondsFromServer: function(){
      $.ajax({
        url: this.props.url,
        dataType: 'json',
        cache: false,
        success: function(data) {
          if (this.isMounted())
          {
            this.setState({data: data});
            ajax_data = this.state.data;
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
          <div>
          </div>
      );
    },
    componentWillMount: function() {
      //console.log("WillMount");
    },
    componentDidMount: function(){
      //console.log("DidMount");
      this.loadSecondsFromServer();
      setInterval(this.loadSecondsFromServer, this.props.pollInterval);
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
      <SecondsComponent url="api/events/hour/1" pollInterval={2500} />,
    document.getElementById('seconds')
  );

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
      global: {
        useUTC: false
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

    $('#seconds').highcharts({
      chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
          load: function () {
            // set up the updating of the chart each second

            var series = this.series[0];

            setTimeout(function(){
              setInterval(function () {
                var x = (new Date()).getTime(); // current time

                var y;
                if ( ajax_data.length == 0 )
                {
                  y = 0;
                }else{
                  y = ajax_data[0].Events;
                }

                series.addPoint([x, y], true, true);
                series.show();

              }, 2700);

              series.setData(
                (function () {
                  // generate an array of random data
                  var data = [],
                      time = (new Date()).getTime(),
                      i;
                  for (i = -19; i <= 0; i += 1) {
                    data.push({
                      x: time + i * 1000,
                      y: Math.random()
                    });
                    console.log("X: ", time + i * 1000);
                    console.log("Y: ", Math.random());

                  }

                  return data;
                }())
              );

            }, 2000);

          }
        }
      },
      title: {
        text: 'Live Events Iptables'
      },
      xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
      },
      yAxis: {
        title: {
          text: 'Value'
        },
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      },
      tooltip: {
        formatter: function () {
          return '<b>' + this.series.name + '</b><br/>' +
            Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
            Highcharts.numberFormat(this.y, 2);
        }
      },
      legend: {
        layout: 'horizontal',
        align: 'center',
        verticalAlign: 'bottom',
        borderWidth: 0
      },
      exporting: {
        enabled: false
      },
      series: [{
        name: 'Events Iptables',
        data: []
      }]
    });
  });
});
