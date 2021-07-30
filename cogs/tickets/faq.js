const Discord = require('discord.js');
const config = require('../../config.json');
var bot = {};

var zamknij = function (msg) {
    //const args = msg.content.trim().split(' ');
    msg.channel.messages.fetch({ limit: 100 }).then(messages => {
        let lastMessage = messages.last();
        let urlText = `\nReakcję znajdziesz [tutaj](${lastMessage.url} 'Kliknij by skoczyć do wiadomości!').`;
        if (!lastMessage.content.includes("Twój ticket właśnie został utworzony")) {
            urlText = "";
        }
        const embed = new Discord.MessageEmbed()
        .setAuthor(`PolishEmergencyV`)
        .setDescription(`Jeśli to wszystko, zamknij proszę ticket klikając :lock: oraz potwierdzając :white_check_mark:. ${urlText}`)
        .setColor("#ff0000")
        .setFooter(config.footerCopyright, config.footerCopyrightImage)
        .setTimestamp()
        msg.channel.send( {embeds: [embed] })
    }).catch(console.error);
    msg.delete();
}


var setup = function (b) {
    bot = b;
    bot.registerCommand("zamknij", zamknij);
}

exports.requires = [];
exports.setup = setup;