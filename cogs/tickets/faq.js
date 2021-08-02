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

var fivem = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`Obecnie pracujemy nad paczką naszych modów zoptymalizowaną specjalnie pod FiveM. Prace jednak trwają, dlatego postanowiliśmy zawiesić wydawanie nowych zgód. 
    Radzimy jednak poczekać i obserwować kanał ogłoszeń. Postaramy się by w tym roku pojawiły się tam pierwsze informacje oraz zapowiedzi odnośnie wspomnianej paczki. 
    Warto poczekać, ponieważ nasze pojazdy będą się cechowały wybitną optymalizacją oraz jakością. Dla serwerów chcących skorzystać z wspomnianej paczki będziemy również oferować dodatkową pomoc oraz pewne bonusy, na razie, prosimy o uzbrojenie się w cierpliwość :wink:`)
    .setColor("#2a44ff")
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var log = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`Zostałeś poproszony o wysłanie zawartości pliku RagePluginHook.log. Plik znajdziesz w głównym folderze gry, i jest on oznaczony jako plik tekstowy.`)
    .setColor("#2a44ff")
    .setImage(`https://cdn.discordapp.com/attachments/741061366357557298/841052997982355456/unknown.png`)
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var stroje = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`**1. Mieszają mi się stroje z amerykańskimi**
    - w OpenIV usuń folder EUP z \`update -> x64 -> dlcpacks\`
    - Zainstaluj ponownie PEUP bez instalacji EUP L&O i S&R
    
    **2. Zainstalowałem automatycznym instalatorem i są dziwne stroje oraz stare jednostki w LSPDFR**
    Zainstaluj konfigi, które są w tym samym archiwum co instalator.
    
    **3. Mam polskie jednostki, ale dziwne stroje.**
    Zainstaluj od nowa stroje.
    
    **4. Konfig do UltimateBackup**
    [LSPDFR.com](https://www.lcpdfr.com/downloads/gta5mods/misc/29319-ultimate-backup-config-for-polish-eup-polskie-stroje-dla-ultimate-backup/ 'Kliknij by przejść do LSPDFR.com!')
    [Nasza strona](https://polishemergencyv.com/file/3-ultimate-backup-config-for-polish-eup/ 'Kliknij by przejść do PolishEmergencyV.com!')
    `)
    .setColor("#2a44ff")
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var dlclist = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`Wyślij screena lub zawartość pliku dlclist.xml znajdującego się w tej lokalizacji: \n\`mods -> update -> update.rpf -> common -> data\``)
    .setColor("#2a44ff")
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var els = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`**1. ELS nie działa!**
    Upewnij się że masz zainstalowany: - ScriptHookV (http://www.dev-c.com/gtav/scripthookv/)
    - AdvancedHook (ten przychodzi z ELSem)
    
    **2. ELS Key Lock Active**
    Wciśnij Scroll Lock.
    
    **3. Światła nie błyskają, działa tylko cruise mode.**
    
    - Włącz OpenIV
    - Tools -> ASI Manager
    - Odinstaluj wszytkie opcje
    - Odinstaluj OpenIV
    - Zrestartuj komputer
    - Zainstaluj OpenIV od nowa
    - Zainstaluj pierwsze dwie opcje w ASI Manager
    - Sprawdź w grze`)
    .setColor("#2a44ff")
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var gameconfig = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`**1. Jak zainstalować gameconfig?**
    Na kanale <#690184232097939591> są dwa filmy zrobione przez nas, część pierwsza pokazuje instalację gameconfigu.
    
    **2. Co to jest X traffic i ped?**
    #x to jest mnożnik danej wartości; 
    - Traffic odpowiada za wielkość ruchu samochodów, 
    - Ped odpowiada za ilość NPC na ulicy. 
    Stock to domyślne wartości GTA.
    
    **3. Gdzie jest gameconfig?**
    \`mods -> update -> update.rpf -> common -> data\`
    
    **Link**
    https://pl.gta5-mods.com/misc/gta-5-gameconfig-300-cars`)
    .setColor("#2a44ff")
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var kanalpomocy = function (msg) {
    const embed = new Discord.MessageEmbed()
    .setAuthor(`PolishEmergencyV`)
    .setDescription(`<#531964192207405096>`)
    .setColor("#2a44ff")
    .setImage(`https://media.giphy.com/media/n9CMNbvOSY4MQGWcon/giphy.gif`)
    .setFooter(config.footerCopyright, config.footerCopyrightImage)
    .setTimestamp()
    msg.channel.send( {embeds: [embed] })
    msg.delete();
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("zamknij", zamknij);
    bot.registerCommand("fivem", fivem);
    bot.registerCommand("log", log);
    bot.registerCommand("stroje", stroje);
    bot.registerCommand("dlclist", dlclist);
    bot.registerCommand("els", els);
    bot.registerCommand("gameconfig", gameconfig);
    bot.registerCommand("kanalpomocy", kanalpomocy);
}


exports.requires = [];
exports.setup = setup;