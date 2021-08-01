const Discord = require('discord.js'); 
const config = require('../../config.json');
let moment = require('moment');
var bot = {}; 

var serverinfo = function (msg) {
    let servericon = msg.guild.iconURL;
    let createdDate = moment(msg.guild.createdTimestamp).format("DD.MM.YYYY h:mm:ss");
    let joinedDate = moment(msg.member.joinedTimestamp).format("DD.MM.YYYY h:mm:ss");
    let guildOwner = msg.guild.ownerId;
    let serverembed = new Discord.MessageEmbed()
        .setTitle(msg.guild.name)
        .setColor("RANDOM")
        .setThumbnail(servericon)
        .addField("Właściciel", `<@${guildOwner}>`, true)
        .addField("Założono", `${createdDate}`, true)
        .addField("Dołączono", `${joinedDate}`, true)
        .addField("Liczba osób", `${msg.guild.memberCount}`, true)
        .addField("Kanały", `${msg.guild.channels.cache.size}`, true)
        .addField("Role", `${msg.guild.roles.cache.size}`, true)
        .setThumbnail(msg.guild.iconURL())
        .setTimestamp()
        .setFooter(msg.author.username, msg.author.avatarURL);
    msg.reply( {embeds: [serverembed] })
}

var setup = function (b) { 
    bot = b;
    bot.registerCommand("serverinfo", serverinfo); 
}

exports.requires = [];
exports.setup = setup;