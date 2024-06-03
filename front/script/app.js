'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let  statusElement, waterChart, proteinChart, creatineChart;
const maxWater = 810;
const maxProtein = 100;
const maxCreatine = 100;
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
      backgroundColor: ['#36a2eb', '#d3d3d3'],
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
const showProteinweight = function (jsonObject) {
  console.log('get proteine weight');
  const remainingProtein = jsonObject['proteinweight'].Waarde;
  console.info(remainingProtein)
  // remainingWater = jsonObject
  const data = {
    labels: ['Remaining Protein'],
    datasets: [{
      // label: 'Proteine weight',
      data: [remainingProtein, maxProtein - remainingProtein],
      backgroundColor: ['#cddc39', '#d3d3d3'],
      hoverOffset: 4
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
  };

  const ctx = document.getElementById('proteinChart').getContext('2d');
  proteinChart = new Chart(ctx, config);
};

const showCreatineweight = function (jsonObject) {
  console.log('get creatine weight');
  const remainingCreatine = jsonObject['creatineweight'].Waarde;
  console.info(remainingCreatine)
  // remainingWater = jsonObject
  const data = {
    labels: ['Remaining Creatine'],
    datasets: [{
      // label: 'Proteine weight',
      data: [remainingCreatine, maxCreatine - remainingCreatine],
      backgroundColor: ['#ffa500', '#d3d3d3'],
      hoverOffset: 4
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
  };

  const ctx = document.getElementById('creatineChart').getContext('2d');
  creatineChart = new Chart(ctx, config);
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
const getProteinweight = function () {
  handleData("http://192.168.168.169:5000/api/v1/proteinweight/", showProteinweight);
};
const getCreatineweight = function () {
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
  socketio.on('B2F_proteinweight', function (object) {
    console.log('new proteinstatus');
    const proteinweight = object.weight;
    console.info(proteinweight);
    proteinChart.data.datasets[0].data[0] = proteinweight;
    proteinChart.data.datasets[0].data[1] = maxProtein - proteinweight;
    proteinChart.update();
  });
  socketio.on('B2F_creatineweight', function (object) {
    console.log('new creatinestatus');
    const creatineweight = object.weight;
    console.info(creatineweight);
    creatineChart.data.datasets[0].data[0] = creatineweight;
    creatineChart.data.datasets[0].data[1] = maxCreatine - creatineweight;
    creatineChart.update();
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
  getProteinweight();
  getCreatineweight();
};

document.addEventListener('DOMContentLoaded', init);

// #endregion