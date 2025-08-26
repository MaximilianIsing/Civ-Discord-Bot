import discord
from discord import app_commands
from discord.ext import commands
import time
import asyncio
import random
import json
import re
from lists import *
from helpers import *
from storage_management import *
import math

with open("storage/TOKEN.txt", "r") as file:
    content = file.read()

Token = content

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)



thisGuild = None
civGuild = None
wonderGuild = None




mostRecentCivOptions = {channel: [] for channel in lobbyHostingChannels}
mostRecentLeaderOptions = {channel: [] for channel in lobbyHostingChannels}
mostRecentPlayers = {channel: [] for channel in lobbyHostingChannels}
mustRecentNumLeaders = {channel: 0 for channel in lobbyHostingChannels}
mostRecentNumCivs = {channel: 0 for channel in lobbyHostingChannels}
gameHasOccured = {channel: False for channel in lobbyHostingChannels}
voteIsActive = {channel: False for channel in lobbyHostingChannels}
forceVote = {channel: False for channel in lobbyHostingChannels}

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

    initializeJSON()

    hostRole = discord.utils.get(thisGuild.roles, name="Host")
    for channelID in lobbyHostingChannels:
        channel = bot.get_channel(channelID)
        if not channel:
            channel = await bot.fetch_channel(channelID)  # fallback if not cached
        await channel.set_permissions(hostRole, send_messages=True)

    print("Bot Ready")


@bot.event
async def on_message(message):
    
    correctionFound = -1
    for correctionID in range(len(correctedInputs)):
        if correctedInputs[correctionID] in message.content:
            correctionFound = correctionID
            break
    
    if correctionFound != -1:
        newMessage = message
        thisCorrection = commandCorrections[correctionFound]
        newContent = (message.content).replace(thisCorrection.input,thisCorrection.correction)
        newMessage.content = newContent
        ctx = await bot.get_context(newMessage)
        await bot.invoke(ctx)
    else:
        await bot.process_commands(message)


@bot.command(name="sync")
async def sync(ctx):
    if ctx.author.id == OwnerID:
        await bot.tree.sync()

        await ctx.send("Synced")
    else:
        await ctx.send("Insufficient permissions")

@bot.command(name="dropPlayerData")
async def dropplayerdata(ctx):
    if ctx.author.id == OwnerID:
        clearJSON()
        await ctx.send("playerData.json file dropped")
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
 

@bot.command(name="updateElo", description="Updates elo test")
async def updateElo(ctx, key, num):
    updateValue(key,num)
    await ctx.send("Elo updated")



@bot.command(name="wonderList", description="Lists all wonders")
async def wonderList(ctx):
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

@bot.command(name="wonderInfo", description="Gives information about the wonder")
async def wonderInfo(ctx):
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
                name='Civilization:', value=f'{thisWonder.civ} - {civEmojiIDs[civDict[replaceSpaces(thisWonder.civ)]]}', inline=True
            )
        wonderEmbed.add_field(
            name='Unlocked By:', value=f'{thisWonder.unlock}', inline=True
        )


        extractedID = extractEmojiID(wonderEmojiIDs[wonderDict[wonder]])
        emojiUrl = f"https://cdn.discordapp.com/emojis/{extractedID}.png"
        wonderEmbed.set_thumbnail(url=emojiUrl)
        await ctx.send(embed = wonderEmbed)
    else: 
        await ctx.send(f"\"{wonder}\" isn't an option, use /wonderList for a list of options (use exact formatting)")

@bot.command(name="civList", description="Lists all civs")
async def civList(ctx):
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


@bot.command(name="leaderList", description="Lists all leaders")
async def leaderlist(ctx):
    output = "__Leader Options Are:__\n"
    for leader in allLeaders:
        output += f"{replaceUnderscores(leader)} - {leaderEmojiIDs[leaderDict[leader]]}\n"
    await ctx.send(output)

@bot.command(name="bannedLeaders", description="Lists all permabanned leaders")
async def leaderlist(ctx):
    output = "__Permabanned Leaders:__\n "
    bannedLeaderNames = [allLeaders[i] for i in hardBannedLeaderIDs]
    bannedLeaderEmojis = [leaderEmojiIDs[i] for i in hardBannedLeaderIDs]
    output += formatOptions(bannedLeaderNames,bannedLeaderEmojis).replace("|","\n")
    await ctx.send(output)



@bot.command(name="cancelVote",description="Gives information about the leader")
async def cancelVote(ctx):
    thisChannelID = ctx.channel.id
    if thisChannelID in lobbyHostingChannels:
        voteIsActive[thisChannelID] = False
        await ctx.channel.purge(limit=500)
        await ctx.send(f"Vote cancelled")
    else:
        await ctx.send(f"Please only use this command inside a lobby hosting channel")
    
@bot.command(name="forceVote",description="Force ends the current vote")
async def cancelVote(ctx):
    thisChannelID = ctx.channel.id
    if thisChannelID in lobbyHostingChannels:
        forceVote[thisChannelID] = True
        await ctx.send(f"Vote force ended")
    else:
        await ctx.send(f"Please only use this command inside a lobby hosting channel")


@bot.command(name="leaderInfo",description="Gives information about the leader")
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
        await ctx.send(f"\"{leader}\" isn't an option, use /leaderList for a list of options (use exact formatting)")


@bot.command(name="mapList", description="Lists all maps")
async def maplist(ctx):
    output = "__Map Options Are:__\n"
    for map in allMaps:
        output += replaceUnderscores(map) + "\n"
    await ctx.send(output)



@bot.command(name="mapInfo",description="Gives information about the map type")
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
        await ctx.send(f"\"{map}\" isn't an option, use /mapList for a list of options (use exact formatting)")

@bot.command(name="reRoll", description="Rerolls draft picks")
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
    hostRoleID = discord.utils.get(ctx.guild.roles, name="Host")

    if thisChannelID in lobbyHostingChannels:  # In lobby_hosting channel
        
        if voteIsActive[thisChannelID]:
            await ctx.send("A vote is already running in this channel")
            return
        else:
            await ctx.channel.set_permissions(hostRoleID, send_messages=False)

        voiceChannel = ctx.guild.get_channel(voiceHostingChannels[thisChannelID])
        playerIDs = [member.id for member in voiceChannel.members]
        

        

        for excluded in excludededUsers:
            if excluded in playerIDs:
                playerIDs.remove(excluded)

        messageContent = ctx.message.content
        exceptionalPlayers = decipherIDs(messageContent)
    
        if len(exceptionalPlayers) > 0:
            for player in exceptionalPlayers:
                if player in playerIDs:
                    playerIDs.remove(player)
                elif player not in playerIDs:
                    playerIDs.append(player)

        
        if len(playerIDs) == 0:
            await ctx.send(f"<#{voiceHostingChannels[thisChannelID]}> is empty")
            return
        if len(playerIDs) == 0: # To do: return to this
            await ctx.send(
                f"<#{voiceHostingChannels[thisChannelID]}> has an insufficient amount of players (2 minimum)"
            )
            return

        voteIsActive[thisChannelID] = True
        

        thisMaxLeaderOptions = math.floor(
            (len(allLeaders) - len(hardBannedLeaderIDs))/len(playerIDs)
        )
        thisMaxLeaderOptions = min(thisMaxLeaderOptions,maxNumLeaderOptions)

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
        
        turnTimerMessage = await ctx.send("Turn Timer: " + formatOptions(turnTimerOptions,turnTimerEmojis))
        for reaction in turnTimerEmojis:
            await turnTimerMessage.add_reaction(reaction)

        civMessage = await ctx.send("Civ Bans: (3 bans max)")

        counter = 0
        while counter < len(antiquityCivs):
            if counter in hardBannedCivIDs:
                counter += 1
                continue
            civ = antiquityCivs[counter]
            reaction = civEmojis[civDict[civ]]
            await civMessage.add_reaction(reaction)
            counter += 1

        # Leader Bans

        leaderMessages = []

        firstLeaderMessage = await ctx.send("Leader Bans: (5 bans max)")
        leaderMessages.append(firstLeaderMessage)

        counter = 0
        banCounter = 0

        currentMessage = 0

        
        while counter < len(allLeaders):
            if counter in hardBannedLeaderIDs:
                counter += 1
                banCounter += 1
                continue
            if (counter - banCounter) % 20 == 0 and (counter - banCounter) != 0:
                currentMessage += 1
                newMessage = await ctx.send("** **")
                leaderMessages.append(newMessage)
            await leaderMessages[currentMessage].add_reaction(leaderEmojis[counter])
            counter += 1




        # Num Leader Options
        numLeaderMessage = await ctx.send("Number of Leader Options per Player:")
        for reactionIndex in range(thisMaxLeaderOptions):
            await numLeaderMessage.add_reaction(numLeaderOptions[reactionIndex])

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

        await ctx.channel.set_permissions(hostRoleID, send_messages=True)

        while not allFinished:
            await asyncio.sleep(doneVotingCheck)

            if forceVote[thisChannelID]:
                forceVote[thisChannelID] = False
                await remainingMessage.delete()
                break

            if not voteIsActive[thisChannelID]:
                return

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

        await ctx.channel.set_permissions(hostRoleID, send_messages=False)

        await finishedMessage.clear_reactions()
        await finishedMessage.edit(content = "Vote Finished: Please Wait")

        start = time.time()

        leaderMessageIDs = [message.id for message in leaderMessages]

        messageIDs = [
            mapMessage.id,
            startTypeMessage.id,
            crisisMessage.id,
            turnTimerMessage.id,
            civMessage.id,
            numLeaderMessage.id,
        ]
        messageIDs.extend(leaderMessageIDs)

        allReactions = await fetchAndFormatReactions(ctx,messageIDs,playerIDs)

        mapReactions = allReactions[0]
        startReactions = allReactions[1]
        crisisReactions = allReactions[2]
        turnTimerReactions = allReactions[3]
        civReactions = allReactions[4]
        numLeaderReactions = allReactions[5]
        leaderReactions = allReactions[6:]
        leaderReactions  = [item for sublist in leaderReactions for item in sublist]


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
        
        turnTimerOption = getPick(turnTimerReactions,1,False)[0]

        if turnTimerOption == 0:
            await ctx.send("Turn Timer Disabled - ❌")
        elif turnTimerOption == 1:
            await ctx.send("Standard Turn Timer - ⏰")
        else:
            await ctx.send("Dynamic Turn Timer - ⏱️")

        for ID in hardBannedCivIDs:
            civReactions.insert(ID,0)

        bannedCivs = getPick(civReactions,3,True)

        for ID in hardBannedCivIDs:
            bannedCivs.append(ID)

        if len(bannedCivs) > 0:
            bannedCivNames = [antiquityCivs[i] for i in bannedCivs]
            bannedCivEmojis = [civEmojiIDs[i] for i in bannedCivs]
            await ctx.send("Civ Bans: " + formatOptions(bannedCivNames,bannedCivEmojis))
        else:
            await ctx.send("No Civ Bans")


        for ID in hardBannedLeaderIDs:
            leaderReactions.insert(ID,0)

        bannedLeaders = getPick(leaderReactions,5,True)

        for ID in hardBannedLeaderIDs:
            bannedLeaders.append(ID)

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
        voteIsActive[thisChannelID] = False
        await ctx.channel.set_permissions(hostRoleID, send_messages=True)
    else:
        await ctx.send(f"Please only use this command inside a lobby hosting channel")
    


bot.run(Token)