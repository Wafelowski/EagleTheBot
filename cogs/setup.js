const Discord = require('discord.js');
const config = require('../config.json');
const sqlite = require('sqlite3');

//---
//const { promisify } = require("util");
var bot = {};

var setupcmd = function (msg) {
    if (!msg.member.permissions.has("ADMINISTRATOR") || msg.member.id != config.ownerID) {
        msg.reply("Brak uprawnień!");
        return
    }
    const args = msg.content.trim().split(' ');
    try {
        var guildID = msg.guild.id
        var guildOwner = msg.guild.ownerID
        let serverDB = new sqlite.Database(`./db/servers/${guildID}.db`, sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
        serverDB.run(`CREATE TABLE IF NOT EXISTS server(serverid INTEGER NOT NULL, serverowner TEXT NOT NULL)`);
        serverDB.run(`CREATE TABLE IF NOT EXISTS roles(role TEXT NOT NULL, roleid TEXT NOT NULL)`);
        serverDB.all('SELECT * FROM server', function(err, rows) {
            if (err) {
                console.log(err);
                return;
            }
            if (rows === undefined) {
                let insertdata = serverDB.prepare(`INSERT INTO server VALUES(?,?)`);
                insertdata.run(guildID, guildOwner);
                insertdata.finalize();
                return;
            } 
            else {
                var serverowner = [];
                rows.forEach( row => serverowner.push(`${row.serverowner}`) );
                if (serverowner != guildOwner) {
                    let replacedata = serverDB.prepare(`REPLACE INTO server VALUES(?,?)`);
                    replacedata.run(guildID, guildOwner);
                    replacedata.finalize();
                }
            }
        });
        //let insertdata = serverDB.prepare(`INSERT INTO server VALUES(?,?)`);
        //insertdata.run(guildID, guildOwner);
        //insertdata.finalize();
        serverDB.close();
    }
    catch (error) {
        msg.reply(`Error \n\`${error}\``)
    }
    let serverDB = new sqlite.Database(`./db/servers/${guildID}.db`, sqlite.OPEN_READWRITE);
    if (args[0] == "info") {
        var modsID = [];
        var adminsID = [];
        const embed = new Discord.MessageEmbed()
            .setAuthor(`Setup - ${msg.guild.name}`)
            //.setDescription(`Administratorzy - ${adminsID.join(', ')}. \nModeratorzy - ${modsID.join(', ')}.`)
            .setColor("#ff0000")
            .setFooter(config.footerCopyright, config.footerCopyrightImage)
            .setTimestamp()
        serverDB.all('SELECT * FROM roles WHERE role = ?',"mod", function(err, rows) {
            if (err) {
                modsID = "Wystąpił błąd - Moderator"
                console.log(err);
                return modsID;
            }
            if (rows === undefined) {
                modsID = "Brak: Moderator"
                return modsID;
            } 
            else {
                rows.forEach( row => modsID.push(`<@&${row.roleid}>`) );
                console.log("line 49");
                embed.addFields(
                    { name: "Moderatorzy", value: `${modsID.join(', ')}`, inline: false },
                    { name: "Moderatorzy", value: `${modsID.join(', ')}`, inline: false },
                );
                //msg.reply(`modsID - ${modsID.join(', ')}`)
            }
            embed.addFields(
                { name: "Moderatorzy", value: `${modsID.join(', ')}`, inline: false },
                { name: "Moderatorzy", value: `${modsID.join(', ')}`, inline: false },
            );
        });
        serverDB.all('SELECT * FROM roles WHERE role = ?',"admin", function(err, rows) {
            if (err) {
                adminsID = "Wystąpił błąd - Administrator"
                console.log(err);
                return adminsID;
            }
            if (rows === undefined) {
                adminsID = "Brak"
                return adminsID;
            } 
            else {
                rows.forEach( row => adminsID.push(`<@&${row.roleid}>`) );
                console.log("line 67");
                embed.addFields(
                    { name: "Administratorzy", value: `${adminsID.join(', ')}`, inline: false },
                    { name: "Moderatorzy", value: `${modsID.join(', ')}`, inline: false },
                );
            }
            embed.addFields(
                { name: "Administratorzy", value: `${adminsID.join(', ')}`, inline: false },
                { name: "Moderatorzy", value: `${modsID.join(', ')}`, inline: false },
            );
        });
        serverDB.close()
        msg.reply( {embeds: [embed] })
    }
    if (args[0] == "add") {
        if ((args[1] == "admin")|| args[1] == "administrator") {
            let insertdata = serverDB.prepare(`INSERT INTO roles VALUES(?,?)`);
            insertdata.run("admin", args[2]);
            insertdata.finalize();
            serverDB.close();
            const embed = new Discord.MessageEmbed()
            .setAuthor(`Setup - ${msg.guild.name}`)
            .setDescription(`Dodano rolę <@&${args[2]}> jako Administrator.`)
            .setColor("#ff0000")
            .setFooter(config.footerCopyright, config.footerCopyrightImage)
            .setTimestamp()
            msg.reply( {embeds: [embed] })
        }
        if ((args[1] == "mod") || (args[1] == "moderator")) {
            let insertdata = serverDB.prepare(`INSERT INTO roles VALUES(?,?)`);
            insertdata.run("mod", args[2]);
            insertdata.finalize();
            serverDB.close();
            const embed = new Discord.MessageEmbed()
            .setAuthor(`Setup - ${msg.guild.name}`)
            .setDescription(`Dodano rolę <@&${args[2]}> jako Moderator.`)
            .setColor("#ff0000")
            .setFooter(config.footerCopyright, config.footerCopyrightImage)
            .setTimestamp()
            msg.reply( {embeds: [embed] })
        }
        if ((args[1] == "weryfikacja") || args[1] == "verification") {
            let insertdata = serverDB.prepare(`INSERT INTO roles VALUES(?,?)`);
            insertdata.run("verification", args[2]);
            insertdata.finalize();
            serverDB.close();
            const embed = new Discord.MessageEmbed()
            .setAuthor(`Setup - ${msg.guild.name}`)
            .setDescription(`Dodano rolę <@&${args[2]}> jako rolę weryfikacji w toku.`)
            .setColor("#ff0000")
            .setFooter(config.footerCopyright, config.footerCopyrightImage)
            .setTimestamp()
            msg.reply( {embeds: [embed] })
        }
    }
    if (args[0] == "remove") {
        let removedata = serverDB.prepare(`DELETE FROM roles WHERE roleid = ${args[1]}`);
        removedata.run();
        removedata.finalize();
        serverDB.close();
        const embed = new Discord.MessageEmbed()
        .setAuthor(`Setup - ${msg.guild.name}`)
        .setDescription(`Usunięto rolę <@&${args[1]}> z listy.`)
        .setColor("#ff0000")
        .setFooter(config.footerCopyright, config.footerCopyrightImage)
        .setTimestamp()
        msg.reply( {embeds: [embed] })
    }
    msg.react('✅')
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("setup", setupcmd);
}

exports.requires = [];
exports.setup = setup;