let last_data=0
let data_count=0
let plotted=0
let uplot = undefined;
var imin = 150;
var imin = 2000;
let startup_time = "something";

var data = [[],[],[],];

var data_window = [[],[],[],];

function data_print(datad)
{
  //document.getElementById("volt").textContent = datad.fetch;
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
      data_window[0].push(value["time                    "]);
      data_window[1].push(value["Target Voltage"]);
      data_window[2].push(value["Cap Voltage"]);

      if (data_count > 100)
      {
        data_window[0].shift();
        data_window[1].shift();
        data_window[2].shift();
      }
      console.log(data)
    });

    if ((data_count > 1) && (plotted==0))
    {
        plotted=1;
        uplot = new uPlot(opts, data, document.body);
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
}

setInterval(data_fetch,1000)


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
     document.getElementById("imax").textContent = Math.round(control_json["imax"]*100)/100;

    //console.log(control_json)
}

function control_fetch()
{
  fetch('/control.json')
    .then((response) => response.json())
    .then((control) => control_read(control));
}

setInterval(control_fetch,1000)






let opts = {
  title: "My Chart",
  id: "plot",
  class: "my-chart",
  width: 1200,
  height: 600,
  series: [
    {},
    {
      // initial toggled state (optional)
      show: true,

      spanGaps: true,

      // in-legend display
      label: "Target Voltage",
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
      label: "Cap Voltage",
      value: (u, v) => v == null ? null : v + " V",

      // series style
      stroke: "blue",
      width: 3,
      fill: "rgba(0, 0, 0, 0)",
      dash: [0, 0],
    }
  ],
};
