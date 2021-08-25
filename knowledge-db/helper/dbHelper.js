const fs = require("fs")

const getData = () => {
    let rawData = fs.readFileSync("db.json");
    return JSON.parse(rawData);
}

const setData = (data) => {
    let rawData = JSON.stringify(data)
    fs.writeFileSync("db.json", rawData);
}

module.exports = {
    getData,
    setData
}

