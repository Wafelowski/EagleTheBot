const sqlite = require('sqlite3');

module.exports = {
	name: 'guildMemberUpdate',
	execute(oldMember, newMember, client) {
		const addedRoles = newMember.roles.cache.filter(role => !oldMember.roles.cache.has(role.id));
			if (!addedRoles.size > 0) return;
		let channel;
		var guildID = oldMember.guild.id;
		if (guildID == "531961175114645534") {
			// eslint-disable-next-line no-redeclare
			channel = client.channels.cache.get('842395141880152095');
		}
		else if (guildID == "847039824321183804") {
			// eslint-disable-next-line no-redeclare
			channel = client.channels.cache.get('853208523605147659');
		}
		let serverDB = new sqlite.Database(`./db/servers/${guildID}.db`, sqlite.OPEN_READWRITE);
		serverDB.all('SELECT * FROM roles WHERE role = ?', "verification", function(err, rows) {
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
			if (oldMember.roles.cache.some(role => role.id == VerificationRole) == false) return;
			if (oldMember.roles.cache.some(role => role.id == VerificationRole)) {
				const addedRoles = newMember.roles.cache.filter(role => !oldMember.roles.cache.has(role.id));
				var addedRoleID = addedRoles.map(r => r.id)
				var addedRoleName = addedRoles.map(r => r.name)
				if (addedRoleID == 732493824223477844) return;
				console.log(`${addedRoleID.values().next().value}`)
				if (addedRoles.size > 0) console.log(`Role "${addedRoles.map(r => r.name)}" zostały przyznane ${oldMember.displayName}.`);
				newMember.roles.remove(addedRoleID, "Anty-Alt")
				if (addedRoles.size > 0) console.log(`Rola "${addedRoleName}" zostały usunięte ${oldMember.displayName}.`);
				channel.send( { content: `Próbowano dodać rolę ${addedRoles.map(r => r.name)} do użytkownika <@${oldMember.id}> (${oldMember.user.tag}) w trakcie weryfikacji. Została usunięta. \n------ \n<@273904398261026817>` })
			}
			serverDB.close();
			return VerificationRole;
			}
		});
	},
};
