//choose which web api to use to generate the chart
function optionChanged(dbSelected) {
  var webApiPath = "";
  var plotTitle = "";
  console.log(dbSelected);

  switch (dbSelected) {
    case "sqlite":
      plotTitle = "SQLite Chart";
      webApiPath = "/sqlite-web-api";
      break;
    case "postgresql":
      plotTitle = "PostgreSQL Chart";
      webApiPath = "/postgresql-web-api";
      break;
    case "mongodb":
      plotTitle = "MongoDB Chart";
      webApiPath = "/mongodb-web-api";
      break;
    default:
      console.log("An improper dropdown option has been selected.");
      return;
  }

  //delete chart div and add new div for chart
  d3.select("#my-chart").remove();
  d3.select("#chart-area")
    .append("div")
    .attr("id", "my-chart");

  d3.json(webApiPath, function (myData) {
    if (!myData) {
      d3.select("#my-chart")
        .append("h4")
        .text("I wasn't able to get data from the Web API you selected.");
      return;
    }

    console.log("I have retrieved data from the following path: " + webApiPath);
    console.log(myData);

    var myXData = [];
    var myYData = [];

    myData.forEach(votes_color => {
      myXData.push(votes_color.color);
      myYData.push(votes_color.votes);
    });

    var data = [
      {
        x: myXData,
        y: myYData,
        marker: {
          color: myXData,
        },
        type: 'bar'
      }
    ];

    var layout = {
      title: plotTitle
    };

    Plotly.newPlot('my-chart', data, layout);

  });

}

//call optionChanged to initilize the webpage with the SQLite chart, the first in the dropdown list
optionChanged("sqlite");