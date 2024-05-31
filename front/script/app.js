const lanIP = `${window.location.hostname}:5000`;
const socketio = io(lanIP);

const listenToUI = function () {};

const listenToSocket = function () {
  socketio.on('connect', function () {
    console.log('verbonden met socket webserver');
  });
};
// #region ***  DOM references                           ***********
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showHistoriek = function (jsonObject) {
 console.info(jsonObject)
}
// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getHistoriek = function () {
  handleData("http://127.0.0.1:5000/api/v1/historiek/", showHistoriek)
}
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

const init = function () {
  console.info('DOM geladen');
  listenToUI();
  listenToSocket();
};

document.addEventListener('DOMContentLoaded', init);

// #endregion