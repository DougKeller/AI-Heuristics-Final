const path = require('path');
const express = require('express');
const app = express();
const port = 5000;

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const fileUpload = require('express-fileupload');
app.use(fileUpload());
app.use('/public', express.static('public'));

const exec = require('child_process').exec;
var estimateCommand = 'python dnd/estimate.py ';
var addCastCommand = 'ruby dnd/add_case.rb ';

app.set('view engine', 'ejs');

app.get('/', (request, response) => {
  response.render('index');
});

var avg = (arr) => {
  var sum = 0;
  arr.forEach(v => sum += v);
  return sum / arr.length;
};

var std = (arr) => {
  var err = 0;
  var average = avg(arr);
  arr.forEach(v => err += Math.pow(v - average, 2));
  err = err / arr.length;
  return Math.sqrt(err);
};

app.post('/estimate', (request, response) => {
  var players = request.body.players;
  var monsters = request.body.monsters;

  var pCount = players.length;
  var pLevel = avg(players);
  var pStd = std(players);
  var mCount = monsters.length;
  var mLevel = avg(monsters);
  var mStd = std(monsters);

  var args = [pCount, pLevel, pStd, mCount, mLevel, mStd].map(v => v.toString()).join(' ');
  var command = estimateCommand + args;

  if (request.files && request.files.userfile) {
    var file = request.files.userfile;
    file.mv('dnd/user_file.csv');
  }

  console.log(`Executing command: ${command}`);
  exec(command, (error, stdout, stderr) => {
    if (error) {
      response.status(422).json(error);
    } else {
      response.status(200).json({
        result: stdout.replace(/\n/, ''),
        players: players,
        monsters: monsters,
        playerCount: pCount,
        playerLevel: pLevel,
        playerStd: pStd,
        monsterCount: mCount,
        monsterLevel: mLevel,
        monsterStd: mStd
      });
    }
  });
});

app.post('/case', (request, response) => {
  var players = request.body.players;
  var monsters = request.body.monsters;

  var pCount = players.length;
  var pLevel = avg(players);
  var pStd = std(players);
  var mCount = monsters.length;
  var mLevel = avg(monsters);
  var mStd = std(monsters);
  var result = request.body.result;

  var args = [pCount, pLevel, pStd, mCount, mLevel, mStd, result].map(v => v.toString()).join(' ');
  var command = addCastCommand + args;

  console.log(`Executing command: ${command}`);
  exec(command, () => {
    response.send();
  });
});

app.use('/accuracy', (request, response) => {
  var args = 'test';
  var command = estimateCommand + args;

  exec(command, (error, stdout, stderr) => {
    if (error) {
      response.status(422).json(error);
    } else {
      response.status(200).json({
        accuracy: parseFloat(stdout)
      });
    }
  });
});

app.listen(port, (err) => {
  if (err) {
    return console.log('An error has occurred.');
  }
  console.log(`Now listening on port ${port}.`);
});