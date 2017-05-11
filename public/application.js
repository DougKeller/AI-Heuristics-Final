var app = angular.module('dnd', []);
app.controller('MainController', ['$scope', '$http', '$timeout', ($scope, $http, $timeout) => {
  $scope.params = {
    monsters: []
  };

  $scope.addMonster = () => {
    $scope.params.monsters.push({});
    var index = $scope.params.monsters.length - 1;
    $timeout(() => document.getElementById("monster-" + index).focus());
  };

  $scope.removeMonster = (index) => { $scope.params.monsters.splice(index, 1) };

  var error = () => $scope.response = 'error';

  $scope.getAccuracy = () => {
    $http.get('/accuracy').then(
      (response) => {
        $scope.accuracy = response.data.accuracy.toFixed(2);
      }
    )
  };

  $scope.getEstimate = () => {
    var params = {
      playerLevel: $scope.params.playerLevel,
      playerCount: $scope.params.playerCount,
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
      monsters: $scope.response.monsters,
      playerCount: $scope.response.playerCount,
      playerLevel: $scope.response.playerLevel,
      result: correctCodes[correctValue.toLowerCase()]
    };

    $http.post('/case', params).then(
      () => {
        $scope.response.correctionMade = true;
        $scope.response.result = correctValue;
      },
      error
    );
  };
}]);