const Discord = require('discord.js');
const config = require('../../config.json');
const sqlite = require('sqlite3');
var bot = {};

var ban = function (msg) {
    const args = msg.content.trim().replace(/  +/g, ' ').replace(/<@.?[0-9]*?> /g, '');
    if (!msg.member.permissions.has("BAN_MEMBERS")) {
        msg.reply("Brak uprawnień!");
        return
    }
    const user = msg.mentions.members.first();
    //args.split(' ').splice(0, 1);
    //args.splice(0, 1);
    var reason = args;
    var silentMsg = "";
    if (!user) {
        msg.reply("Musisz podać użytkownika! `!ban <id>`");
        return
    }
    if (!user.kickable) {
        msg.reply("Nie mogę zbanować tego użytkownika!")
        return
    }
    if (user == msg.author) {
        msg.reply("Dlaczego chcesz zbanować samego siebie?")
        return
    }
    if (!reason) {
        // eslint-disable-next-line no-redeclare
        var reason = "Brak powodu"
    }
    if (msg.content.includes("-s")) {
        var silent = true;
        // eslint-disable-next-line no-redeclare
        var silentMsg = " [Flaga -s]"
    }
    msg.reply(`Zrozumiano, użytkownik został zbanowany.${silentMsg}`);
    if (!silent) user.send(`**${msg.guild.name}**: Zostałeś zbanowany za \`${reason}\``)
    msg.guild.members.ban(user, {
        reason: reason,
    });
}

var altban = function (msg) {
    
    if (msg.member.id == "337509297321803786" || msg.member.permissions.has("BAN_MEMBERS")) {
        var args = msg.content.trim().split(' ');
        var user = bot.client.users.cache.find(user => user.id === args[0])
        //bot.users.cache.find(user => user.id === 'USER-ID')
        //args.split(' ').splice(0, 1);
        //args.splice(0, 1);
        if (!user) {
            msg.reply("Musisz podać użytkownika! `!altban <id>`");
            return
        }
        if (!user.kickable) {
            msg.reply("Nie mogę zbanować tego użytkownika!")
            return
        }
        if (user == msg.author) {
            msg.reply("Dlaczego chcesz zbanować samego siebie?")
            return
        }
        msg.reply(`Zrozumiano, użytkownik został zbanowany.`);
        //if (!silent) user.send(`**${msg.guild.name}**: Zostałeś zbanowany za \`Alt konto\``)
        msg.guild.members.ban(user, {
            reason: "Alt konto",
        });
    }
    else {
        msg.reply("Brak uprawnień!");
        return
    }
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("ban", ban);
    bot.registerCommand("altban", altban);
}

exports.requires = [];
exports.setup = setup;

