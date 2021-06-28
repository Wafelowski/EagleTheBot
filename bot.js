const Discord = require('discord.js');
const {Intents} = require('discord.js');
const client = new Discord.Client({ intents: Intents.ALL, allowedMentions: { parse: ['users', 'roles'], repliedUser: false } });
const { exit } = require('process');

const config = require('./config.json');
var bot = {};

//-=-=-=-=-=-=-=-
//Load cogs
//-=-=-=-=-=-=-=-
const coreCogs = ["./cogs/test.js", "./cogs/kick.js"]
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