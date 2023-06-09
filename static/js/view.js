let last_data=0;
var data_count=0;
let plotted_full=0;
let plotted_window=0;
let uplot = undefined;
let uplot_window = undefined;
let uplot_current = undefined;
var imin = 150;
var imax = 2000;
let startup_time = "something";
var window_size = 25;

var data = [[],[],[],[],];

var data_window = [[],[],[],];
var data_current = [[],[],[],[],];

let size = document.getElementById("plot").getBoundingClientRect()
let big_width = size.width;

function data_print(datad)
{
  //document.getElementById("volt").textContent = dat time: false,ad.fetch;
}

function json_read(farts)
{
    //console.log(farts)
    if(farts.length ==0)
    {
      return
    }

    document.getElementById("voltage").textContent = Math.round(farts[farts.length - 1]["Target Voltage"]*100)/100;
    document.getElementById("cap-voltage").textContent = Math.round(farts[farts.length - 1]["Cap Voltage"]*100)/100;
    document.getElementById("cap-current").textContent = Math.round(farts[farts.length - 1]["DMM Current"]*100)/100;

    document.getElementById("psu-voltage").textContent = Math.round(farts[farts.length - 1]["PSU Voltage"]*100)/100;
    document.getElementById("psu-current").textContent = Math.round(farts[farts.length - 1]["PSU Current"]);

    last_data=farts[farts.length - 1]["time                    "];

    farts.forEach((value) => {
      data_count++;
      data[0].push(value["time                    "]);
      data[1].push(value["Target Voltage"]);
      data[2].push(value["Cap Voltage"]);
      data[3].push(value["DMM Current"]);
    });

    data_window = [[],[],[],];
    data_current = [[],[],[],[],];
    if(data_count > window_size){
      console.log("Enough data")
      for (let step = 0; step < window_size; step++)
      {
        // Voltage window
        data_window[0].push(data[0][data[0].length-window_size+step]);
        data_window[1].push(data[1][data[1].length-window_size+step]);
        data_window[2].push(data[2][data[2].length-window_size+step]);
        // Current window
        data_current[0].push(data[0][data[0].length-window_size+step]);
        data_current[1].push(imin);
        data_current[2].push(imax);
        data_current[3].push(data[3][data[3].length-window_size+step]);
      }
      if (plotted_window==0)
      {
      console.log("not plotted")
          plotted_window=1;
          uplot_window = new uPlot(opts_window, data_window, document.getElementById("voltage_window"));
          uplot_current = new uPlot(opts_current, data_current, document.getElementById("current_window"));
      }else{
        uplot_window.setData(data_window);
        uplot_current.setData(data_current);
        console.log("update window")
      }
    }else{
      console.log("Not Enough data: "+data_count )
    }

    if ((data_count > 1) && (plotted_full==0))
    {
        plotted_full=1;
        uplot = new uPlot(opts_full, data, document.getElementById("voltage_full"));
    }

    if (data_count > 1)
    {
        uplot.setData(data);
    }

}


function data_fetch()
{
  fetch('/data.json?time='+last_data)
    .then((response) => response.json())
    .then((data) => json_read(data));

  window_size = document.getElementById('window_values').value;


  setTimeout(data_fetch,1000)
}

setTimeout(data_fetch,1000)


function control_read(control_json)
{
    //console.log(farts)
    if(control_json.length ==0)
    {
      return
    }

    if (startup_time == "something")
    {
        if (data[0][0] != undefined) {
            startup_time = data[0][0];
        }
     }else if(startup_time != control_json["start_time"])
     {
       //console.log('Insert reload here st['+startup_time+']')
       window.location.reload()
     }
     document.getElementById("voltage-max").textContent = Math.round(control_json["voltage"]*100)/100;
     document.getElementById("imin").textContent = Math.round(control_json["imin"]*100)/100;
     imin = Math.round(control_json["imin"]*100)/100;
     document.getElementById("imax").textContent = Math.round(control_json["imax"]*100)/100;
     imax = Math.round(control_json["imax"]*100)/100;

    //console.log(control_json)
}

function control_fetch()
{
  fetch('/control.json')
    .then((response) => response.json())
    .then((control) => control_read(control));
}

setInterval(control_fetch,1000)






let opts_full = {
  title: "Full Test Data (Voltages)",
  //id: "voltage_full",
  class: "my-chart",
  width: big_width*0.66,
  height: 700,
  series: [
    {},
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: true,

      // in-legend display
      label: "Target",
      value: (u, v) => v == null ? null : v + " V",

      // series style
      stroke: "red",
      width: 3,
      fill: "rgba(255, 0, 0, 0)",
      dash: [0, 0],
    },
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: false,

      // in-legend display
      label: "Cap",
      value: (u, v) => v == null ? null : v + " V",

      // series style
      stroke: "blue",
      width: 3,
      fill: "rgba(0, 0, 0, 0)",
      dash: [0, 0],
    }
  ],
};


let opts_window = {
  title: "Window of Test Data (Voltages)",
  //id: "voltage_window",
  class: "my-chart",
  width: big_width*0.3,
  height: 300,
  series: [
    {},
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: true,

      // in-legend display
      label: "Target",
      value: (u, v) => v == null ? null : v + " V",

      // series style
      stroke: "red",
      width: 3,
      fill: "rgba(255, 0, 0, 0)",
      dash: [0, 0],
    },
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: false,

      // in-legend display
      label: "Cap",
      value: (u, v) => v == null ? null : v + " V",

      // series style
      stroke: "blue",
      width: 3,
      fill: "rgba(0, 0, 0, 0)",
      dash: [0, 0],
    }
  ],
};


let opts_current = {
  title: "Window of Capacitor charge (Current)",
  //id: "voltage_window",
  class: "my-chart",
  width: big_width*0.3,
  height: 300,
  series: [
    {},
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: true,

      // in-legend display
      label: "I-Min",
      value: (u, v) => v == null ? null : v + " μA",

      // series style
      stroke: "red",
      width: 3,
      fill: "rgba(255, 0, 0, 0)",
      dash: [0, 0],
    },
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: false,

      // in-legend display
      label: "I-Max",
      value: (u, v) => v == null ? null : v + " μA",

      // series style
      stroke: "blue",
      width: 3,
      fill: "rgba(0, 0, 0, 0)",
      dash: [0, 0],
    },
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: false,

      // in-legend display
      label: "I",
      value: (u, v) => v == null ? null : v + " μA",

      // series style
      stroke: "green",
      width: 3,
      fill: "rgba(0, 0, 0, 0)",
      dash: [0, 0],
    }
  ],
};
