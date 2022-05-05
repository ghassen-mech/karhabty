var mqtt = require("mqtt");
var MongoClient = require("mongodb").MongoClient;
var url = "mongodb://localhost:27017/raw_data";
var client = mqtt.connect("mqtt://io.adafruit.com", {
  username: "riadh",
  password: "aio_vrVV66IjWXW3MvxKSEN1RHo9LlZ0",
});
var vib = `${client.options.username}/feeds/vibration`;
const Vonage = require("@vonage/server-sdk");

const vonage = new Vonage({
  apiKey: "1bf1439a",
  apiSecret: "1oMLOwp0SXLLuqJT",
});
const from = "KARHABTI";
const to = "21622986521";
const text = "Please check your véhicule";

// on mqtt conect subscribe on tobic test
client.on("connect", function () {
  client.subscribe([vib], function (err) {
    if (err) console.log(err);
  });
});

//when recive message
client.on("message", function (topic, message) {
  var obj = {
    matricule: "102 TU 2000",
    vibration: "",
    date: new Date(),
  };
  if (topic === "riadh/feeds/vibration") obj.vibration = JSON.parse(message);
  // alram write to mongo notification_collections
  if (obj.vibration > 40) {
    insert_collection(obj, "notification");
    vonage.message.sendSms(from, to, text, (err, responseData) => {
      if (err) {
        console.log(err);
      } else {
        if (responseData.messages[0]["status"] === "0") {
          console.log("Message sent successfully.");
        } else {
          console.log(
            `Message failed with error: ${responseData.messages[0]["error-text"]}`
          );
        }
      }
    });
  } else insert_collection(obj, "backup");
  console.log(obj);
});

function insert_collection(message, collection) {
  MongoClient.connect(url, function (err, db) {
    if (err) throw err;
    var dbo = db.db("raw_data");
    dbo.collection(collection).insertOne(message, function (err, res) {
      if (err) throw err;
      db.close();
    });
  });
}
