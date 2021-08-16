const Discord = require('discord.js');
const config = require('../config.json');

module.exports = function() { 
    this.throwError = function(msgObj, err, line, cmd) {
      const embedError = new Discord.MessageEmbed()
          .setAuthor(`Błąd`)
          .setDescription(`Linia: \`${line}\` \nKomenda: \`${cmd}\` \nTreść: \n\`\`\`${err}\`\`\``)
          .setColor("#ff0000")
          .setFooter(config.footerCopyright, config.footerCopyrightImage)
          .setTimestamp()
      msgObj.reply( {embeds: [embedError] })
    }
  }