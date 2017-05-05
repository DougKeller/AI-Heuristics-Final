var app = angular.module('dnd', []);
app.controller('MainController', ['$scope', '$http', '$timeout', ($scope, $http, $timeout) => {
  $scope.params = {
    players: [],
    monsters: []
  };

  $scope.addPlayer = () => {
    $scope.params.players.push({});
    var index = $scope.params.players.length - 1;
    $timeout(() => document.getElementById("player-" + index).focus());
  };

  $scope.addMonster = () => {
    $scope.params.monsters.push({});
    var index = $scope.params.monsters.length - 1;
    $timeout(() => document.getElementById("monster-" + index).focus());
  };

  $scope.removePlayer = (index) => { $scope.params.players.splice(index, 1) };
  $scope.removeMonster = (index) => { $scope.params.monsters.splice(index, 1) };

  var error = () => $scope.response = 'error';

  $scope.getAccuracy = () => {
    $http.get('/accuracy').then(
      (response) => {
        $scope.accuracy = response.data.accuracy;
      }
    )
  };

  $scope.getEstimate = () => {
    var params = {
      players: $scope.params.players.map(v => v.level),
      monsters: $scope.params.monsters.map(v => v.level)
    }
    $http.post('/estimate', params).then(
      (response) => {
        $scope.response = response.data;
        $scope.getAccuracy();
      },
      error
    );
  };

  $scope.makeCorrection = (correctValue) => {
    var correctCodes = {
      easy: 0,
      medium: 1,
      hard: 2,
      deadly: 3
    };

    var params = {
      players: $scope.response.players,
      monsters: $scope.response.monsters,
      result: correctCodes[correctValue.toLowerCase()]
    };

    $http.post('/case', params).then(
      () => $scope.response.correctionMade = true,
      error
    );
  };
}]);