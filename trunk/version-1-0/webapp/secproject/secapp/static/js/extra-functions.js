var hola = 1;

$(function () {
  $(document).ready(function () {
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
      global: {
        useUTC: false
      },
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

    $('#seconds').highcharts({
      chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
          load: function () {

            // set up the updating of the chart each 2,5 seconds
            var series = this.series[0];
            var ajax_data = 0;
            $.ajax({
              url: "api/events/hour/1",
              dataType: 'json',
              cache: false,
              success: function(data) {
                ajax_data = data[0].Events;
              }.bind(this),
              error: function(xhr, status, err){
                console.error(this.props.url, status, err.toString());
              }.bind(this)
            });
            setInterval(function () {
              var x = (new Date()).getTime(), // current time
                  y = ajax_data;
              console.log("Y: ",y);
              console.log("RANDOM");
              series.addPoint([x, y], true, true);
            }, 2500);
          }
        }
      },
      title: {
        text: 'Events on live'
      },
      xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
      },
      yAxis: {
        title: {
          text: 'Events'
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
        name: 'Events Iptables'+hola,
        data: (function () {
          // generate an array of random data previous load
          // events
          // este array de datos se muestra previo a la carga
          // de información por parte del setInterval de arriba

          console.log("DATA RANDOM");
          var data = [],
              time = (new Date()).getTime(),
              i;

          for (i = -19; i <= 0; i += 1) {
            data.push({
              x: time + i * 2500,
              y: Math.random()
            });
          }
          return data;
        }())
      }]
    });
  });
});
