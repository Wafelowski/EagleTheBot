var bot = {};
//for later use
//var command_desc = "Komenda Testowa";
//var command_type = "Inne";

var test = function (msg) {
    msg.reply("Yikes");
}

var setup = function (b) {
    bot = b;
    bot.registerCommand("test", test);
}

exports.requires = [];
exports.setup = setup;