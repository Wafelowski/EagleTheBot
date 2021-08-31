const Discord = require('discord.js');
require('../throwError.js')();
const config = require('../../config.json');
var bot = {};

var purge = function (msg) {
    const args = msg.content.trim().split(' ');
    const amount = args[0];
    if (!amount) return msg.reply('Musisz podać ilość wiadomości!');

    if (isNaN(amount) || parseInt(amount <= 0)) return msg.reply('Podana wartość nie jest liczbą!');
    
    if (parseInt(amount) > 100) return msg.reply('Podana wartość jest większa od stu. Jestem zbyt leniwy by dodać większy limit.');
    //const amount = parseInt(msg.content.split(' ')[1]) ? parseInt(msg.content.split(' ')[1]) : parseInt(msg.content.split(' ')[2])
    msg.channel.messages.fetch({
    limit: parseInt(amount) + 1,
    }).then((messages) => {
        msg.channel.bulkDelete(messages).catch(error => throwError(msg, error, "20", "purge " + msg.content));  //console.log(error.stack));
    });
    let reason;
    if (args[1] != undefined) {
        args.shift();
        // reason = args.map(function (x) {
        //     return x.replace(',', ' ');
        // });
        reason = args.join(' ');
        console.log(reason);
    }
    else reason = "Brak";
    const embed = new Discord.MessageEmbed()
          .setAuthor(`Usunięto wiadomości`)
          .setDescription(`**Ilość**: \`${amount}\` \n**Powód**: \`${reason}\``)
          .setColor("#ff0000")
          .setFooter(config.footerCopyright, config.footerCopyrightImage)
          .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    embed.delete()
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("purge", purge);
}

exports.requires = [];
exports.setup = setup;