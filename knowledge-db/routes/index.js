var express = require('express');
var router = express.Router();
let { getData, setData } = require("../helper/dbHelper")


/* GET home page. */
router.get('/', function(req, res, next) {
    res.json(getData())
});

router.post('/', function(req, res, next){
  const newData = req.body;
  setData(newData);
  res.json(getData());
})

module.exports = router;
