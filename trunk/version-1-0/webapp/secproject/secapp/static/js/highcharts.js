var timestamp = Date.UTC(2016,7,30);
console.log("TIMESTAMP: ", timestamp);
var array = [];
var array_2 = [];
for (var i=0; i < 31; i++){
  var aux = Date.UTC(2016,7,i);
  var aux_2 = Date.UTC(2016,6,i);
  array.push([aux,i]);
  array_2.push([aux_2,i]);
}
console.log("ARRAY: ", array);

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
    this.container.style.background = 'url(http://www.highcharts.com/samples/graphics/sand.png)';
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
      text: 'USD to EUR exchange rate over time'
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
        text: 'Exchange rate'
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
        type: 'area',
        name: 'USD to EUR',
        data: array,
        point: {
          events: {
            select: function(event) {
              console.log('point selected @ ' + this.x + ', '+ this.y);
            },
            unselect: function(event) {
              var p = this.series.chart.getSelectedPoints();
              if(p.length > 0 && p[0].x == this.x) {
                console.log('point unselected');
              }
            }
          }
        }
      },
      {
        type: 'area',
        name: 'EUR to USD',
        data: array_2,
        point: {
          events: {
            select: function(event) {
              console.log('point selected @ ' + this.x + ', '+ this.y);
            },
            unselect: function(event) {
              var p = this.series.chart.getSelectedPoints();
              if(p.length > 0 && p[0].x == this.x) {
                console.log('point unselected');
              }
            }
          }
        }
      }
    ]
  });
});
