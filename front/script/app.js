'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let waterChart, statusElement;
const maxWater = 810;
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showHistoriek = function (jsonObject) {
  console.info(jsonObject);
};
const showWaterlevel = function (jsonObject) {
  const remainingWater = jsonObject['waterlevel'].Waarde;
  // remainingWater = jsonObject
  const data = {
    labels: ['Remaining Water'],
    datasets: [{
      // label: 'Water Level',
      data: [remainingWater, maxWater - remainingWater],
      backgroundColor: ['#36a2eb', '#ff6384'],
      hoverOffset: 4
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
  };

  const ctx = document.getElementById('waterChart').getContext('2d');
  waterChart = new Chart(ctx, config);
};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getHistoriek = function () {
  handleData("http://192.168.168.169:5000/api/v1/historiek/", showHistoriek);
};
const getWaterlevel = function () {
  console.log('get water');
  handleData("http://192.168.168.169:5000/api/v1/waterlevel/", showWaterlevel);
};
const getProteinweight = function () {
  console.log('get water');
  handleData("http://192.168.168.169:5000/api/v1/proteinweight/", showProteinweight);
};
const getCreatineweight = function () {
  console.log('get water');
  handleData("http://192.168.168.169:5000/api/v1/creatineweight/", showCreatineweight);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
const listenToUI = function () { };


const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
  socketio.on('B2F_waterlevel', function (object) {
    console.log('new waterlevel');
    const remainingWater = object.waterlevel; // dynamically fetched

    waterChart.data.datasets[0].data[0] = remainingWater;
    waterChart.data.datasets[0].data[1] = maxWater - remainingWater;
    waterChart.update();
  });
  socketio.on('B2F_bottlestatus', function (object) {
    console.log('new bottlestatus');
    const bottlestatus = object.status;
    if (bottlestatus) {
      statusElement.innerHTML = "Status: Bottle Present";
      statusElement.style.color = "green";
    } else {
      statusElement.innerHTML = "Status: No Bottle";
      statusElement.style.color = "red";
    }
  });
};
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

const init = function () {
  console.info('DOM geladen');
  statusElement = document.getElementById('status');
  listenToUI();
  listenToSocket();
  getHistoriek();
  getWaterlevel();
};

document.addEventListener('DOMContentLoaded', init);

// #endregion