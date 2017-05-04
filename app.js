const path = require('path');
const express = require('express');
const app = express();
const port = 5000;

const bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const fileUpload = require('express-fileupload');
app.use(fileUpload());

const exec = require('child_process').exec;
var rootCommand = 'python dnd/estimate.py ';

app.set('view engine', 'ejs');

app.get('/', (request, response) => {
  response.render('index');
});

app.post('/estimate', (request, response) => {
  var pCount = parseInt(request.body.playercount);
  var pLevel = parseInt(request.body.playerlevel);
  var mCount = parseInt(request.body.monstercount);
  var mLevel = parseInt(request.body.monsterlevel);

  if (request.files.userfile) {
    var file = request.files.userfile;
    file.mv('dnd/user_file.csv');
  }

  var args = [pCount, pLevel, mCount, mLevel].map(v => v.toString()).join(' ');
  var command = rootCommand + args;

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

app.listen(port, (err) => {
  if (err) {
    return console.log('An error has occurred.');
  }
  console.log(`Now listening on port ${port}.`);
});