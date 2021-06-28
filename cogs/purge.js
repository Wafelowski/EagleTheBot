const Discord = require('discord.js');
const {Intents} = require('discord.js');
const client = new Discord.Client({ intents: Intents.ALL, allowedMentions: { parse: ['users', 'roles'], repliedUser: false } });
const config = require('../config.json');
var bot = {};

var purge = function (msg) {
    const user = msg.mentions.users.first();
    const amount = parseInt(msg.content.split(' ')[1]) ? parseInt(msg.content.split(' ')[1]) : parseInt(msg.content.split(' ')[2])
    if (!amount) return msg.reply('Musisz podać ilość wiadomości!');
    if (!amount && !user) return msg.reply('Musisz podać użytkownika oraz ilość wiadomości lub samą ilość!');
    msg.channel.messages.fetch({
    limit: 100,
    }).then((messages) => {
        if (user) {
            const filterBy = user ? user.id : client.user.id;
            messages = messages.filter(m => m.author.id === filterBy).array().slice(0, amount);
        }
        msg.channel.bulkDelete(messages).catch(error => console.log(error.stack));
    });
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("purge", purge);
}

exports.requires = [];
exports.setup = setup;