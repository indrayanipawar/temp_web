var SELF_IP="localhost"


var express = require('express')
var bodyParser = require('body-parser')
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var cors = require('cors');

const app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use(cors());

const PORT = 5050;


app.use(express.static('public'));
http.listen(PORT || 8000, function () {
    console.log('listening on', PORT);
});
