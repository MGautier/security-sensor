c3.generate({
  data: {
    url: 'api/visualizations/chart.json/',
    mimeType: 'json',
    selection: {
      enabled: true
    },
    onclick: function (d, element){
      console.log("D",d);
      console.log("element",element);
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
});
