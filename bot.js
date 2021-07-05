const Discord = require('discord.js');
const {Intents} = require('discord.js');
const sqlite = require('sqlite3');
const client = new Discord.Client({ intents: Intents.ALL, allowedMentions: { parse: ['users', 'roles'], repliedUser: false } });
const { exit } = require('process');

const config = require('./config.json');
var bot = {};

//-=-=-=-=-=-=-=-
//Load cogs
//-=-=-=-=-=-=-=-
const coreCogs = ["./cogs/setup.js", "./cogs/useless/test.js", "./cogs/moderation/purge.js", "./cogs/moderation/kick.js", "./cogs/moderation/bans.js"]
var loadedCogs = {};
var listeners = {};


bot.listeners = listeners;
bot.config = config;
bot.client = client;
bot.loadedCogs = loadedCogs;
bot.ready = false;
var cog;

//-=-=-=-=-=-=-=-
//Client events
//-=-=-=-=-=-=-=-

//client.on('debug', console.log)
//      .on('warn', console.log)
  

client.on('ready', () => {
  console.log(`Zalogowano jako ${client.user.tag}! \nBot by Wafelowski.dev`);
  for (var cogName in loadedCogs) {
    cog = loadedCogs[cogName];
    if (typeof cog.ready === 'function') {
      console.info("Przygotowywanie " + cogName);
      cog.ready();
    }
  }

  bot.client.user.setStatus('online');
  bot.client.user.setActivity('przejazdy alarmowe', { type: 'WATCHING' });

  let serversDB = new sqlite.Database('./db/servers.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
  serversDB.run(`CREATE TABLE IF NOT EXISTS servers(serverid INTEGER NOT NULL, serverowner TEXT NOT NULL)`);
  let blacklistDB = new sqlite.Database('./db/blacklist.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
  blacklistDB.run(`CREATE TABLE IF NOT EXISTS users(userid INTEGER NOT NULL, usertag TEXT NOT NULL, staff TEXT NOT NULL)`);
  let botStaffDB = new sqlite.Database('./db/botStaff.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
  botStaffDB.run(`CREATE TABLE IF NOT EXISTS staff(userid INTEGER NOT NULL, usertag TEXT NOT NULL, nickname TEXT NOT NULL)`);

  bot.ready = true;
});

client.on('message', msg => {
  if (!bot.ready) {
    console.warn("Command received, before bot became ready.");
    return;
  }
  if (!msg.content.startsWith(config.prefix) || msg.author.bot) {
    return;
  }
  if (msg.content.includes("@here") || msg.content.includes("@everyone")) return false;
    if (msg.mentions.has(client.user.id)) {
        msg.channel.send({ content: `Hej! Mój prefix to ${config.prefix}`});
    }
    msg.content = msg.content.substr(config.prefix.length, msg.content.length);
    var command = msg.content.split(" ")[0];
    msg.content = msg.content.substr(command.length + 1, msg.content.length);
    var fn = listeners[command];
    if (typeof fn === 'function') {
      try {
        let ret = fn(msg);
        if (ret) {
          //await ret;
        }
      } catch (error) {
        console.error("Błąd: " + msg.content, { error });
      }
    } else {
      msg.reply("Komenda nieznana.");
    }
});

client.on('guildMemberUpdate', (oldMember, newMember) => {
  if (!bot.ready) return;
  const addedRoles = newMember.roles.cache.filter(role => !oldMember.roles.cache.has(role.id));
	if (!addedRoles.size > 0) return;
  //const channel = bot.client.channels.cache.get('853208523605147659');
  var guildID = oldMember.guild.id;
  console.log("line 92")
  var serverDB = new sqlite.Database(`./db/servers/${guildID}.db`, sqlite.OPEN_READWRITE);
  serverDB.all('SELECT * FROM roles WHERE role = ?', "verification", function(err, rows) {
    console.log("line 95")
    if (err) {
      console.log(`guildMemberUpdate Error: ${err}`);
      return false;
    }
    if (rows === undefined) {
      return false;
    } 
    else {
      let VerificationRole = [];
      rows.forEach( row => VerificationRole.push(`${row.roleid}`) );
      console.log("line 105");
      console.log(VerificationRole);
      if (oldMember.roles.cache.some(role => role.id === VerificationRole)) {
        const addedRoles = newMember.roles.cache.filter(role => !oldMember.roles.cache.has(role.id));
        console.log("line 114")
        var addedRoleID = addedRoles.map(r => r.id)
        var addedRoleName = addedRoles.map(r => r.name)
        console.log(`${addedRoleID.values().next().value}`)
        if (addedRoles.size > 0) console.log(`Role "${addedRoles.map(r => r.name)}" zostały przyznane ${oldMember.displayName}.`);
        newMember.roles.remove(addedRoleID, "Anty-Alt")
        if (addedRoles.size > 0) console.log(`Rola "${addedRoleName}" zostały usunięte ${oldMember.displayName}.`);
      }
      serverDB.close();
      return VerificationRole;
    }
  });

  if (oldMember.roles.cache.some(role => role.id === VerificationRole)) {
    const addedRoles = newMember.roles.cache.filter(role => !oldMember.roles.cache.has(role.id));
    console.log("line 114")
    var addedRoleID = addedRoles.map(r => r.id)
    var addedRoleName = addedRoles.map(r => r.name)
    console.log(`${addedRoleID.values().next().value}`)
    if (addedRoles.size > 0) console.log(`Role "${addedRoles.map(r => r.name)}" zostały przyznane ${oldMember.displayName}.`);
    newMember.roles.remove(addedRoleID, "Anty-Alt")
    if (addedRoles.size > 0) console.log(`Rola "${addedRoleName}" zostały usunięte ${oldMember.displayName}.`);
  }
  
  // // If the role(s) are present on the old member object but no longer on the new one (i.e role(s) were removed)
	// const removedRoles = oldMember.roles.cache.filter(role => !newMember.roles.cache.has(role.id));
	// if (removedRoles.size > 0) console.log(`The roles ${removedRoles.map(r => r.name)} were removed from ${oldMember.displayName}.`);
	// // If the role(s) are present on the new member object but are not on the old one (i.e role(s) were added)
	// const addedRoles = newMember.roles.cache.filter(role => !oldMember.roles.cache.has(role.id));
	// if (addedRoles.size > 0) console.log(`The roles ${addedRoles.map(r => r.name)} were added to ${oldMember.displayName}.`);

});

bot.registerCommand = function (command, func) {
  bot.listeners[command] = func;
}

bot.loadCog = function (cogname) {
  if (cogname in loadedCogs) {
    return;
  }
  try {
    var e = require(cogname);
    if (Array.isArray(e.requires) && e.requires.length > 0) {
      console.info("Moduł " + cogname + " wymaga: " + e.requires);
      for (var i = 0; i < e.requires.length; i++) {
        bot.loadCog(e.requires[i]);
      }
    }
    console.info("Wczytywanie " + "["+cogname+"]" + "...");
    e.setup(bot);
    loadedCogs[cogname] = e;
  } catch (err) {
    console.error("Wczytywanie modułu nieudane -" + cogname, {err: err});
    process.exit();
  }
}

//-=-=-=-=-=-=-=-
//Register backup commands
//-=-=-=-=-=-=-=-

bot.registerCommand("ping", async function (msg) {
  var pingg = Date.now()-msg.createdTimestamp
  var ping = pingg.toString().replace("-","")
  var apii = Math.round(client.ws.ping)
  var api = apii.toString().replace("-","")
  //await msg.reply(`🏓 Pong! \`${ping}ms.\` API - \`${api}ms\``);
  const embed = new Discord.MessageEmbed()
  .setAuthor("🏓 Pong!")
  .setColor("#00ff00")
  .setDescription(`Ping - \`${ping}ms\` \nAPI - \`${api}ms\``)
  .setFooter(config.footerCopyright, config.footerCopyrightImage)
  .setTimestamp()
  await msg.channel.send( {embeds: [embed] })
});
bot.registerCommand("cogs", async function (msg) {
  msg.reply(`Cogs - ${loadedCogs}`)
});
bot.registerCommand("shutdown", async function (msg) {
  if (msg.author.id !== config.ownerID) return;
  await msg.reply('Zamykanie!');
  exit()
});

//-=-=-=-=-=-=-=-
//Load cogs
//-=-=-=-=-=-=-=-

coreCogs.forEach(function (element) {
  bot.loadCog(element);
}, this);

config.startupExtensions.forEach(function (element) {
  bot.loadCog(element);
}, this);


//-=-=-=-=-=-=-=-
//Wafelowski.dev
//-=-=-=-=-=-=-=-
client.login(config.token)