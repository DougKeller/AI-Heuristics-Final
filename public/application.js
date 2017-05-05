var app = angular.module('dnd', []);
app.controller('MainController', ['$scope', '$http', '$timeout', ($scope, $http, $timeout) => {
  $scope.players = [];
  $scope.monsters = [];

  $scope.params = {};

  $scope.updatePlayerValues = () => {
    $scope.params.playerCount = $scope.players.length;
    var sum = 0;
    $scope.players.forEach(player => sum += player.level);
    $scope.params.playerLevel = sum / $scope.params.playerCount;
  };

  $scope.updateMonsterValues = () => {
    $scope.params.monsterCount = $scope.monsters.length;
    var sum = 0;
    $scope.monsters.forEach(monster => sum += monster.level);
    $scope.params.monsterLevel = sum / $scope.params.monsterCount;
  };

  $scope.addPlayer = () => {
    $scope.players.push({});
    var index = $scope.players.length - 1;
    $timeout(() => document.getElementById("player-" + index).focus());
  };

  $scope.addMonster = () => {
    $scope.monsters.push({});
    var index = $scope.monsters.length - 1;
    $timeout(() => document.getElementById("monster-" + index).focus());
  };

  $scope.removePlayer = (index) => { $scope.players.splice(index, 1) };
  $scope.removeMonster = (index) => { $scope.monsters.splice(index, 1) };

  var error = () => $scope.response = 'error';

  $scope.getEstimate = () => {
    $http.post('/estimate', $scope.params).then(
      (response) => {
        $scope.response = response.data;
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
      playerCount: $scope.response.playerCount,
      playerLevel: $scope.response.playerLevel,
      monsterCount: $scope.response.monsterCount,
      monsterLevel: $scope.response.monsterLevel,
      result: correctCodes[correctValue.toLowerCase()]
    };

    $http.post('/case', params).then(
      () => $scope.response.correctionMade = true,
      error
    );
  };
}]);