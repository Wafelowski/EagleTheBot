const Discord = require('discord.js'); //Zimportuj discord.js
const config = require('../config.json'); //Załaduj konfig
var bot = {}; //Zdefiniuj bota

var funkcja = function (msg) { //Funkcja zawierająca zawartość kodu komendy
    msg.reply("Yikes");
}

var setup = function (b) { //Funkcja ładująca komendę
    bot = b;
    bot.registerCommand("komenda", funkcja); //Zarejestrowanie komendy, "nazwa", funkcja
}

exports.requires = [];
exports.setup = setup;