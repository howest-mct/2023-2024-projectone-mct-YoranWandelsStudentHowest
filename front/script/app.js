'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const listenToUI = function () { };

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
};
// #region ***  DOM references                           ***********
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showHistoriek = function (jsonObject) {
  console.info(jsonObject);
};

const showGraphWater = function (jsonObject) {
  const maxWater = 1000; // in ml
  const remainingWater = 400; // in ml

  const data = {
    labels: ['Remaining Water', 'Used Water'],
    datasets: [{
      label: 'Water Level',
      data: [remainingWater, maxWater - remainingWater],
      backgroundColor: ['#36a2eb', '#ff6384'],
      hoverOffset: 4
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
  };

  const waterChart = new Chart(
    document.getElementById('waterChart'),
    config
  );
}
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getHistoriek = function () {
  handleData("http://192.168.168.169:5000/api/v1/historiek/", showHistoriek);
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
};

document.addEventListener('DOMContentLoaded', init);

// #endregion