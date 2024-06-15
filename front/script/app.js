'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let waterChart, proteinChart, creatineChart, shakeChart, waterShakeChart,
register, login, shake, overview, statusElement, bottleElement, error, userid, sign, shakestatus, shakelink, homelink;

const maxWater = 24;
const maxProtein = 30;
const maxCreatine = 30;
let proteinHistory = [];
let creatineHistory = [];
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showWaterlevel = function () {
  const remainingWater = 20;
  // remainingWater = jsonObject
  const data = {
    labels: ['Remaining Water'],
    datasets: [{
      // label: 'Water Level',
      data: [remainingWater, maxWater - remainingWater],
      backgroundColor: ['#b3d9ff', '#c0c0c0'],
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

const showProteinweight = function () {
  const remainingProtein = 500;
  // remainingWater = jsonObject
  const data = {
    labels: ['Remaining Protein'],
    datasets: [{
      // label: 'Proteine weight',
      data: [remainingProtein, maxProtein - remainingProtein],
      backgroundColor: ['#f5deb3', '#c0c0c0'],
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

const showCreatineweight = function () {
  const remainingCreatine = 500;
  // remainingWater = jsonObject
  const data = {
    labels: ['Remaining Creatine'],
    datasets: [{
      // label: 'Proteine weight',
      data: [remainingCreatine, maxCreatine - remainingCreatine],
      backgroundColor: ['#e6e6e6', '#c0c0c0'],
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

const showShakeChart = function (jsonObject) {
  console.log(jsonObject);
  const proteinHistory = [];
  const creatineHistory = [];
  const WaterHistory = [];

  for (const shakedata of jsonObject['shake_history']) {
    // console.log(shakedata);

    if (shakedata['DeviceID'] == 5) {
      proteinHistory.push(shakedata['Waarde']);
    }
    if (shakedata['DeviceID'] == 6) {
      creatineHistory.push(shakedata['Waarde']);
    }
    if (shakedata['DeviceID'] == 8) {
      WaterHistory.push(shakedata['Waarde']);
    }

    const actiedatum = shakedata.Actiedatum;
    const gebruikerID = shakedata.GebruikerID;
  }

  const proteinData = proteinHistory;
  const creatineData = creatineHistory;

  const maxLength = Math.max(proteinData.length, creatineData.length);
  const padArray = (arr, length) => [...arr, ...Array(length - arr.length).fill(0)];

  const proteinDataPadded = padArray(proteinData, maxLength);
  const creatineDataPadded = padArray(creatineData, maxLength);

  const cumulativeData = (data) => data.map((val, index) => data.slice(0, index + 1).reduce((a, b) => a + b, 0));
  const proteinCumulative = cumulativeData(proteinDataPadded);
  const creatineCumulative = cumulativeData(creatineDataPadded);

  const shakeChartData = {
    labels: Array.from({ length: maxLength }, (_, i) => (i + 1).toString()),
    datasets: [
      {
        label: 'Protein shakes',
        data: proteinCumulative,
        borderColor: '#f0ad4e',
        backgroundColor: '#f5deb3',
        borderWidth: 1
      },
      {
        label: 'Creatine shakes',
        data: creatineCumulative,
        borderColor: '#999999',
        backgroundColor: '#e6e6e6',
        borderWidth: 1
      }
    ]
  };

  const shakeChartConfig = {
    type: 'line',
    data: shakeChartData,
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Aantal shakes',
            color: '#333',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          beginAtZero: true
        },
        y: {
          title: {
            display: true,
            text: 'Gram',
            color: '#333',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          beginAtZero: true,
          max: 50
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Weekly intake',
          font: {
            size: 18,
            weight: 'bold'
          }
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              label += context.raw + ' g';
              return label;
            }
          }
        }
      }
    }
  };

  shakeChart = new Chart(document.getElementById('shakeChart'), shakeChartConfig);
};

const showWaterShakeChart = function (jsonObject) {
  console.log(jsonObject);

  const WaterHistory = [];

  for (const shakedata of jsonObject['shake_history']) {
    if (shakedata['DeviceID'] == 8) {
      WaterHistory.push(shakedata['Waarde']);
    }
  }

  const maxLength = WaterHistory.length;
  const padArray = (arr, length) => [...arr, ...Array(length - arr.length).fill(0)];
  const waterDataPadded = padArray(WaterHistory, maxLength);

  const cumulativeData = (data) => data.map((val, index) => data.slice(0, index + 1).reduce((a, b) => a + b, 0));
  const waterCumulative = cumulativeData(waterDataPadded);

  const waterShakeChartData = {
    labels: Array.from({ length: waterDataPadded.length }, (_, i) => (i + 1).toString()),
    datasets: [
      {
        label: 'Water intake',
        data: waterCumulative,
        borderColor: '#337ab7',
        backgroundColor: '#bce8f1',
        borderWidth: 1
      }
    ]
  };

  const waterShakeChartConfig = {
    type: 'line',
    data: waterShakeChartData,
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Aantal shakes',
            color: '#333',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          beginAtZero: true
        },
        y: {
          title: {
            display: true,
            text: 'milliliter',
            color: '#333',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          beginAtZero: true,
          max: 5000
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              label += context.raw + ' ml';
              return label;
            }
          }
        }
      }
    }
  };

  waterShakeChart = new Chart(document.getElementById('waterShakeChart'), waterShakeChartConfig);
};


// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
const callbackAddGebruiker = function () {
  console.log('nieuwe gebruiker toegevoegt');
};
const callbackLogin = function (data) {
  console.log('test');
  if (data && data.gebruikerid) {
    console.log('Inloggen succesvol');
    // Sla de gebruikers-ID op in localStorage
    localStorage.setItem('userid', data.gebruikerid);
    // Doorsturen naar de overview pagina
    window.location.href = 'overview.html';
  } else if (data && data.error) {
    error.innerHTML = data.error;
    // Toon een foutmelding aan de gebruiker
    // alert(data.error);
  }
};

const callbackLogout = function () {
  console.log('logging out');
  localStorage.removeItem('userid');
  userid = null;
  window.location.href = 'login.html';
};

const callbackCreateshake = function (data) {
  console.log(data);
  const status = data.status;
  if (status != 'succes') {
    error.innerHTML = status;
    shakestatus.innerHTML = '';
  } else {
    error.innerHTML = '';
    shakestatus.innerHTML = 'Shake created';
  }
};
const callbackShutdown = function (data) {
  console.log('shutting down..')
}
// #endregion

// #region ***  Data Access - get___                     ***********

// const getHistoriek = function () {
//   handleData("http://${lanIP}/api/v1/historiek/", showHistoriek);
// };

const getShakeShart = function () {
  console.log(userid);
  handleData(`http://${lanIP}/api/v1/shakehist/`, showShakeChart);
  handleData(`http://${lanIP}/api/v1/shakehist/`, showWaterShakeChart);
};
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
const listenToUI = function () { };

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
  if (overview) {
    socketio.on('B2F_waterlevel', function (object) {
      console.log('new waterlevel');
      const remainingWater = object.waterlevel; // dynamically fetched

      waterChart.data.datasets[0].data[0] = Math.abs(remainingWater - maxWater);
      waterChart.data.datasets[0].data[1] = remainingWater;
      waterChart.update();
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
    socketio.on('B2F_shake', function (shakeData) {
      if (shakeData.deviceid == 6) {
        shakeChart.data.datasets[0].data.push(shakeData.shakeamount);
      } else if (shakeData.deviceid == 5) {
        shakeChart.data.datasets[1].data.push(shakeData.shakeamount);
      } else {
        shakeChart.data.datasets[0].data.push(shakeData.shakeamount);
      }
      shakeChart.update();
      waterShakeChart.update();
    });
  }
  if (shakestatus) {
    socketio.on('B2F_bottlestatus', function (object) {
      console.log('new bottlestatus');
      const bottlestatus = object.status;
      if (bottlestatus) {
        statusElement.innerHTML = "Status: Bottle Present";
        bottleElement.forEach(element => {
          element.classList.add('c-svg__bottle--active');
        });
      } else {
        statusElement.innerHTML = "Status: No Bottle";
        bottleElement.forEach(element => {
          element.classList.remove('c-svg__bottle--active');
        });
      }
    });
    socketio.on('B2F_shake_status', function (status) {
      console.log(status);
      shakestatus.innerHTML = status.status;
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
    const errorElement = document.querySelector('.js-error');
    console.log(username, email, password, passwordConfirm);

    if (username && email && password && passwordConfirm) {
      if (password === passwordConfirm) {
        const jsonobject = {
          Gebruikersnaam: username,
          Wachtwoord: password,
          Email: email
        };
        handleData(`http://${lanIP}/api/v1/gebruiker/`, function () {
          console.log('nieuwe gebruiker toegevoegt');
          error.innerHTML = '';
          document.querySelector('#gebruikersnaam').value = '';
          document.querySelector('#email').value = '';
          document.querySelector('#password').value = '';
          document.querySelector("#confirm-password").value = '';
        }, null, 'POST', JSON.stringify(jsonobject));
        window.location.href = 'login.html';
      } else {
        error.innerHTML = 'Passwords not equal';
      }
    } else {
      error.innerHTML = 'All fields are required';
    }
  });
};


const listenToClickLogin = function () {
  const button = document.querySelector('.js-login');
  button.addEventListener('click', function () {
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    const jsonobject = {
      Email: email,
      Wachtwoord: password
    };
    handleData(`http://${lanIP}/api/v1/inloggen/`, callbackLogin, null, 'POST', JSON.stringify(jsonobject));
    // window.location.href = 'overview.html';
  });
};

const listenToClickLogout = function () {
  const button = document.querySelector('#sign');
  button.addEventListener('click', function () {
    if (userid) {
      // Als de gebruiker is ingelogd, uitloggen en naar de inlogpagina navigeren
      handleData(`http://${lanIP}/api/v1/uitloggen/`, callbackLogout, null, 'POST', null);
    } else {
      // Als de gebruiker niet is ingelogd, gewoon naar de inlogpagina navigeren
      window.location.href = 'login.html';
    }
  });
};

const listenToClickCreateShake = function () {
  const button = document.querySelector('.js-shake');
  button.addEventListener('click', function () {
    const radioButtons = document.getElementsByName('shake-type');
    const inputAmount = document.getElementById('amount');
    const inputWateramount = document.getElementById('water-amount');
    let powder;

    radioButtons.forEach(button => {
      if (button.checked) {
        powder = button.value;
      }
    });

    const powderAmount = inputAmount.value;
    const waterAmount = inputWateramount.value;

    if (powderAmount && waterAmount) {
      const jsonobject = {
        Powder: powder,
        PowderAmount: powderAmount,
        WaterAmount: waterAmount
      };
      console.log(jsonobject);
      handleData(`http://${lanIP}/api/v1/createshake/`, callbackCreateshake, null, 'POST', JSON.stringify(jsonobject));
      shakestatus.innerHTML = 'Creating shake..';
      error.innerHTML = '';
    } else {
      error.innerHTML = 'Please set both powder amount and water amount.';
    }
  });
};
const listenToClickShutdown = function () {
  const button = document.querySelector('.js-shutdown')
  button.addEventListener('click', function(){
    console.log('shutdown')
    handleData(`http://${lanIP}/api/v1/shutdown/`, callbackShutdown, null, 'POST', null);
  })
}

// #endregion

// #region ***  Init / DOMContentLoaded                  ***********



const init = function () {
  console.info('DOM geladen');
  register = document.querySelector('.js-register');
  login = document.querySelector('.js-login');
  shake = document.querySelector('.js-shake');
  overview = document.querySelector('.c-dashboard');
  statusElement = document.querySelector('#status');
  bottleElement = document.querySelectorAll('.c-svg__bottle');
  error = document.querySelector('.c-error');
  sign = document.querySelector('#sign');
  shakestatus = document.querySelector('.c-shake--status');
  shakelink = document.querySelector('.js-shake__link');
  homelink = document.querySelector('.js-overview__link')
  if(overview) {
    homelink.classList.add('c-nav__link--active');
    shakelink.classList.remove('c-nav__link--active');
  }
  if (shakestatus) {
    shakelink.classList.add('c-nav__link--active');
    console.log('status')
    homelink.classList.remove('c-nav__link--active');
  }
  userid = localStorage.getItem('userid');
  // Controleer of de gebruiker is ingelogd
  if (userid) {
    sign.innerHTML = 'Sign out';
  }
  listenToUI();
  listenToSocket();
  listenToClickLogout();
  listenToClickShutdown();
  if (overview) {
    showWaterlevel();
    showProteinweight();
    showCreatineweight();
    getShakeShart();

    // getHistoriek();
    // getWaterlevel();
    // getProteinweight();
    // getCreatineweight();
  }
  if (register) {
    listenToClickRegister();
  }
  if (login) {
    listenToClickLogin();
  }
  if (shake) {
    listenToClickCreateShake();
  }
};

document.addEventListener('DOMContentLoaded', init);

// #endregion