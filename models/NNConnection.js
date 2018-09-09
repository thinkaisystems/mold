var mongoose = require('mongoose');

var ConnectionSchema = new mongoose.Schema({  
  "ConName": String,  
  "ConType": String,
  "Retention": String,
  "FileLocation": String,
  "BrokerEndPoint": String,
  "TopicName": String,
  "Status": String,
  "NoOfRecords": Number,
  "updated_at": { type: Date, default: Date.now },
});

module.exports = mongoose.model('NNConnection', ConnectionSchema);
