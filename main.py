import discord
import keep_alive
from discord.ext import commands

keep_alive.keep_alive()

bot = commands.Bot(command_prefix = "//", description = "Bot de Kuzotin")

@bot.event
async def on_ready():
	print("Ready !")

@bot.command()
async def coucou(ctx):
	await ctx.send("Coucou !")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.playing, name="Minecraft | //help"
    ))

@bot.command()
async def serverinfo(ctx):
	server = ctx.guild
	numberOfTextChannels = len(server.text_channels)
	numberOfVoiceChannels = len(server.voice_channels)
	serverDescription = server.description
	numberOfPerson = server.member_count
	serverName = server.name
	message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nLa description du serveur est {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
	await ctx.send(message)

@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} a été ban pour la raison suivante : {reason}.")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(877937966184554516)
    await channel.send(f"Acceuillons a bras ouvert {member.mention} ! Bienvenue dans ce magnifique serveur :)")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(877954157762473994)
    await channel.send(f"En cette belle journée nous déplorons la perte d'un membre bien aimé, {member.mention}.")

@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} a été kick.")

@bot.command()
async def clear(ctx, nombre : int):
	messages = await ctx.channel.history(limit = nombre + 1).flatten()
	for message in messages:
		await message.delete()

async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

status = ["//help",
		"A votre service",
		"L'eau mouille", 
		"Le feu brule", 
		"Lorsque vous volez, vous ne touchez pas le sol", 
		"Winter is coming", 
		"Mon créateur est Kuzotin", 
		"Il n'est pas possible d'aller dans l'espace en restant sur terre", 
		"La terre est ronde",
		"La moitié de 2 est 1",
		"7 est un nombre heureux",
		"Les allemands viennent d'allemagne",
		"Le coronavirus est un virus se répandant en Europe, en avez vous entendu parler ?",
		"J'apparais 2 fois dans l'année, a la fin du matin et au début de la nuit, qui suis-je ?",
		"Le plus grand complot de l'humanité est",
		"Pourquoi lisez vous ca ?"]

bot.run("T'as cru que j'allais te donner le token")
