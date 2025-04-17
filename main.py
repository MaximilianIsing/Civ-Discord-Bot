import discord
from discord import app_commands
from discord.ext import commands
import time
import asyncio
import random
import re


with open("TOKEN.txt", "r") as file:
    content = file.read()

Token = content

intents = discord.Intents.default()
intents.message_content = True
OwnerID = 424980696264867880
bot = commands.Bot(command_prefix="/", intents=intents)

doneVotingCheck = 2 # Num of seconds between checks

allCivs = [
        "Aksum",
        "Carthage",
        "Egypt",
        "Greece",
        "Han",
        "Khmer",
        "Maurya",
        "Maya",
        "Mississippian",
        "Persia",
        "Rome",
    ]


allLeaders = [
        "Ada_Lovelace",
        "Amina",
        "Ashoka_World_Conqueror",
        "Ashoka_World_Renouncer",
        "Augustus",
        "Benjamin_Franklin",
        "Catherine_the_Great",
        "Charlemagne",
        "Confucius",
        "Friedrich_Baroque",
        "Friedrich_Oblique",
        "Harriet_Tubman",
        "Hatshepsut",
        "Himiko_High_Shaman",
        "Himiko_Queen_of_Wa",
        "Ibn_Battuta",
        "Isabella",
        "Jose_Rizal",
        "Lafayette",
        "Machiavelli",
        "Napoleon_Emperor",
        "Napoleon_Revolutionary",
        "Pachacuti",
        "Simon_Bolivar",
        "Tecumseh",
        "Trung_Trac",
        "Xerxes_King_of_Kings",
        "Xerxes_the_Achaemenid",
    ]


allMaps = [
        "Continents",
        "Continents_Plus",
        "Archipelago",
        "Fractal",
        "Shuffle",
        "Terra_Incognita",
    ]

mapEmojis = ["🇨", "🇵", "🇦", "🇫", "🇸", "🇹"]


allStartOptions = [
        "Balanced",
        "Standard"
    ]

startEmojis =  ["🇧","🇸"]


crisisOptions =  [
        "Enabled",
        "Disabled"
    ]

crisisEmojis = ["✅", "🚫"]


numLeaderOptions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]


numCivOptions =  ["1️⃣", "2️⃣"]

mostRecentCivOptions = []
mostRecentLeaderOptions = []
mostRecentPlayers = []

gameHasOccured = False

civEmojis = []
leaderEmojis = []
civEmojiIDs = [None] * len(allCivs)
leaderEmojiIDs = [None] * len(allLeaders)



def replaceUnderscores(input):
    return input.replace("_", " ")


@bot.event
async def on_ready():
    print(f"Bot Ready")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command(name="sync")
async def sync(ctx):
    if ctx.author.id == OwnerID:
        await bot.tree.sync()

        for civ in allCivs:
            civEmojis.append(discord.utils.get(ctx.guild.emojis, name=civ))

        for leader in allLeaders:
            leaderEmojis.append(discord.utils.get(ctx.guild.emojis, name=leader))

        for i in range(len(civEmojiIDs)):
            civEmojiIDs[i] = f"<:{civEmojis[i].name}:{civEmojis[i].id}>"

        for i in range(len(leaderEmojiIDs)):
            leaderEmojiIDs[i] = f"<:{leaderEmojis[i].name}:{leaderEmojis[i].id}>"

        await ctx.send("Synced")
    else:
        await ctx.send("Insufficient permissions")


@bot.command(name="clear")
async def clear(ctx):
    if ctx.author.id == OwnerID:
        await ctx.channel.purge(limit=500)
    else:
        await ctx.send("Insufficient permissions")


@bot.command(name="status", description="Say hello!")
async def status(ctx):
    await ctx.send("Status: Online")


def formatOptions(names, emojis):
    output = ""
    for i in range(len(names)):
        output += emojis[i]
        output += " - "
        output += replaceUnderscores(names[i])

        if i != len(names) - 1:
            output += " |"
        output += " "
    return output

async def formatReactions(reactionList, allPlayers):
    countList = [0] * len(reactionList)

    for r in range(len(reactionList)):
       userReactions = reactionList[r].users()
       async for user in userReactions:
            if user.id in allPlayers:
                countList[r] += 1
    return countList



def getNLargest(countsList, n):
    if len(countsList) <= n:
        return [[i] for i in range(len(countsList))]

    # Initialize counts and indices
    counts = [0] * n
    indices = [[] for i in range(n)]  # Use lists to store indices

    for i in range(len(countsList)):
        for k in range(n):
            if countsList[i] > counts[k]:
                # Shift elements down and insert the new value
                for p in range(n - 1, k - 1, -1):
                    if p == k:
                        counts[p] = countsList[i]
                        indices[p] = [i]  # Reset indices for this position
                    else:
                        counts[p] = counts[p - 1]
                        indices[p] = indices[p - 1]
                break
            elif countsList[i] == counts[k]:
                # Append index if the value is equal to the current value
                indices[k].append(i)
                break

    return indices

def flattenList(list): # Flattens by 1 degree
    output = []
    for sublist in list:
        for value in sublist:
            output.append(value)
    return output

def getPick(countList, n, nonePossible):
    picked = getNLargest(countList,n)
    for i in range(len(picked)):
        random.shuffle(picked[i])
    picked = flattenList(picked)
    if nonePossible:
        options = []
        for i in picked:
            if countList[i] != 0:
                options.append(i)
        picked = options

    if len(picked) > n:
        return picked[:n]
    else:
        return picked


async def fetchAndFormatReactions(ctx,message_ids, playerIDs):
    # Fetch messages concurrently
    messages = await asyncio.gather(*[ctx.fetch_message(msg_id) for msg_id in message_ids])
    # Format reactions concurrently for each message
    reactions = await asyncio.gather(*[
        formatReactions(message.reactions, playerIDs) for message in messages
    ])

    return reactions

@bot.command(name="admin_vote", description = "Admin vote start")
async def admin_vote(ctx):
    if ctx.author.id == OwnerID:
        await vote(ctx, True)
    else:
        await ctx.send("Insufficient permissions")

def decipherIDs(message):
    IDs = re.findall(r"<@(\d+)>", message)
    IDs = [int(uid) for uid in IDs]

    return IDs

@bot.command(name="vote", description="Starts lobby vote")
async def vote(ctx, admin = False):
    lobbyHostingChannel = 1351993272096260127
    if ctx.channel.id == lobbyHostingChannel:  # In lobby_hosting channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Game Lobby")
        playerIDs = [member.id for member in voiceChannel.members]

        messageContent = ctx.message.content
        excludedPlayers = decipherIDs(messageContent)

        hasExcluded = False
        if len(excludedPlayers) > 0:
            for player in excludedPlayers:
                if player in playerIDs:
                    playerIDs.remove(player)
                    hasExcluded = True

        if len(playerIDs) == 0:
            await ctx.send(f"<#{1351989426951295056}> is empty")
            return
        if len(playerIDs) == 1 and not admin:
            await ctx.send(
                f"<#{1351989426951295056}> has an insufficient amount of players (2 minimum)"
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
        
        if hasExcluded:
            i = 0
            for player in excludedPlayers:
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
        for reaction in civEmojis:
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
                else:
                    await remainingMessage.edit(content=output)
        
        await remainingMessage.edit(content = "Vote Finished, Please Wait")

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
            bannedCivNames = [allCivs[i] for i in bannedCivs]
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
        for i in range(len(allCivs)):
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
        
        gameHasOccured = True
        mostRecentCivOptions = postBanCivs.copy()
        mostRecentLeaderOptions = postBanLeaders.copy()
        mostRecentPlayers = playerIDs.copy()

        for player in playerIDs:
            output = f"<@{player}>\n"

            output += "__Civ Options:__\n"
            for c in range(civOptions):
                thisCiv = postBanCivs.pop()
                output += f"{civEmojiIDs[thisCiv]} - {replaceUnderscores(allCivs[thisCiv])}\n"

            output += "__Leader Options:__\n"
            for l in range(leaderOptions):
                thisLeader = postBanLeaders.pop()
                output += f"{leaderEmojiIDs[thisLeader]} - {replaceUnderscores(allLeaders[thisLeader])}\n"

            await ctx.send(output + "\n")
    else:
        await ctx.send(f"Please use <#{lobbyHostingChannel}> for this command")

@bot.command(name="reroll", description="Rerolls draft picks")
async def reroll(ctx):
    tempCivs = mostRecentCivOptions.copy()
    tempLeaders = mostRecentLeaderOptions.copy()

    for player in mostRecentPlayers:
            output = f"<@{player}>\n"

            output += "__Civ Options:__\n"
            for c in range(tempCivs):
                thisCiv = tempCivs.pop()
                output += f"{civEmojiIDs[thisCiv]} - {replaceUnderscores(allCivs[thisCiv])}\n"

            output += "__Leader Options:__\n"
            for l in range(tempLeaders):
                thisLeader = tempLeaders.pop()
                output += f"{leaderEmojiIDs[thisLeader]} - {replaceUnderscores(allLeaders[thisLeader])}\n"

            await ctx.send(output + "\n")



bot.run(Token)
