var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
const session = require('cookie-session');
var csrf = require('csurf')

//var socket_io    = require( "socket.io" );


var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;


//var users = require('./routes/users');

var sassMiddleware = require('node-sass-middleware');
var path = require('path');

var mongoose = require('mongoose')
mongoose.connect('mongodb://localhost/mudlark-db-dev', function(err) {
  if(err) { console.log("\x1b[31m" + err.message); }
});

var app = express();

// Socket.io
//var io           = socket_io();
//app.io           = io;


// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.locals.pretty = true;

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(
   sassMiddleware({
       src: __dirname + '/scss', 
       dest: __dirname + '/public/stylesheets',
       prefix:  '/stylesheets',
       outputStyle: 'compressed',
       debug: true,       
   })
); 
app.use(session({keys: ['kjhkjhkukg', 'kufk8fyukukfkuyf']}));
app.use(express.static(path.join(__dirname, 'public')));

app.use(passport.initialize());
app.use(passport.session());

// passport config
var User = require('./models/user');
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());


app.use(function(req, res, next) {
  //res.locals.base_url = "/aquila"
  res.locals.base_url = ""
  res.locals.user = req.user;
  res.locals.path = req.path;
  next(null, req, res);
})

app.use(csrf({ cookie: true }))

app.use(function(req, res, next) {
  res.locals.csrfToken = req.csrfToken();
  next(null, req, res);
})

var routes = require('./routes/index');//(io);
var routes_user = require('./routes/user');//(io);
var routes_project = require('./routes/project');//(io);

app.use('/', routes);
app.use('/', routes_user);
app.use('/projects', routes_project);
//app.use('/users', users);




// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

// socket.io events
//io.on( "connection", function( socket )
//{
//    console.log( "A user connected" );
//});



module.exports = app;
