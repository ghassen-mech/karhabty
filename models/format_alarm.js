const mongoose = require("mongoose");
const Schema = mongoose.Schema;
const alarmSchema = new Schema({
  matricule: String,
  vibration: String,
  //gps:float ,
  date: new Date(),
});
module.exports = mongoose.model("notification", alarmSchema);
