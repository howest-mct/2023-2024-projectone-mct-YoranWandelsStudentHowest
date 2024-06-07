'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let statusElement, waterChart, proteinChart, creatineChart, registerContainer, register, login;
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
  console.info(remainingProtein);
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
  console.info(remainingCreatine);
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
const callbackAddGebruiker = function () {
  console.log('nieuwe gebruiker toegevoegt');
};
const callbackLogin = function () {
  console.log('login');
};
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
  if (register) {
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
  }
};

const listenToClickRegister = function () {
  const button = document.querySelector('.js-register');
  button.addEventListener('click', function () {
    console.log('nieuwe gebruiker');
    const username = document.querySelector('#gebruikersnaam').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    const passwordConfirm = document.querySelector("#confirm-password").value;
    console.log(username, email, password, passwordConfirm);
    if (username && email && password && passwordConfirm) {
      console.log(username, email, password, passwordConfirm);
      if (password == passwordConfirm) {
        const jsonobject = {
          Gebruikersnaam: username,
          Wachtwoord: password,
          Email: email
        };
        handleData("http://192.168.168.169:5000/api/v1/gebruiker/", callbackAddGebruiker, null, 'POST', JSON.stringify(jsonobject));
      } else {
        console.log('Passwords not equal');
      }
    } else {
      console.log('All fields are required.');
    }
  });
};

const listenToClickLogin = function () {
  const button = document.querySelector('.js-login');
  button.addEventListener('click', function () {
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    console.log(email, password);
    const jsonobject = {
      Email: email,
      Wachtwoord: password
    };
    handleData("http://192.168.168.169:5000/api/v1/inloggen/", callbackLogin, null, 'POST', JSON.stringify(jsonobject));
  });
};
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const showWaterlevelTest = function () {
  const remainingWater = 400;
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

const showProteinweightTest = function () {
  console.log('get proteine weight');
  const remainingProtein = 500;
  console.info(remainingProtein);
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

const showCreatineweightTest = function () {
  console.log('get creatine weight');
  const remainingCreatine = 500;
  console.info(remainingCreatine);
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

const showShakeGraphTest = function () {
  // Data for the shake chart
  const shakeData = {
    labels: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    datasets: [{
      label: 'Shake Data',
      data: [65, 59, 80, 81, 56, 55, 40],
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderWidth: 1
    }]
  };

  // Configuration options for the shake chart
  const shakeConfig = {
    type: 'line',
    data: shakeData,
    options: {
      responsive: true,
      scales: {
        x: {
          beginAtZero: true
        },
        y: {
          beginAtZero: true
        }
      }
    }
  };

  // Create the shake chart
  const shakeChartCtx = document.getElementById('shakeChart').getContext('2d');
  new Chart(shakeChartCtx, shakeConfig);
};

const init = function () {
  console.info('DOM geladen');
  statusElement = document.querySelector('#status');
  registerContainer = document.querySelector('.register-container');
  register = document.querySelector('.js-register');
  login = document.querySelector('.js-login');
  listenToUI();
  listenToSocket();

  showWaterlevelTest();
  showProteinweightTest();
  showCreatineweightTest();
  showShakeGraphTest();

  getHistoriek();
  getWaterlevel();
  getProteinweight();
  getCreatineweight();
  if (register) {
  }
  if (registerContainer) {
    listenToClickRegister();
  }
  if (login) {
    listenToClickLogin();
  }
};

document.addEventListener('DOMContentLoaded', init);

// #endregion