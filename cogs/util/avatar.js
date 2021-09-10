const Discord = require('discord.js'); 
const config = require('../../config.json');
var bot = {}; 

var avatar = function (msg) {
    const args = msg.content.trim().split(' ');
    const member = msg.mentions.members.first() || msg.guild.members.cache.get(args[0]) || msg.guild.members.cache.find(x => x.user.username.toLowerCase() === args.slice(0).join(' ') || x.user.username === args[0]) || msg.member;

        if (!member.user.avatarURL) return msg.reply(`**Błąd**: Użytkownik nie posiada avatara.`);

        const avatar = new Discord.MessageEmbed()
			.setTitle(`Avatar - ${member.user.username}`)
            .setColor("RANDOM")
            .setImage(member.user.avatarURL())
            .setColor(member.displayHexColor)
            .setImage(member.user.displayAvatarURL({ dynamic: true, size: 2048 }))
            .setURL(member.user.avatarURL())
            .setFooter(config.footerCopyright, config.footerCopyright)
        msg.reply( {embeds: [avatar] })
            .catch(() => msg.reply('**Błąd**: Brak uprawnień - `Embed` '));
}

var setup = function (b) { 
    bot = b;
    bot.registerCommand("avatar", avatar); 
}

exports.requires = [];
exports.setup = setup;