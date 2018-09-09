var mongoose = require('mongoose');

var NNFieldsListSchema = new mongoose.Schema({  
  "Con_id": String,
  "Field_list": String,
  "Field_Type_List": String,
  "Time_Series_Field_List": String,  
  "Time_Series": Boolean,    
});

module.exports = mongoose.model('nnfieldslist', NNFieldsListSchema,'nnfieldslist');







