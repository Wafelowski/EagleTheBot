const Discord = require('discord.js');
const Intents = ['GUILDS', 'GUILD_MESSAGES','GUILD_MEMBERS', 'GUILD_INTEGRATIONS','GUILD_WEBHOOKS' , 'GUILD_INVITES', 'GUILD_VOICE_STATES', 'GUILD_PRESENCES', 'GUILD_MESSAGES', 'GUILD_MESSAGE_REACTIONS','GUILD_MESSAGE_TYPING', 'DIRECT_MESSAGES', 'DIRECT_MESSAGES','DIRECT_MESSAGE_TYPING'];
const client = new Discord.Client({ intents: Intents, allowedMentions: { parse: ['users', 'roles'], repliedUser: false } });

//-=-=-=-=-=-=-=-
//Requirements
//-=-=-=-=-=-=-=-
const config = require('./config.json');
const sqlite = require('sqlite3');
const fs = require('fs');
const { exit } = require('process');

//BotInfo
let os = require('os')
let cpuStat = require("cpu-stat")
//----


//-=-=-=-=-=-=-=-
//Load cogs
//-=-=-=-=-=-=-=-
var bot = {};
const coreCogs = ["./cogs/setup.js", "./cogs/useless/test.js", "./cogs/moderation/purge.js", 
"./cogs/moderation/bans.js", //"./cogs/moderation/watchlist.js", //"./cogs/moderation/kick.js", 
"./cogs/tickets/faq.js",
"./cogs/util/avatar.js", "./cogs/util/serverinfo.js", "./cogs/util/userinfo.js"]
var loadedCogs = {};
var listeners = {};

bot.listeners = listeners;
bot.config = config;
bot.client = client;
bot.loadedCogs = loadedCogs;
bot.ready = false;
var cog;

//-=-=-=-=-=-=-=-
//Load events
//-=-=-=-=-=-=-=-
const eventFiles = fs.readdirSync('./events').filter(file => file.endsWith('.js'));

for (const file of eventFiles) {
	const event = require(`./events/${file}`);
	if (event.once) {
		client.once(event.name, (...args) => event.execute(...args, client));
	} else {
		client.on(event.name, (...args) => event.execute(...args, client));
	}
}

//-=-=-=-=-=-=-=-
//Client events
//-=-=-=-=-=-=-=-

client.on('debug', console.log)
      .on('warn', console.log)
  

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
  var state = 0;
  const presences = [
      { type: 'WATCHING',  message: 'przejazdy alarmowe' },
      { type: 'COMPETING', message: 'Elektra vs FSV' },
      { type: 'PLAYING', message: 'PEUP 4.0 | Jutro o 18' },
      { type: 'LISTENING', message: 'Elektra GES 110' },
      { type: 'WATCHING',  message: 'kolumnę OPP' },
      { type: 'PLAYING',  message: 'pałowanie symulator' },
      { type: 'LISTENING', message: 'AS-420' },
      { type: 'COMPETING', message: 'prawa autorskie' },
      { type: 'PLAYING',  message: 'banowanie gier Roblox' },
      { type: 'WATCHING', message: 'przecieki'}
  ];

  setInterval(() => {
      state = (state + 1) % presences.length;
      const presence = presences[state];

      bot.client.user.setActivity(presence.message, { type: presence.type });
      client.user.setActivity(presence.message, { type: presence.type });
  }, 120000);

  let serversDB = new sqlite.Database('./db/servers.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
  serversDB.run(`CREATE TABLE IF NOT EXISTS servers(serverid INTEGER NOT NULL, serverowner TEXT NOT NULL)`);
  let blacklistDB = new sqlite.Database('./db/blacklist.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
  blacklistDB.run(`CREATE TABLE IF NOT EXISTS users(userid INTEGER NOT NULL, usertag TEXT NOT NULL, staff TEXT NOT NULL)`);
  let botStaffDB = new sqlite.Database('./db/botStaff.db', sqlite.OPEN_READWRITE | sqlite.OPEN_CREATE);
  botStaffDB.run(`CREATE TABLE IF NOT EXISTS staff(userid INTEGER NOT NULL, usertag TEXT NOT NULL, nickname TEXT NOT NULL)`);

  bot.ready = true;
});

client.on('messageCreate', msg => {
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

bot.registerCommand("botinfo", async function (msg) {
  cpuStat.usagePercent(function(err, percent) {
      if (err) {
          return console.log(err);
      }
      function msToTime(ms) {
        let seconds = (ms / 1000).toFixed(1);
        let minutes = (ms / (1000 * 60)).toFixed(1);
        let hours = (ms / (1000 * 60 * 60)).toFixed(1);
        let days = (ms / (1000 * 60 * 60 * 24)).toFixed(1);
        if (seconds < 60) return seconds + " Sek";
        else if (minutes < 60) return minutes + " Min(s)";
        else if (hours < 24) return hours + " Hour(s)";
        else return days + " Day(s)"
      }
      ///const duration = moment.duration(client.uptime).format(" D [days], H [hrs], m [mins], s [secs]");
      var apii = Math.round(client.ws.ping)
      var api = apii.toString().replace("-","")
      const botinfo = new Discord.MessageEmbed()
          .setTitle("**Bot Info:**")
          .setColor("RANDOM")
          .addField("⏳ RAM", `${(process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2)} / ${(os.totalmem() / 1024 / 1024).toFixed(2)} MB`, true)
          .addField("📡 API", `${api}ms`, true)
          .addField("⌚️ Uptime ", `${msToTime(client.uptime)}`, true)
          .addField("📁 Użytkownicy", `${client.users.cache.size}`, true)
          .addField("📁 Serwery", `${client.guilds.cache.size}`, true)
          .addField("📁 Kanały ", `${client.channels.cache.size}`, true)
          .addField("👾 Discord.js", `v${Discord.version}`, true)
          .addField("🔰 Node", `${process.version}`, true)
          .addField("🤖 CPU", `\`\`\`md\n${os.cpus().map(i => `${i.model}`)[0]}\`\`\``)
          .addField("🤖 Zużycie CPU", `\`${percent.toFixed(2)}%\``, true)
          .addField("🤖 Architektura", `\`${os.arch()}\``, true)
          .addField("💻 Platforma", `\`\`${os.platform()}\`\``, true)
          .setFooter(config.footerCopyright, config.footerCopyrightImage)
          .setTimestamp()  
      msg.channel.send({embeds: [botinfo] })
  });
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