
	var Project = require('../models/project');
	var User = require('../models/user');  
  var CsvReadableStream = require('csv-reader');

  var path = require('path')
	var MAX_FILESIZE_MB = 10;	

	var express = require('express');
	var router = express.Router();
	var fs = require('fs');
	var formidable = require('formidable');
	var fs = require('fs');
	const fileType = require('file-type');
	var PythonShell = require('python-shell');

	var extend = require('util')._extend

	// route middleware to make sure a user is logged in
	function isLoggedIn(req, res, next) {

	    // if user is authenticated in the session, carry on 
	    if (req.isAuthenticated())
	    //res.locals.user = testuser;
	        return next();

	    req.session.returnTo = "/new-project" + req.path;
	    
	    // if they aren't redirect them to the home page
	    res.redirect('/login');
	}

	function verifyWippid(req, res, next) {

		next();

	}

  // Todo: update so it's projects/301 instead
  router.get("/dashboard", isLoggedIn, function(req, res, next) {
    res.render("projects/dashboard", { title: "Dashboard" })
  })

	router.get("/new", isLoggedIn, function(req, res, next) {
		res.render("projects/new", extend({},  {title: "New Project", wip_project_id: 0}));	// Add the path to the response so it's easy to program the sidenav
	});

	router.post("/project-details", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("submitted project details");
		res.send("done")
		


	});


	router.post("/upload-data", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("uploaded data");
		res.send("done");
	})

	router.post("/upload-evaluation-data", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("submitted data");
		//res.send({"success": true, "details": [{ "Columns": 31 }, {"Rows": 734 }] });


	  //  wip_project = res.locals.wip_project;
	    wip_project_id = Math.floor(Math.random(1) * 1000);
	  // Ensure user does not already have a WipProject.

	  // if (user has documents saved in wip project already)
	  //res.send({"success": false, "error": "You cannot upload a new dataset as you have already uploaded one."})
	  //return;

	  //wip_project.deleteDocumentsAndMetadataAndSave(function(err, wip_project) {
	  //  if (err) throw err;

    var responded = false;
    var numberOfLines = 0;
    var numberOfTokens = 0;
    var columnHeadings = [];
    var filename = null;

    var rowCount = 0;
    var columnCount = 0;

    var form = new formidable.IncomingForm({"maxFileSize": MAX_FILESIZE_MB * 1024 * 1024}); // 25mb

    // parse the incoming request containing the form data
    form.parse(req);

    form.on('fileBegin', function(name, file) {

    	var dir = path.join(__dirname, '../data/' + req.user._id);
    	if(!fs.existsSync(dir)) {
    		fs.mkdirSync(dir);
    	}
      var projdir = path.join(__dirname, "../data/" + req.user._id + "/" + wip_project_id);
      if(!fs.existsSync(projdir)) {
        fs.mkdirSync(projdir);
      }

    	console.log('hi')
    	file.path = projdir + "/" + "dataset.csv";

    })
    

    // form.on('fileBegin', function(field, file) {
    //     responded = false;
    //     var fileType = file.type;
    //     console.log(fileType)
    //     if (fileType != 'text/plain') {
    //       this.emit('error', new Error("File must be a plain text file."));
    //     }
    // });

    // every time a file has been uploaded successfully,
    // read it and tokenize it
    form.on('file', function(name, file) {
      filename = file.name;
      var f = this;  

      // Ensure filetype is correct
      var fileType = file.type;        
      if (fileType != 'text/csv') {
        this.emit('error', new Error("File must be a csv file."));
        return;
      }
      

      // Tokenize the file with the WipProject.
      //var str = fs.readFileSync(file.path, 'utf-8');

      var inputStream = fs.createReadStream(file.path, 'utf8');
      var rows = [];

      inputStream
        .pipe(CsvReadableStream({ parseNumbers: true, parseBooleans: true, trim: true }))
        .on('data', function (row) {
            if(columnHeadings.length == 0)
              columnHeadings = row;
            else {
              rows.push(row);
            }
        })
        .on('end', function (data) {
            console.log("Headings: ", columnHeadings);
            console.log("Rows:     ", rows);
            rowCount = rows.length;
            columnCount = columnHeadings.length;
            f.emit('end_uploading');
        });

      



      // wip_project.createDocumentGroupsFromString(str, function(err, numberOfLines, numberOfTokens) {

      //   if(err) { 
      //     f.emit('error', new Error(err.errors.documents));
      //     fs.unlink(file.path, (err) => {
      //       if (err) throw err;
      //     });
      //   } else {


      //     // numberOfLines = wip_project.documents.length;
      //     // numberOfTokens = [].concat.apply([], wip_project.documents).length;

      //     wip_project.setFileMetadata({
      //       "Filename": filename ,
      //       "Number of documents": numberOfLines,
      //       "Number of tokens" : numberOfTokens,
      //       "Average tokens/document" : parseFloat((numberOfTokens / numberOfLines).toFixed(2))
      //     });


          

      //     wip_project.save(function(err, wip_project) {
      //       if(err) { 
      //         f.emit('error', err);
      //       } else {
      //         // Delete the file after reading is complete.
      //         fs.unlink(file.path, (err) => {
      //           if (err) throw err;
      //         });

      //         //console.log("New Documents (first 3):", wip_project.documents.slice(0, 3));              
      //         //numberOfLines = wip_project.documents.length;
      //         //numberOfTokens = [].concat.apply([], wip_project.documents).length;


      //         f.emit('end_uploading'); // Only send out signal once the WipProject has been updated.
      //       }
      //     });
      //   }
      // });



    });

    // log any errors that occur
    form.on('error', function(err) {

        if(!responded) {

          // If err.message is the one about filesize being too large, change it to a nicer message.
          if(err.message.substr(0, 20) == 'maxFileSize exceeded') {
            err.message = "The file was too large. Please ensure it is less than 1mb.";
          }


          res.send({ "success": false, "error": err.message });
          res.end();
          responded = true;
          
          
        }   
    });

    // once all the files have been uploaded, send a response to the client
    form.on('end_uploading', function() {
      if(!responded){
        //res.send({'success': true, details: wip_project.fileMetadataToArray() });
        res.send({'success': true, details: [
          {"Columns": columnCount},
          {"Rows": rowCount}
        ],
        columnHeadings: columnHeadings

        });
        //responded = true;
      }
    });


  















	});

	router.post("/upload-category-hierarchy", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("submitted data");
		res.send({"success": true});
	});
	router.post("/upload-category-training-data", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("submitted data");
		res.send({"success": true});
	});

	router.post("/upload-evaluation-data-reset", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("reset eval data");
		res.send({"success": true});
	});


	router.post("/timeline", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("timeline options");
		res.send("done")
	});

	router.post("/data-options", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("data options");
		res.send("done")
	});


	router.post("/entity-recognition", isLoggedIn, verifyWippid, function(req, res, next) {
		console.log("ER options");
		res.send("done")
	});




	router.post('/build-project', isLoggedIn, verifyWippid, function(req, res, next) {

		var redirected = false;

		console.log(req.body)

		console.log('----------------------------------')

		// Take args and run the python code, and redirect to the generator/running page



		pyshell = PythonShell.run('nlp/test.py', { args: ['-wm'] }, function (err, results) {
	  		if (err) throw err;
	  		//console.log('results: %j', results);
	  		console.log('finished running python code');  	
	  			
		});

		pyshell.on('message', function (message) {
		  // received a message sent from the Python script (a simple "print" statement)
		  console.log(message);
		 // process.stdout.write(message);
		  // Determine what type of message it is

		  if(!redirected) 
		  	//console.log("UIHODSHA")
		  	res.redirect('/new-project/building-project');	
		  	redirected = true

		  if(message.indexOf("|MP|:") > -1) {
		  	io.emit('module_progress',message);
		  } else {
		 	 io.emit('logentry',message);
		  }
		  //if (err) throw err;
		  // Redirect to the /running page once the pidfile has been generated
		  //if(message == "CREATED PIDFILE\r") {
		  
		  //}
		});	

	});

	// GET method for generator, which redirects if the generator is already running
	router.get('/build-project', function(req, res, next) {
		var variables = { title: "Evaluate Dataset" }
		fs.exists("/tmp/nlp_pid.pid", function(exists) {
			if(exists) {
				res.redirect('/new-project/building-project');
			} else {
				res.render('404', variables);				
			}
		});
	});

	// Special path for generator/running, as it needs to check if Python code is running
	router.get('/building-project', function(req, res, next) {
		var variables = { title: 'Generator' };
		fs.exists("/tmp/nlp_pid.pid", function(exists) {
			if(exists) {
				res.render('building_project', variables);
			} else {
				res.redirect('/new-project/build-project');
			}
		});		
	});





	module.exports = router;

