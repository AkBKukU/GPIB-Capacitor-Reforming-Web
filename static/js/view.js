function data_print(datad)
{
  //document.getElementById("volt").textContent = datad.fetch;
}

function json_read(data)
{
    console.log(data)
    document.getElementById("voltage").textContent = Math.round(data[data.length - 1]["Target Voltage"]*100)/100
    document.getElementById("cap-voltage").textContent = Math.round(data[data.length - 1]["Cap Voltage"]*100)/100
    document.getElementById("cap-current").textContent = Math.round(data[data.length - 1]["DMM Current"]*100)/100
}


function data_fetch()
{
  fetch('/data.json')
    .then((response) => response.json())
    .then((data) => json_read(data))
    .catch(document.getElementById("voltage").textContent = "");
}

setInterval(data_fetch,1000)

startup_time="something"
