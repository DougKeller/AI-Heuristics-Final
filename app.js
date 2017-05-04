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

app.post('/estimate', (request, response) => {
  var pCount = parseInt(request.body.playercount);
  var pLevel = parseFloat(request.body.playerlevel);
  var mCount = parseInt(request.body.monstercount);
  var mLevel = parseFloat(request.body.monsterlevel);

  if (request.files.userfile) {
    var file = request.files.userfile;
    file.mv('dnd/user_file.csv');
  }

  var args = [pCount, pLevel, mCount, mLevel].map(v => v.toString()).join(' ');
  var command = estimateCommand + args;

  console.log(`Executing command: ${command}`);
  exec(command, (error, stdout, stderr) => {
    if (error) {
      response.render('error');
    } else {
      response.render('result', {
        text: stdout,
        playercount: pCount,
        playerlevel: pLevel,
        monstercount: mCount,
        monsterlevel: mLevel
      });
    }
  });
});

app.post('/case', (request, response) => {
  var pCount = parseInt(request.body.playercount);
  var pLevel = parseInt(request.body.playerlevel);
  var mCount = parseInt(request.body.monstercount);
  var mLevel = parseInt(request.body.monsterlevel);
  var result = parseInt(request.body.result);

  var args = [pCount, pLevel, mCount, mLevel, result].map(v => v.toString()).join(' ');
  var command = addCastCommand + args;

  exec(command, () => {
    response.send();
  });
});

app.listen(port, (err) => {
  if (err) {
    return console.log('An error has occurred.');
  }
  console.log(`Now listening on port ${port}.`);
});