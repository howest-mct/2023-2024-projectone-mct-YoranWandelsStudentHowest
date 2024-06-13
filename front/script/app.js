'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

// #region ***  DOM references                           ***********
let waterChart, proteinChart, creatineChart, shakeChart, register, login, shake, overview, statusElement, bottleElement, error, userid, sign, shakestatus;
const maxWater = 810;
const maxProtein = 164;
const maxCreatine = 161;
let proteinHistory = [];
let creatineHistory = [];
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showWaterlevel = function () {
  const remainingWater = 400;
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

  // Definieer de arrays om de gegevens op te slaan
  const proteinHistory = [];
  const creatineHistory = [];

  for (const shakedata of jsonObject['shake_history']) {
    // Log elk individueel item voor controle
    console.log(shakedata);

    // Voeg shakedata toe aan de juiste array op basis van DeviceID
    if (shakedata['DeviceID'] == 5) {
      proteinHistory.push(shakedata['Waarde']);
    }
    if (shakedata['DeviceID'] == 6) {
      creatineHistory.push(shakedata['Waarde']);
    }

    // Gebruik de gegevens van elk item, bijvoorbeeld:
    const actiedatum = shakedata.Actiedatum;
    const gebruikerID = shakedata.GebruikerID;
    // Voer hier verdere acties uit met de gegevens, zoals het toevoegen aan een grafiek, enz.
  }

  //  data voor de proteïne-, creatine- en watergrafieken
  const proteinData = proteinHistory;
  const creatineData = creatineHistory;

  // Zorg ervoor dat de gegevensarrays van dezelfde lengte zijn door ze indien nodig aan te vullen met nullen
  const maxLength = Math.max(proteinData.length, creatineData.length);
  const padArray = (arr, length) => [...arr, ...Array(length - arr.length).fill(0)];

  const proteinDataPadded = padArray(proteinData, maxLength);
  const creatineDataPadded = padArray(creatineData, maxLength);

  // Maak cumulatieve gegevens voor elke dataset
  const cumulativeData = (data) => data.map((val, index) => data.slice(0, index + 1).reduce((a, b) => a + b, 0));
  const proteinCumulative = cumulativeData(proteinDataPadded);
  const creatineCumulative = cumulativeData(creatineDataPadded);

  // Gegevens voor de shakegrafiek met gecombineerde tooltips
  const shakeChartData = {
    labels: Array.from({ length: maxLength }, (_, i) => (i + 1).toString()),
    datasets: [
      {
        label: 'Protein shakes',
        data: proteinCumulative,
        borderColor: '#f0ad4e', // Nieuwe randkleur
        backgroundColor: '#f5deb3', // Nieuwe achtergrondkleur
        borderWidth: 1
      },
      {
        label: 'Creatine shakes',
        data: creatineCumulative,
        borderColor: '#999999', // Nieuwe randkleur
        backgroundColor: '#e6e6e6', // Nieuwe achtergrondkleur
        borderWidth: 1
      }
    ]
  };

  // Configuratieopties voor de shakegrafiek
  const shakeChartConfig = {
    type: 'line',
    data: shakeChartData,
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Aantal shakes', // Tekst voor de x-as
            color: '#333', // Kleur van de tekst
            font: {
              size: 14, // Grootte van het lettertype
              weight: 'bold' // Vetgedrukt lettertype
            }
          },
          beginAtZero: true
        },
        y: {
          title: {
            display: true,
            text: 'Gram', // Tekst voor de y-as
            color: '#333', // Kleur van de tekst
            font: {
              size: 14, // Grootte van het lettertype
              weight: 'bold' // Vetgedrukt lettertype
            }
          },
          beginAtZero: true,
          max: 10 // Maximale waarde van de y-as
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Wekelijkse inname', // Voeg de titel hier toe
          font: {
            size: 18, // Grootte van het lettertype van de titel
            weight: 'bold' // Vetgedrukt lettertype van de titel
          }
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            font: {
              size: 14, // Grootte van het lettertype van de legende
              weight: 'bold' // Vetgedrukt lettertype van de legende
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
              label += context.raw + ' gram';
              return label;
            }
          }
        }
      }
    }
  };

  // Maak de shakegrafiek
  shakeChart = new Chart(document.getElementById('shakeChart'), shakeChartConfig);
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
  const status = data.status
  if (status != 'succes') {
    error.innerHTML = status
    shakestatus.innerHTML = ''
  } else {
    error.innerHTML = ''
    shakestatus.innerHTML = 'Shake created'
  }
};
// #endregion

// #region ***  Data Access - get___                     ***********

// const getHistoriek = function () {
//   handleData("http://${lanIP}/api/v1/historiek/", showHistoriek);
// };

const getShakeShart = function () {
  console.log(userid);
  handleData(`http://${lanIP}/api/v1/shakehist/`, showShakeChart);
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

      waterChart.data.datasets[0].data[0] = remainingWater;
      waterChart.data.datasets[0].data[1] = maxWater - remainingWater;
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
  }
  if (shake) {
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
    socketio.on('B2F_shake', function (shakeData) {
      if (shakeData.deviceid == 6) {
        shakeChart.data.datasets[0].data.push(shakeData.shakeamount);
      } else if (shakeData.deviceid == 5) {
        shakeChart.data.datasets[1].data.push(shakeData.shakeamount);
      }
      shakeChart.update();
    })
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
      shakestatus.innerHTML = 'Creating shake..'
    } else {
      error.innerHTML = 'Please set both powder amount and water amount.';
    }
  });
};

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
  shakestatus = document.querySelector('.c-shake--status')
  userid = localStorage.getItem('userid');
  // Controleer of de gebruiker is ingelogd
  if (userid) {
    sign.innerHTML = 'Sign out';
  }
  listenToUI();
  listenToSocket();
  listenToClickLogout();
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