module.exports = {
  USERNAME_MAXLENGTH: 50,
  PASSWORD_MAXLENGTH: 1000,
  EMAIL_MAXLENGTH: 254,
  PROJECT_NAME_MAXLENGTH: 100,
  PROJECT_DESCRIPTION_MAXLENGTH: 1000,

  // Returns true if a string is not blank (filled with whitespace).
  validateNotBlank: function(str) {
    return str == null || ('' != str.replace(/^\s+/, '').replace(/\s+$/, ''))

  },
  // Set the updated_at and created_at fields.
  setCurrentDate: function() {
    var currentDate = new Date();
    this.updated_at = currentDate;
    if (!this.created_at)
      this.created_at = currentDate;  
  },
  // Verify an associated record exists in the database.
  verifyAssociatedExists: function(model, asso_id, next) {  
    model.findOne({_id: asso_id}, function(err, obj) {
      if(err || obj == null) { next( { "association": new Error("Associated " + model.collection.collectionName + " record must exist in database.") } )  }
      else { next() }
    });
  },
  // Verify that all records in an associated array exist in the database.
  verifyAssociatedObjectsExist: function(model, asso_arr, next) { 
    var len = asso_arr.length;
    //console.log(asso_arr);
    //console.log(asso_arr[0])
    //model.findById(asso_arr[0], function(err, f) {
    //  console.log(err, f);
    //})

    model.count( { _id: { $in : asso_arr } } , function(err, count) {
      if(len != count) {
        next( { "association": new Error("All associated " + model.collection.collectionName + " records must exist in database.") });
      } else {
        next();
      }
    });
  },
}
