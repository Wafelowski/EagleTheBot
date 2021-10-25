// eslint-disable-next-line no-unused-vars
const Discord = require('discord.js');
require('../throwError.js')();
var bot = {};

var ban = function (msg) {
    let args = msg.content.trim().split(' ');
    if (args.length === 0) return msg.reply('Musisz podać użytkownika! \n> `!ban <id/@> (0-7 dni) (Powód)` \n> Dni określają czas usunięcia wiadomości użytkownika.');
    let member = msg.mentions.members.first();
    let userid;
    if (member) userid = member.id;
    if (!member) {
        if (args[0].startsWith('<@') && args[0].endsWith('>')) {
            const id = args[0].slice(2, -1);
            member = msg.guild.members.fetch(`${id}`)
            .then(userid = id)
            // eslint-disable-next-line no-undef
            .catch(error => throwError(msg, error, "18", "ban " + msg.content));
            //userid = `${id}`;
        }
        else {
            member = msg.guild.members.fetch(`${args[0]}`)
            .then(userid = args[0])
            // eslint-disable-next-line no-undef
            .catch(error => throwError(msg, error, "25", "ban " + msg.content));
            //userid = `${args[0]}`;
        }
    }
    args.shift();
    let days = args[0];
    let daysMsg = "";
    days === parseInt(args[0])
    if (days <= 7 && days >= 0) {
        daysMsg = `Dodatkowo usunięto wiadomości z ostatnich ${days} dni.`
        args.shift();
    }
    else days = 0;
    let reason = args.join(' ');
    let silentMsg = "";
    // if (!member.bannable) {
    //     msg.reply("Nie mogę zbanować tego użytkownika!")
    //     return
    // }
    if ((member == msg.author) || (msg.author.id == userid)) {
        msg.reply("Dlaczego chcesz zbanować samego siebie?")
        return
    }
    if (!reason) {
        reason = "Brak powodu"
    }
    if (reason.includes("-s")) {
        silentMsg = " [Flaga -s]"
    }
    msg.guild.bans.create(userid, {days: days, reason: reason})
        .then(msg.reply(`Zrozumiano, użytkownik <@${userid}> został zbanowany za ${reason}.${silentMsg} ${daysMsg}`))
        .catch(console.error);
    //msg.reply(`Zrozumiano, użytkownik <@${userid}> został zbanowany za ${reason}.${silentMsg} ${daysMsg}`);
}

var banold = function (msg) {
    if (!msg.member.permissions.has("BAN_MEMBERS")) {
        msg.reply("Brak uprawnień!");
        return
    }
    //const args = msg.content.trim().split(' ');
    const args = msg.content.trim().replace(/  +/g, ' ').replace(/<@.?[0-9]*?> /g, '');
    const user = msg.mentions.members.first() || msg.guild.members.cache.get(args[0]) || msg.guild.members.cache.find(x => x.user.username.toLowerCase() === args.slice(0).join(' ') || x.user.username === args[0]);
    //const user = msg.mentions.members.first();
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
    bot.registerCommand("oldban", banold);
}

exports.requires = [];
exports.setup = setup;

