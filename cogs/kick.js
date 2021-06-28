const Discord = require('discord.js');
const config = require('../config.json');
var bot = {};

var kick = function (msg) {
    const args = msg.content.trim().split(' ');
    console.info(args)
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("kick", kick);
}

exports.requires = [];
exports.setup = setup;