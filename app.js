const path = require('path');
const express = require('express');
const app = express();
const port = 5000;

const exec = require('child_process').exec;
var command = 'python foo.py';

app.set('view engine', 'ejs');

app.get('/', (request, response) => {
  response.render('index');
});

app.post('/', (request, response) => {
  exec(command, (error, stdout, stderr) => {
    response.render('result', { text: stdout });
  });
});

app.listen(port, (err) => {
  if (err) {
    return console.log('An error has occurred.');
  }
  console.log(`Now listening on port ${port}.`);
});