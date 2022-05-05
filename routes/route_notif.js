var express = require("express");
var router = express.Router();
/* GET users listing. */

// This will help us connect to the database
const dbo = require("../database/conn");

router.get("/", async function (req, res, next) {
  const dbConnect = dbo.getDb();

  dbConnect
    .collection("notification")
    .find({})
    .limit(50)
    .toArray(function (err, result) {
      if (err) {
        res.status(400).send("Error fetching notification!");
      } else {
        res.json(result);
      }
    });
});

module.exports = router;
