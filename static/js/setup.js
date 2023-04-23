const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
if (urlParams.get('error') == "voltage")
{
    alert("Please enter a valid voltage");
}
if (urlParams.get('error') == "resistor")
{
    alert("Please enter a valid resistance");
}
if (urlParams.get('error') == "imin")
{
    alert("Please enter a valid minimum current");
}
if (urlParams.get('error') == "imax")
{
    alert("Please enter a valid maximum current");
}
if (urlParams.get('error') == "log_name")
{
    alert("Please enter a valid log name");
}

function doDownload() {
    var file=document.getElementById("log-select");
    document.location="/logs_download?log_filename=" + file.value;
}


function doReplay() {
    var file=document.getElementById("log-select");
    var lines=document.getElementById("replay-speed").value;
    document.location="/view?log_filename=" + file.value+"&lines="+lines;
}



function logs_read(logs_json)
{
    //console.log(farts)
    if(logs_json.length ==0)
    {
      return
    }


    for(x in logs_json){
        var sel = document.createElement("option");
        sel.innerHTML = logs_json[x];
        sel.value  = logs_json[x];
        document.getElementById("log-select").appendChild(sel);
    }
}

function logs_fetch()
{
  fetch('/logs.json')
    .then((response) => response.json())
    .then((logs) => logs_read(logs));
}
logs_fetch()
