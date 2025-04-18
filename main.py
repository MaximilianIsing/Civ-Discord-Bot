import discord
from discord import app_commands
from discord.ext import commands
import time
import asyncio
import random
from lists import *
from helpers import *

with open("TOKEN.txt", "r") as file:
    content = file.read()

Token = content

intents = discord.Intents.default()
intents.message_content = True
OwnerID = 424980696264867880

bot = commands.Bot(command_prefix="/", intents=intents)

guildID = 1351787046720503808
civGuildID = 1362491827478986752
wonderGuildID = 1362574955375493291

thisGuild = None
civGuild = None
wonderGuild = None


doneVotingCheck = 2 # Num of seconds between checks

lobbyHostingChannels = [1351993272096260127, 1362542399905202300]
voiceHostingChannels = {
    1351993272096260127: 1362542552376410252,
    1362542399905202300: 1351989426951295056
}


mostRecentCivOptions = {channel: [] for channel in lobbyHostingChannels}
mostRecentLeaderOptions = {channel: [] for channel in lobbyHostingChannels}
mostRecentPlayers = {channel: [] for channel in lobbyHostingChannels}
mustRecentNumLeaders = {channel: 0 for channel in lobbyHostingChannels}
mostRecentNumCivs = {channel: 0 for channel in lobbyHostingChannels}
gameHasOccured = {channel: False for channel in lobbyHostingChannels}

playerDraftMessagePointers = {channel: [] for channel in lobbyHostingChannels}





civEmojis = []
leaderEmojis = []
wonderEmojis = []
wonderEmojiIDs = [None] * len(allWonders)
civEmojiIDs = [None] * len(allCivs)
leaderEmojiIDs = [None] * len(allLeaders)








@bot.event
async def on_ready():
    global thisGuild
    global civGuild
    global wonderGuild
    thisGuild = await bot.fetch_guild(guildID)
    civGuild = await bot.fetch_guild(civGuildID)
    wonderGuild = await bot.fetch_guild(wonderGuildID)
    for civ in allCivs:
        civEmojis.append(discord.utils.get(civGuild.emojis, name=civ))

    for leader in allLeaders:
        leaderEmojis.append(discord.utils.get(thisGuild.emojis, name=leader))

    for wonder in allWonderIDs:
        wonderEmojis.append(discord.utils.get(wonderGuild.emojis, name=wonder))


    for i in range(len(civEmojiIDs)):
        civEmojiIDs[i] = f"<:{civEmojis[i].name}:{civEmojis[i].id}>"

    for i in range(len(leaderEmojiIDs)):
        leaderEmojiIDs[i] = f"<:{leaderEmojis[i].name}:{leaderEmojis[i].id}>"

    for i in range(len(allWonders)):
        wonderEmojiIDs[i] = f"<:{wonderEmojis[i].name}:{wonderEmojis[i].id}>"


    print("Bot Ready")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command(name="sync")
async def sync(ctx):
    if ctx.author.id == OwnerID:
        await bot.tree.sync()

        await ctx.send("Synced")
    else:
        await ctx.send("Insufficient permissions")


@bot.command(name="clear")
async def clear(ctx):
    if ctx.author.id == OwnerID:
        print("Clearing")
        await ctx.channel.purge(limit=500)
    else:
        await ctx.send("Insufficient permissions")


@bot.command(name="status", description="Say hello!")
async def status(ctx):
    await ctx.send("Status: Online")
 

@bot.command(name="wonderlist", description="Lists all wonders")
async def wonderlist(ctx):
    antiquity = "__Wonder Options Are:__\n"
    
    i = 0
    for wonder in antiquityWonders:
        antiquity += f"{wonder.name} - {wonderEmojiIDs[wonderDict[replaceSpaces(wonder.name)]]}"
        if i != len(antiquityWonders)-1:
            antiquity += " | "
            
        i += 1
    await ctx.send(antiquity)

    exploration = "** **\n"
    i = 0
    for wonder in explorationWonders:
        exploration += f"{wonder.name} - {wonderEmojiIDs[wonderDict[replaceSpaces(wonder.name)]]}"
        if i != len(explorationWonders)-1:
            exploration += " | "

        i += 1
    await ctx.send(exploration)

    modern = "** **\n"
    i = 0
    for wonder in modernWonders:
        modern += f"{wonder.name} - {wonderEmojiIDs[wonderDict[replaceSpaces(wonder.name)]]}"
        if i != len(modernWonders)-1:
            modern += " | "

        i += 1
    await ctx.send(modern)

@bot.command(name="wonderinfo", description="ives information about the wonder")
async def wonderinfo(ctx):
    messageContent = ctx.message.content
    wonder = replaceSpaces(extractWonder(messageContent))
    wonder = autoCapitalize(wonder)
    if  wonder in allWonderIDs:
        thisWonder = allWonders[wonderDict[wonder]]


        wonderEmbed = discord.Embed(
            title = replaceUnderscores(wonder),
            description = f"{thisWonder.age} age wonder",
            color = discord.Color.purple()
        )

        wonderEmbed.add_field(
            name='Effect:', value=f"{thisWonder.effect}\n", inline = False
        )

        wonderEmbed.add_field(
            name='Placement:', value=f"{thisWonder.condition}\n", inline = False
        )

        wonderEmbed.add_field(
            name='Cost (Online):', value=f'{int(thisWonder.cost/2)} production', inline = True
        )
        if thisWonder.civ != "None":
            wonderEmbed.add_field(
                name='Civilization:', value=f'{thisWonder.civ} - {civEmojiIDs[civDict[thisWonder.civ]]}', inline=True
            )
        wonderEmbed.add_field(
            name='Unlocked By:', value=f'{thisWonder.unlock}', inline=True
        )


        extractedID = extractEmojiID(wonderEmojiIDs[wonderDict[wonder]])
        emojiUrl = f"https://cdn.discordapp.com/emojis/{extractedID}.png"
        wonderEmbed.set_thumbnail(url=emojiUrl)
        await ctx.send(embed = wonderEmbed)
    else: 
        await ctx.send(f"\"{wonder}\" isn't an option, use /wonderlist for a list of options (use exact formatting)")

@bot.command(name="civlist", description="Lists all civs")
async def civlist(ctx):
    output = "__Civ Options Are:__\n"
    for civ in antiquityCivs:
        output += f"{replaceUnderscores(civ)} - {civEmojiIDs[civDict[civ]]}\n"
    output+="\n"
    for civ in explorationCivs:
        output += f"{replaceUnderscores(civ)} - {civEmojiIDs[civDict[civ]]}\n"
    output+="\n"
    for civ in modernCivs:
        output += f"{replaceUnderscores(civ)} - {civEmojiIDs[civDict[civ]]}\n"
    await ctx.send(output)


@bot.command(name="leaderlist", description="Lists all leaders")
async def leaderlist(ctx):
    output = "__Leader Options Are:__\n"
    for leader in allLeaders:
        output += f"{replaceUnderscores(leader)} - {leaderEmojiIDs[leaderDict[leader]]}\n"
    await ctx.send(output)



@bot.command(name="leaderinfo",description="Gives information about the leader")
async def leaderinfo(ctx, leader):
    messageContent = ctx.message.content
    leader = replaceSpaces(extractLeader(messageContent))
    leader = autoCapitalize(leader)
    if  replaceSpaces(leader) in allLeaders:
        leaderEmbed = discord.Embed(
            title = replaceUnderscores(leader),
            description = leaderInfoList[leader] + "\n\nUnlocks: " + leaderUnlocks[leader],
            color = discord.Color.orange()
        )
        extractedID = extractEmojiID(leaderEmojiIDs[leaderDict[leader]])
        emojiUrl = f"https://cdn.discordapp.com/emojis/{extractedID}.png"
        leaderEmbed.set_thumbnail(url=emojiUrl)
        await ctx.send(embed = leaderEmbed)
    else: 
        await ctx.send(f"\"{leader}\" isn't an option, use /leaderlist for a list of options (use exact formatting)")


@bot.command(name="maplist", description="Lists all maps")
async def maplist(ctx):
    output = "__Map Options Are:__\n"
    for map in allMaps:
        output += replaceUnderscores(map) + "\n"
    await ctx.send(output)



@bot.command(name="mapinfo",description="Gives information about the map type")
async def mapinfo(ctx):
    messageContent = ctx.message.content
    map = replaceSpaces(extractMap(messageContent))
    map = autoCapitalize(map)
    if map in allMaps:
        mapEmbed = discord.Embed(
            title = replaceUnderscores(map),
            description = mapInfoList[map] + "\n\n" + mapFavoring[map],
            color = discord.Color.blue()
        )
        mapEmbed.set_image(url=mapInfoLinks[map])

        await ctx.send(embed = mapEmbed)
    else: 
        await ctx.send(f"\"{map}\" isn't an option, use /maplist for a list of options (use exact formatting)")

@bot.command(name="reroll", description="Rerolls draft picks")
async def reroll(ctx):
    global gameHasOccured
    thisChannelID = ctx.channel.id
    if thisChannelID not in lobbyHostingChannels:
        await ctx.send(f"Please only use this command inside a lobby hosting channel")
        return
    
    if gameHasOccured[thisChannelID]:
        global mostRecentCivOptions
        global mostRecentLeaderOptions
        global mostRecentPlayers
        global mustRecentNumLeaders
        global mostRecentNumCivs
        global playerDraftMessagePointers

        await ctx.message.delete()
        for message in playerDraftMessagePointers[thisChannelID]:
            await message.delete()
        playerDraftMessagePointers[thisChannelID].clear()

        tempCivs = mostRecentCivOptions[thisChannelID].copy()
        tempLeaders = mostRecentLeaderOptions[thisChannelID].copy()

        random.shuffle(tempCivs)
        random.shuffle(tempLeaders)

        for player in mostRecentPlayers[thisChannelID]:
                output = f"<@{player}>\n"

                output += "__Civ Options:__\n"
                for c in range(mostRecentNumCivs[thisChannelID]):
                    thisCiv = tempCivs.pop()
                    output += f"{civEmojiIDs[thisCiv]} - {replaceUnderscores(antiquityCivs[thisCiv])}\n"

                output += "__Leader Options:__\n"
                for l in range(mustRecentNumLeaders[thisChannelID]):
                    thisLeader = tempLeaders.pop()
                    output += f"{leaderEmojiIDs[thisLeader]} - {replaceUnderscores(allLeaders[thisLeader])}\n"

                thisMessage = await ctx.send(output + "\n")
                playerDraftMessagePointers[thisChannelID].append(thisMessage)
    else:
        await ctx.send("Run a vote first (use /vote)")

@bot.command(name="vote", description="Starts lobby vote")
async def vote(ctx):
    thisChannelID = ctx.channel.id
    if thisChannelID in lobbyHostingChannels:  # In lobby_hosting channel
        voiceChannel = ctx.guild.get_channel(voiceHostingChannels[thisChannelID])
        playerIDs = [member.id for member in voiceChannel.members]

        messageContent = ctx.message.content
        exceptionalPlayers = decipherIDs(messageContent)
    
        if len(exceptionalPlayers) > 0:
            for player in exceptionalPlayers:
                if player in playerIDs:
                    playerIDs.remove(player)
        
        if len(exceptionalPlayers) > 0:
            for player in exceptionalPlayers:
                if player not in playerIDs:
                    playerIDs.append(player)


        if len(playerIDs) == 0:
            await ctx.send(f"<#{voiceHostingChannels[thisChannelID]}> is empty")
            return
        if len(playerIDs) == 1:
            await ctx.send(
                f"<#{voiceHostingChannels[thisChannelID]}> has an insufficient amount of players (2 minimum)"
            )
            return

        await ctx.channel.purge(limit=500)

        # Players
        output = "Players: "
        i = 0
        for player in playerIDs:
            output += f"<@{player}>"

            if i != len(playerIDs) - 1:
                output += ","
            output += " "

            i += 1

        await ctx.send(output)


        mapMessage = await ctx.send("Map Options: " + formatOptions(allMaps,mapEmojis))
        for reaction in mapEmojis:
            await mapMessage.add_reaction(reaction)

        # Start type
        startTypeMessage = await ctx.send("Start Type: " + formatOptions(allStartOptions,startEmojis))
        for reaction in startEmojis:
            await startTypeMessage.add_reaction(reaction)

        # Crisis or not
        crisisMessage = await ctx.send("Crisis: " + formatOptions(crisisOptions,crisisEmojis))
        for reaction in crisisEmojis:
            await crisisMessage.add_reaction(reaction)

        civMessage = await ctx.send("Civ Bans: (3 bans max)")
        for civ in antiquityCivs:
            reaction = civEmojis[civDict[civ]]
            await civMessage.add_reaction(reaction)

        # Leader Bans
        firstLeaderMessage = await ctx.send("Leader Bans: (5 bans max)")
        for r in range(20):
            await firstLeaderMessage.add_reaction(leaderEmojis[r])

        secondLeaderMessage = await ctx.send("** **")
        for r in range(20, len(allLeaders)):
            await secondLeaderMessage.add_reaction(leaderEmojis[r])

        # Num Leader Options
        numLeaderMessage = await ctx.send("Number of Leader Options per Player:")
        for reaction in numLeaderOptions:
            await numLeaderMessage.add_reaction(reaction)

        # Num Civ Options
        if len(playerIDs) <= 4:
            numCivMessage = await ctx.send("Number of Civilization Options per Player:")
            for reaction in numCivOptions:
                await numCivMessage.add_reaction(reaction)

        finishedMessage = await ctx.send("Done Voting?")
        await finishedMessage.add_reaction("➕")

        remaining = playerIDs.copy()
        allFinished = False

        output = ""
        for player in remaining:
            output += f"<@{player}>\n"

        remainingMessage = await ctx.send(output)

        while not allFinished:
            await asyncio.sleep(doneVotingCheck)

            hasChanged = False

            updatedFinishedMessage = await ctx.fetch_message(finishedMessage.id)

            finishedReactions = updatedFinishedMessage.reactions

            for reaction in finishedReactions:
                async for player in reaction.users():
                    if player.id in remaining:
                        remaining.remove(player.id)
                        hasChanged = True

            if hasChanged:
                output = ""
                for player in remaining:
                    output += f"<@{player}>\n"

                if len(remaining) == 0:
                    allFinished = True
                    await remainingMessage.delete()
                else:
                    await remainingMessage.edit(content=output)
        
        await finishedMessage.clear_reactions()
        await finishedMessage.edit(content = "Vote Finished: Please Wait")

        start = time.time()

        messageIDs = [
            mapMessage.id,
            startTypeMessage.id,
            crisisMessage.id,
            civMessage.id,
            numLeaderMessage.id,
            firstLeaderMessage.id,
            secondLeaderMessage.id
        ]

        allReactions = await fetchAndFormatReactions(ctx,messageIDs,playerIDs)

        mapReactions, startReactions, crisisReactions, civReactions, numLeaderReactions, firstLeaderReactions, secondLeaderReactions = allReactions

        leaderReactions = firstLeaderReactions + secondLeaderReactions
        
        end = time.time()

        await finishedMessage.edit(content = f"Vote Finished: Loading Took {end - start:.2f} Seconds")

        if len(playerIDs) <= 4:
            finalNumCivMessage = await ctx.fetch_message(numCivMessage.id)
            numCivReactions = await formatReactions(finalNumCivMessage.reactions,playerIDs)


        chosenMapIndex = getPick(mapReactions,1,False)[0]

        await ctx.send(
            f"The Map is {mapEmojis[chosenMapIndex]} - {replaceUnderscores(allMaps[chosenMapIndex])}"
        )

        startOption = getPick(startReactions,1,False)[0]
        if startOption == 1:
            await ctx.send("Standard Start - 🇸")
        else:
            await ctx.send("Balanced Start - 🇧")

        crisisOption = getPick(crisisReactions,1,False)[0]

        if crisisOption == 1:
            await ctx.send("Crisis Disabled - 🚫")
        else:
            await ctx.send("Crisis Enabled - ✅")

        bannedCivs = getPick(civReactions,3,True)
        if len(bannedCivs) > 0:
            bannedCivNames = [antiquityCivs[i] for i in bannedCivs]
            bannedCivEmojis = [civEmojiIDs[i] for i in bannedCivs]
            await ctx.send("Civ Bans: " + formatOptions(bannedCivNames,bannedCivEmojis))
        else:
            await ctx.send("No Civ Bans")

        bannedLeaders = getPick(leaderReactions,5,True)
        if len(bannedLeaders) > 0:
            bannedLeaderNames = [allLeaders[i] for i in bannedLeaders]
            bannedLeaderEmojis = [leaderEmojiIDs[i] for i in bannedLeaders]
            await ctx.send("Leader Bans: " + formatOptions(bannedLeaderNames,bannedLeaderEmojis))
        else:
            await ctx.send("No Leader Bans")


        postBanCivs = []
        for i in range(len(antiquityCivs)):
            if not (i in bannedCivs):
                postBanCivs.append(i)

        postBanLeaders = []
        for i in range(len(allLeaders)):
            if not (i in bannedLeaders):
                postBanLeaders.append(i)

        random.shuffle(postBanCivs)
        random.shuffle(postBanLeaders)

        # get number of leaderOptions
        leaderOptions = getPick(numLeaderReactions,1,False)[0] + 1

        civOptions = getPick(numCivReactions,1,False)[0] + 1
        if len(playerIDs) > 4:
            civOptions = 1
            
        global gameHasOccured
        global mostRecentCivOptions
        global mostRecentLeaderOptions
        global mostRecentPlayers
        global mustRecentNumLeaders
        global mostRecentNumCivs
        global playerDraftMessagePointers
        
        gameHasOccured[thisChannelID] = True
        mostRecentCivOptions[thisChannelID] = postBanCivs.copy()
        mostRecentLeaderOptions[thisChannelID] = postBanLeaders.copy()
        mostRecentPlayers[thisChannelID] = playerIDs.copy()
        mustRecentNumLeaders[thisChannelID] = leaderOptions
        mostRecentNumCivs[thisChannelID] = civOptions
        playerDraftMessagePointers[thisChannelID].clear()

        for player in playerIDs:
            output = f"<@{player}>\n"

            output += "__Civ Options:__\n"
            for c in range(civOptions):
                thisCiv = postBanCivs.pop()
                output += f"{civEmojiIDs[thisCiv]} - {replaceUnderscores(antiquityCivs[thisCiv])}\n"

            output += "__Leader Options:__\n"
            for l in range(leaderOptions):
                thisLeader = postBanLeaders.pop()
                output += f"{leaderEmojiIDs[thisLeader]} - {replaceUnderscores(allLeaders[thisLeader])}\n"

            thisMessage = await ctx.send(output + "\n")
            playerDraftMessagePointers[thisChannelID].append(thisMessage)
    else:
        await ctx.send(f"Please only use this command inside a lobby hosting channel")





bot.run(Token)
