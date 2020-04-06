var mongoose = require('mongoose')
var Schema = mongoose.Schema;
var cf = require("./common/common_functions");
//var cf = require("./common/common_functions")
//var WipDocumentGroup = require('./wip_document_group')
//var Project = require("./project")
//var DocumentGroup = require("./document_group")
//var natural = require('natural');
//var tokenizer = new natural.TreebankWordTokenizer();
//var clone = require('clone');
ObjectId = require('mongodb').ObjectID;




// A model for storing projects.




var ProjectSchema = new Schema({
  // The user who created the project.
  user_id: {
       type: mongoose.Schema.Types.ObjectId,
       ref: 'User',
       required: true,
       unique: true,
       index: true,
  },    

  // The name of the project.
  project_name: {
      type: String,
      required: true,
      minlength: 1,
      maxlength: cf.PROJECT_NAME_MAXLENGTH,
      validate: cf.validateNotBlank
    },

  // A description of the project.
  project_description: {
      type: String,
      required: false,
      minlength: 1,
      maxlength: cf.PROJECT_DESCRIPTION_MAXLENGTH,
      validate: cf.validateNotBlank
  },

  // Some metadata about the WIP Project.
  file_metadata: {
      'Filename': {
        type: String,
        minlength: 0,
        maxlength: 255,
      },
    
      'Number of columns': Number,
      'Number of rows': Number//,
      //'Average tokens/document': Number
  },


  timeline_options: {
    y_axis_label: {
      type: String,
      minlength: 0,
      maxlength: 255
    },
    categorical_variable: {
      type: String,
      minlength: 0,
      maxlength: 255
    },
    tooltip_fields: {
      type: [String],
    }
  },

  entity_recognition_options: {
    entity_recognition_strategy: {
      type: String
    },
    structured_fields: {
      type: [String]
    }
  }
}, {
  timestamps: { 
    createdAt: "created_at",
    updatedAt: "updated_at"
  }
});
ProjectSchema.set('validateBeforeSave', false);

/* Model */

var Project = mongoose.model('Project', ProjectSchema);

module.exports = Project;
