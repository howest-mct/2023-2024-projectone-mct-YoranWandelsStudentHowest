'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);
let waterChart;
const maxWater = 810;

const listenToUI = function () { };


const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
  socketio.on('B2F_waterlevel', function (data) {
    console.log('new waterlevel');
    const remainingWater = data.waterlevel; // dynamically fetched

    waterChart.data.datasets[0].data[0] = remainingWater;
    waterChart.data.datasets[0].data[1] = maxWater - remainingWater;
    waterChart.update();
  });
};
// #region ***  DOM references                           ***********
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showHistoriek = function (jsonObject) {
  console.info(jsonObject);
};
const showWaterlevel = function (jsonObject) {
  water
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
}
const showGraphWater = function (jsonObject) {

};
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getHistoriek = function () {
  handleData("http://192.168.168.169:5000/api/v1/historiek/", showHistoriek);
};
const getWaterlevel = function () {
  handleData("http://192.168.168.169:5000/api/v1/waterlevel/", showWaterlevel);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
  getHistoriek();
  getWaterlevel();
  showGraphWater();
};

document.addEventListener('DOMContentLoaded', init);

// #endregion