let last_data=0
let data_count=0
let plotted=0
let uplot = undefined;

var data = [[],[],[],];

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

      if (data_count > 100)
      {
        data[0].shift();
        data[1].shift();
        data[2].shift();
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

startup_time="something"

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

      spanGaps: false,

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
