const Discord = require('discord.js'); 
const config = require('../../config.json');
var bot = {}; 

var userinfo = function (msg) {
    const user = msg.author;
    const DISCORD_EPOCH = 1420070400000;
    function convertSnowflakeToDate(snowflake) {
        // return new Date(snowflake / 4194304 + epoch)
        return Math.floor((snowflake / 4194304 + DISCORD_EPOCH) / 1000)
    }
    
    if (msg.member.flags == undefined) {
        msg.member.flags = "Brak"
    }
    
    let roles = msg.member.roles.cache.map(role => role.id);
    roles.pop();
    const roles2 = roles.join(">, <@&");
    let embed = new Discord.MessageEmbed()
        .setTitle(`${user.tag}`)
        .setColor(`${msg.member.displayHexColor}`)
        .addField("Użytkownik", `${user}`, true)
        .addField("Tag", user.tag, true)
        .addField("ID", user.id, true)
        .addField("Założono",  `<t:${convertSnowflakeToDate(user.id)}>`, true)
        .addField("Flagi", msg.member.flags, true)
        .addField("Dołączono", `<t:${Math.floor(msg.member.joinedAt.getTime() / 1000)}>`, true)
        .addField(`Role - ${roles.length}`, `<@&${roles2}>`, true)
        .setTimestamp()
        .setFooter(config.footerCopyright, config.footerCopyrightImage);
    msg.reply( {embeds: [embed] });    
}

var setup = function (b) { 
    bot = b;
    bot.registerCommand("userinfo", userinfo); 
}

exports.requires = [];
exports.setup = setup;