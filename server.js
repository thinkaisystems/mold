var express =   require("express");
var bodyParser =    require("body-parser");
var cookieParser = require('cookie-parser');
var multer  =   require('multer');
var app =   express();

//var modelMongoDbPath="E:\\Softwares\\Node\\node-parser\\models\\";
var modelMongoDbPath="/node-parser/models/";
var _g_parser_hostport=PARAMDOCKERHOSTPORT;
var mongoose = require('mongoose');
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://PARAMDOCKERHOSTIP:27017/nnmodel')
  .then(() =>  console.log('connection succesful'))
  .catch((err) => console.error(err));

  
  // view engine setup
app.set('views', __dirname+'/views');
app.set('view engine', 'ejs');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());



var http = require('http')  
  , server = http.createServer(app)
  , io = require('socket.io')(server);



app.use(express.static(__dirname + '/public'));
app.use(express.static(__dirname + '/pages'));
app.use('/vendor', express.static('vendor'));
app.use('/dist', express.static('dist'));
app.use('/data', express.static('data'));

var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, './uploads');
  },
  filename: function (req, file, callback) {
    callback(null, file.fieldname + '-' + Date.now());
  }
});
var upload = multer({ storage : storage }).array('userPhoto',2);



app.get('/',function(req,res){
	

	//res.sendFile(__dirname + "/index.html");
      res.sendFile(__dirname + "/index.html");
});


app.get('/next',function(req,res){
console.log(res.body);
      res.sendFile(__dirname + "/next.html");
});

app.post('/api/photo',function(req,res){
    upload(req,res,function(err) {
        //console.log(req.body);
        //console.log(req.files);
        if(err) {
            return res.end("Error uploading file.");
        }
        res.end("File is uploaded");
    });
});

//////////////////START OF PYTHON///////////////////////////
app.post("/python", function(req, res) {
    

	
//var count = 0
io.on('connection', function (socket) {
  //count++;
console.log("in socket");
  //io.emit('news', { msg: 'One more person is online', count: count });
  //socket.emit('private', { msg: 'Welcome you are the ' + count + ' person here' });

  socket.on('private', function (data) {
    console.log(data);
  });

  socket.on('disconnect', function() {
    //count--;
    //io.emit('news', { msg: 'Someone went home', count: count })
  });
});



	
	var filenameTemp = {
        "filename": "invoke-script",
        "password": "1234",
        "twitter": "@user1"
    }
	
	//req.query.filename
    //if(!req.body.filename) {
    //    return res.send({"status": "error", "message": "missing filename"});
    //} else if(req.body.filename != filenameTemp.filename) {
    //    return res.send({"status": "error", "message": "wrong username"});
    //} else 
	{
	
		
	var pythonResult = {
        "output": "555"
    }
	
			var PythonShell = require('python-shell');
			var pyshell = new PythonShell('/python/'+req.body.filename+'.py');

			io.emit('news', { msg: "----Processing Python----------", count: 5555 });
			//pyshell.send(JSON.stringify([1,'param2','hello',4,5]));
			pyshell.send(JSON.stringify({ command: "do_stuff", args: [1, 2, 3] ,configFieldNames:req.body.config_field_name,ConId:req.body.ConId,ModelId:req.body.ModelId}));
			

			pyshell.on('message', function (message) {
				
				pythonResult.output=message;			
				io.emit('news', { msg: message, count: 5555 });
				
			
				
			});

			// end the input stream and allow the process to exit
			pyshell.end(function (err) {
				
				if (err){
					console.log("-----ERROR------------------------");
					console.log(err);
					//throw err;
				};	

				io.emit('news', { msg: 'DONE', count: -1 });			
				res.send({redirectto: '/next'});
				
				//console.log('finished');
			});
			console.log("End");
			console.log(new Date());
			io.emit('news', { msg: "----Started Python----------", count: 5555 });
			//return res.send(pythonResult);		
    }
});

//////////////////END OF PYTHON///////////////////////////

////////////////////MODEL Operations/////////////////////////////////////
///////Model-Create
app.get('/models/create',function(req,res){
	res.render("create-model");
});

//////Model-Save
app.post('/models/save',function(req,res){
console.log(res.body);

var NNModel = require(modelMongoDbPath +"NNModel");
	  
	  console.log(req.body);
	  
	  var inputobject={				
				"ConId": req.body.ConId,
				"TrainConId": req.body.TrainConId,
				"ModelName": req.body.ModelName,
				"MainField":req.body.MainField,
				"MainFieldFilter":req.body.MainFieldFilter,
				"MainFieldFilterVal1":req.body.MainFieldFilterVal1,
				"MainFieldFilterVal2":req.body.MainFieldFilterVal2,
				"FieldsSelected": req.body.FieldsSelected,
				"ModelType": req.body.ModelType,
				"ModelMethod": req.body.ModelMethod,
				"InfluencingFields": req.body.InfluencingFields,
				"TimeSeriesField": req.body.TimeSeriesField,
				"TimeSeriesFieldFormat": req.body.TimeSeriesFieldFormat,
				"IntervalSpan": req.body.IntervalSpan,
				"TimeSpanFrom": req.body.TimeSpanFrom,
				"TimeSpanTo": new Date(),
				"NumOfRecords": req.body.NumOfRecords,
				"AggregationFun": req.body.AggregationFun,
				"NNLoss": req.body.NNLoss,
				"NNMetric": req.body.NNMetric,
				"NNOptimizer": req.body.NNOptimizer,
				"NN_NB_Epoch":req.body.NN_NB_Epoch,
				"NNBatchSize":req.body.NNBatchSize,
				"NNThreshold":req.body.NNThreshold,
				"SVMKernal": req.body.SVMKernal,
				"SVM_NU":req.body.SVM_NU,
				"SVMGamma":req.body.SVMGamma,
				"IsHistoryData": true,				
	         }
			 
			 //"HistoryData_ConID":req.body.HistoryData_ConID,
	  
	  var nnModelObj = new NNModel(inputobject);

	  nnModelObj.save(function(err) {
		if(err) {
		  console.log(err);
		  res.render("create-model");
		} else {
		  console.log("Successfully created an model entry.");
		  res.redirect("/models/show/"+nnModelObj._id);
		}
	  });
	  	    
	  
});

///////Model-List
app.get('/model-list',function(req,res){
	
	var NNModel = require(modelMongoDbPath +"NNModel");
		NNModel.find({}).exec(function (err, models) {
			if (err) {
				console.log("Error:", err);
			}
			else {
				//res.send({models: models});
				res.render("model-list", {models: models});
			}
		});

});


////////Model-Update
app.post('/models/update/:id',function(req,res){
	
	console.log(req.body);
	
	var updatedobject={				
				"ConId": req.body.ConId,
				"TrainConId": req.body.TrainConId,
				"ModelName": req.body.ModelName,
				"MainField":req.body.MainField,
				"MainFieldFilter":req.body.MainFieldFilter,
				"MainFieldFilterVal1":req.body.MainFieldFilterVal1,
				"MainFieldFilterVal2":req.body.MainFieldFilterVal2,
				"FieldsSelected": req.body.FieldsSelected,
				"ModelType": req.body.ModelType,
				"ModelMethod": req.body.ModelMethod,
				"InfluencingFields": req.body.InfluencingFields,
				"TimeSeriesField": req.body.TimeSeriesField,
				"TimeSeriesFieldFormat": req.body.TimeSeriesFieldFormat,
				"IntervalSpan": req.body.IntervalSpan,
				"TimeSpanFrom": req.body.TimeSpanFrom,
				"TimeSpanTo": new Date(),
				"NumOfRecords": req.body.NumOfRecords,
				"AggregationFun": req.body.AggregationFun,
				"NNLoss": req.body.NNLoss,
				"NNMetric": req.body.NNMetric,
				"NNOptimizer": req.body.NNOptimizer,
				"NN_NB_Epoch":req.body.NN_NB_Epoch,
				"NNBatchSize":req.body.NNBatchSize,
				"NNThreshold":req.body.NNThreshold,
				"SVMKernal": req.body.SVMKernal,
				"SVM_NU":req.body.SVM_NU,
				"SVMGamma":req.body.SVMGamma,
				"IsHistoryData": true,
				"updated_at":new Date(),
	         }
			 //"HistoryData_ConID": req.body.HistoryData_ConID,
	
	var NNModel = require(modelMongoDbPath +"NNModel");
	NNModel.findByIdAndUpdate(req.params.id, { $set: updatedobject}, { new: true }, function (err, model) {
		if (err) {
			console.log(err);
			res.render("edit-model", {model: req.body});
		}
		res.redirect("/models/show/"+model._id);
	});

});


////////Model-Show
app.get('/models/show/:id', function(req, res) {
  
  var NNModel = require(modelMongoDbPath +"NNModel");
  NNModel.findOne({_id: req.params.id}).exec(function (err, model) {
    if (err) {
      console.log("Error:", err);
    }
    else {
      res.render("show-model", {model: model});
    }
  });  
  
});


//////Model-Edit
app.get('/models/edit/:id', function(req, res) {
  
  var NNModel = require(modelMongoDbPath +"NNModel");
  NNModel.findOne({_id: req.params.id}).exec(function (err, model) {
    if (err) {
      console.log("Error:", err);
    }
    else {
      res.render("edit-model", {model: model});
    }
  });  
  
});

///////Model-Delete
app.post('/models/delete/:id', function(req, res) {
  
  var NNModel = require(modelMongoDbPath +"NNModel");
  NNModel.remove({_id: req.params.id}, function(err) {
    if(err) {
      console.log(err);
    }
    else {
      console.log("Model deleted!");
      res.redirect("/model-list");
    }
  }); 
  
});


////////Model-api
app.get('/model-api/:id', function(req, res) {
  
  var NNModel = require(modelMongoDbPath +"NNModel");
  NNModel.findOne({_id: req.params.id}).exec(function (err, model) {
    if (err) {
      console.log("Error:", err);
    }
    else {
      res.send({model: model});
    }
  });  
  
});


////////////////////MODEL Operations/////////////////////////////////////



////////////////////CONNECTION Operations/////////////////////////////////////
////////CONNECTION-Show
app.get('/connections/show/:id', function(req, res) {
  
  var NNConnection = require(modelMongoDbPath +"NNConnection");
  NNConnection.findOne({_id: req.params.id}).exec(function (err, connection) {
    if (err) {
      console.log("Error:", err);
    }
    else {
      res.render("show-connection", {connection: connection});
    }
  });  
  
});


///////Connection-API
app.get('/connection-api',function(req,res){
	
	var NNConnection = require(modelMongoDbPath +"NNConnection");
		NNConnection.find({}).exec(function (err, connections) {
			if (err) {
				console.log("Error:", err);
			}
			else {				
				res.send({connections: connections});
			}
		});

});

///////Connection-List
app.get('/connection-list',function(req,res){
	
	var NNConnection = require(modelMongoDbPath +"NNConnection");
		NNConnection.find({}).exec(function (err, connections) {
			if (err) {
				console.log("Error:", err);
			}
			else {				
				res.render("connection-list", {connections: connections});
			}
		});

});


///////Connection-Create
app.get('/connections/create',function(req,res){
	res.render("create-connection");
});


//////Connection-Save
app.post('/connections/save',function(req,res){
console.log(res.body);

var NNConnection = require(modelMongoDbPath +"NNConnection");
	  
	  console.log(req.body);
	  
	  if(req.body.ConType=="1")
	  {
		  req.body.BrokerEndPoint="";
		  req.body.TopicName="";
		  //req.body.NoOfRecords=0;
	  }
	  else if(req.body.ConType=="2")
	  {
		  req.body.FileLocation="";
	  }
	  
	  var inputobject={
				"ConName": req.body.ConName,
				"ConType":req.body.ConType,
				"Retention": req.body.Retention,
				"FileLocation": req.body.FileLocation,
				"BrokerEndPoint": req.body.BrokerEndPoint,
				"TopicName": req.body.TopicName,
				"NoOfRecords": req.body.NoOfRecords,
	         }
	  
	  var nnConnectionObj = new NNConnection(inputobject);

	  nnConnectionObj.save(function(err) {
		if(err) {
		  console.log(err);
		  res.render("create-connection");
		} else {
		  console.log("Successfully created an connection entry.");
		  //res.redirect("/connections/show/"+nnConnectionObj._id);
		  fnConnectionConnector(req, res,nnConnectionObj._id);
		}
	  });
	  	    
	  
});



//////Connection-Edit
app.get('/connections/edit/:id', function(req, res) {
  
  var NNConnection = require(modelMongoDbPath +"NNConnection");
  NNConnection.findOne({_id: req.params.id}).exec(function (err, connection) {
    if (err) {
      console.log("Error:", err);
    }
    else {		
      res.render("edit-connection", {connection: connection});
    }
  });  
  
});


////////Connection-Update
app.post('/connections/update/:id',function(req,res){
	
	console.log(req.body);
	
	  if(req.body.ConType=="1")
	  {
		  req.body.BrokerEndPoint="";
		  req.body.TopicName="";
		  //req.body.NoOfRecords=0;
	  }
	  else if(req.body.ConType=="2")
	  {
		  req.body.FileLocation="";
	  }
	  
	
	var updatedobject={				
						"ConName": req.body.ConName,
						"ConType":req.body.ConType,
						"Retention": req.body.Retention,
						"FileLocation": req.body.FileLocation,
						"BrokerEndPoint": req.body.BrokerEndPoint,
						"TopicName": req.body.TopicName,
						"NoOfRecords": req.body.NoOfRecords,
					}
	
	var NNConnection = require(modelMongoDbPath +"NNConnection");
	NNConnection.findByIdAndUpdate(req.params.id, { $set: updatedobject}, { new: true }, function (err, connection) {
		if (err) {
			console.log(err);
			res.render("edit-connection", {connection: req.body});
		}
		res.redirect("/connections/show/"+connection._id);
	});

});

///////Connection-Delete
app.post('/connections/delete/:id', function(req, res) {
  
  var NNConnection = require(modelMongoDbPath +"NNConnection");
  NNConnection.remove({_id: req.params.id}, function(err) {
    if(err) {
      console.log(err);
    }
    else {
      console.log("Connection deleted!");
      res.redirect("/connection-list");
    }
  }); 
  
});

////////////////////CONNECTION Operations/////////////////////////////////////

function fnConnectionConnector(req, res,objConnectionId)
{
			var PythonShell = require('python-shell');
			var pyshell = new PythonShell('/python/invoke-connector.py');
		
			console.log("Connector Driver Start" + objConnectionId);			
			pyshell.send(JSON.stringify({ command: "temp_cmd", args: [1, 2, 3] ,connectionId:objConnectionId}));
			

			pyshell.on('message', function (message) {
				
				
				//io.emit('news', { msg: message, count: 5555 });
				console.log(message);
			
				
			});

			// end the input stream and allow the process to exit
			pyshell.end(function (err) {
				
				if (err){
					console.log("-----ERROR------------------------");
					console.log(err);
					//throw err;
				};	

				
				var NNConnection = require(modelMongoDbPath +"NNConnection");
				NNConnection.findOne({_id: objConnectionId}).exec(function (err, connection) {
					if(err) {
						console.log(err);
						//res.render("create-connection");
					} else {
						console.log("Successfully from python");
						res.redirect("/connections/show/"+objConnectionId);
					}
				});  
				
				
				io.emit('news', { msg: 'DONE', count: 5555 });			
				//res.send({redirectto: '/next'});
				
				//console.log('finished');
			});
			console.log("Connector Driver End");
			console.log(new Date());
			

}


///////FieldsList-API
app.get('/fieldslist-api/:id',function(req,res){
	
	console.log(req.params.id);
		
	var objNNFieldsList = require(modelMongoDbPath +"nnfieldslist");
		objNNFieldsList.findOne({Con_id:req.params.id}).exec(function (err, fieldsList) {
			if (err) {
				console.log("Error:", err);
			}
			else {				
				res.send({fieldsList: fieldsList});
			}
		});

});



///////Results-API
app.get('/results-api/:id',function(req,res){
	
	console.log(req.params.id);
		
	var objNNResults = require(modelMongoDbPath +"nnresults");
		objNNResults.findOne({Model_id:req.params.id}).exec(function (err, resultsList) {
			if (err) {
				console.log("Error:", err);
			}
			else {				
				res.send({resultsList: resultsList});
			}
		});

});

///////Results-API
app.get('/results-stream-api/:id',function(req,res){
	
	console.log(req.params.id);
		
	var objNNResults = require(modelMongoDbPath +"nnresults");
		objNNResults.findOne({S_Model_id:req.params.id}).exec(function (err, resultsList) {
			if (err) {
				console.log("Error:", err);
			}
			else {				
				res.send({resultsList: resultsList});
			}
		});

});



///////WATCHER-API
app.post('/start-watch',function(req,res){
	
	
	//console.log("req.body.modelId"+req.body.modelId);
	
	
	var chokidar = require('chokidar');

	var watcher = chokidar.watch('./python/TB/'+req.body.modelId+'/', {persistent: true,
    followSymlinks: false,
    usePolling: true,
    depth: undefined,
    interval: 100,
    ignorePermissionErrors: false});
	
	//io.emit('news', { msg: 'File watcher starter', count: 101010 });		
	
	watcher.on('add', function(path) {
		
		//console.log('File', path, 'has been added');
		//io.emit('news', { msg: 'File'+path+ 'has been added', count: 111111 });		
		io.emit('news', { msg: 'FileWatchFoundFile', count: 1155 });		
		watcher.close();		
		
	}).on('error', function(error) {console.error('Error happened', error);})
	//.on('change', function(path) {console.log('File', path, 'has been changed');})
    //.on('unlink', function(path) {console.log('File', path, 'has been removed');})
	
		

});


//app.listen
server.listen(_g_parser_hostport,function(){
    console.log("Working on port 3000");
});