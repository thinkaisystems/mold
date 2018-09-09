var mongoose = require('mongoose');

var ConConfigSchema = new mongoose.Schema({
  "ConId": string,
  "FieldName": String,  
  "FieldValue": String,  
  "updated_at": { type: Date, default: Date.now },
});

module.exports = mongoose.model('NNConConfig', ConConfigSchema);
