var mongoose = require('mongoose');

var nnresultsSchema = new mongoose.Schema({  
  "Model_id": String,
  "Timestamp": Date,
  "Result": String,
});

module.exports = mongoose.model('nnresults', nnresultsSchema,'nnresults');







