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

leaderInfoList = {
        "Ada_Lovelace": "Cities receive +2 Science per Age after you complete a Civic Mastery. This resets at the start of each Age. Gain Culture equal to 50% of your total Science per turn when you complete a Technology Mastery.",
        "Amina": "+1 Resource Capacity in Cities. +1 Gold per Age for each Resource assigned to Cities. +5 Combat Strength on all Units in Plains and Desert.",
        "Ashoka_World_Conqueror": "+1 Production in Cities for every 5 excess Happiness. +10% Production in Settlements not founded by you. Declaring a Formal War grants a Celebration. +5 Combat Strength against Fortified Districts for all Units during a Celebration.",
        "Ashoka_World_Renouncer": "+1 Food in Cities for every 5 excess Happiness. +10% Food in all Settlements during a Celebration. All Buildings gain a +1 Happiness adjacency for all Improvements.",
        "Augustus": "+2 Production in the Capital for every Town. Can purchase Culture Buildings in Towns. +50% Gold towards purchasing Buildings in Towns.",
        "Benjamin_Franklin": "+1 Science per Age on Production Buildings in Cities. +50% Production towards constructing Production Buildings. +1 Science  per Age from active Endeavors you started or supported. Can have two Endeavors of the same type active at a time.",
        "Catherine_the_Great": "+2 Culture per Age on displayed Great Works. Buildings with Great Work slots gain 1 additional slot. Cities settled in Tundra gain Science equal to 25% of their Culture per turn.",
        "Charlemagne": "Military and Science Buildings receive a Happiness adjacency for Quarters. Gain 2 Cavalry units, once unlocked, when entering a Celebration. +5 Combat Strength for Cavalry units during a Celebration.",
        "Confucius": "+25% Growth Rate in all Cities. +2 Science from Specialists.",
        "Friedrich_Baroque": "Gain a Great Work upon capturing a Settlement for the first time. Gain an Infantry Unit when you construct a Culture Building.",
        "Friedrich_Oblique": "Army Commanders start with the Merit Commendation, granting them +1 Command Radius. Gain an Infantry Unit when you construct a Science Building.",
        "Harriet_Tubman": "+50% Influence towards initiating Espionage actions. Gain 5 War Support on all wars declared against you. Units ignore movement penalties from Vegetation.",
        "Hatshepsut": "+1 Culture for every imported Resource. +15% Production towards the construction of Buildings and Wonder in Cities adjacent to Navigable Rivers.",
        "Himiko_High_Shaman": "+2 Happiness per Age on Happiness Buildings. +50% Production towards constructing Happiness Buildings. +20% Culture but -10% Science. These effects are doubled during a Celebration.",
        "Himiko_Queen_of_Wa": "Gain a unique Endeavor, Friend of Wei, which can be performed in an Alliance to grant you and your ally +25% Science. Can support Endeavors for free. +4 Science per Age for every leader you're Friendly or Helpful with.",
        "Ibn_Battuta": "Gains 2 Attribute points after the first Civic in every Age. +1 Sight for all Units. Gain a unique Endeavor called Trade Maps that lets you gradually see other Leaders' explored areas.",
        "Isabella": "Gain 300 Gold every time you discover a Natural Wonder, doubled if the Natural Wonder is in Distant Lands. +100% tile yields from Natural Wonders, +50% Gold towards purchasing Naval Units, and -1 Gold Maintenance for Naval Units.",
        "Jose_Rizal": "When gaining rewards from a Narrative Event, gain +20 Culture and Gold per Age. +50% Celebration duration and Happiness towards Celebrations. Has additional Narrative Events.",
        "Lafayette": "Gains a unique Endeavor, Reform, which grants an additional Social Policy slot. Supporting this Endeavor also grants the other Leader an additional Social Policy slot. +1 Combat Strength for all Units for each Tradition, but not Policy, slotted in the Government. +1 Culture and Happiness per Age in Settlements, doubled for Settlements in Distant Lands.",
        "Machiavelli": "Gain +3 Influence per Age. Gain 50 Gold per Age when your Diplomatic Action proposals are accepted, or 100 Gold per Age when they are rejected. Ignore Relationship requirements for declaring Formal Wars. You can Levy Military Units from City-states you are not Suzerain of.",
        "Napoleon_Emperor": "Gain a unique Sanction, Continental System, which reduces the Trade Route limit of the targeted Leader to all other Leaders by 1, causes a massive relationship penalty, and costs more to reject. +8 Gold per Age for every Leader you are Unfriendly or Hostile with. Can reject Endeavors for free.",
        "Napoleon_Revolutionary": "+1 Movement for all Land Units. Defeating an enemy Unit provides Culture equal to of 50% its Combat Strength.",
        "Pachacuti": "All Buildings gain a Food adjacency for Mountains. Specialists adjacent to Mountains do not cost Happiness maintenance.",
        "Simon_Bolivar": "Gain 1 War Support on all wars. Upon conquering a Settlement for the first time, can purchase 1 Constructible for free. Unrest does not prevent Purchasing.",
        "Tecumseh": "+1 Food and Production per Age in Settlements for every City-state you are Suzerain of. +1 Combat Strength for all your Units for every City-State you are Suzerain of.",
        "Trung_Trac": "+3 free Promotions on your first Army Commander. Your Commanders gain +20% experience. +10% Science in Cities on Tropical tiles; this bonus is doubled during any Formal War you declare.",
        "Xerxes_King_of_Kings": "+3 Combat Strength for Units that are attacking in neutral or enemy territory. +100 Culture and Gold per Age upon capturing a Settlement for the first time. +10% Gold in all Settlements, doubled in Settlements not founded by you. +1 Settlemen t limit per Age.",
        "Xerxes_the_Achaemenid": "+1 Trade Route limit with all other leaders. +50 Culture and +100 Gold per Age when you create a Trade Route or Road. +1 Culture and Gold per Age on unique buildings and unique tile improvements."
    }

leaderUnlocks = {
        "Ada_Lovelace": "British",
        "Amina": "Songhai, Bugandan",
        "Ashoka_World_Conqueror": "Chola, Nepalese",
        "Ashoka_World_Renouncer": "Chola, Nepalese",
        "Augustus": "None",
        "Benjamin_Franklin": "American",
        "Catherine_the_Great": "Russian",
        "Charlemagne": "Norman",
        "Confucius": "Ming, Qing",
        "Friedrich_Baroque": "Prussian",
        "Friedrich_Oblique": "Prussian",
        "Harriet_Tubman": "American",
        "Hatshepsut": "None",
        "Himiko_High_Shaman": "Meiji Japanese",
        "Himiko_Queen_of_Wa": "Meiji Japanese",
        "Ibn_Battuta": "Abbasid",
        "Isabella": "Spanish, Mexican",
        "Jose_Rizal": "Hawaiian",
        "Lafayette": "French Imperial",
        "Machiavelli": "None",
        "Napoleon_Emperor": "French Imperial",
        "Napoleon_Revolutionary": "French Imperial",
        "Pachacuti": "Incan",
        "Simon_Bolivar": "Mexican",
        "Tecumseh": "Shawnee, American, Mexican",
        "Trung_Trac": "Majapahit",
        "Xerxes_King_of_Kings": "None",
        "Xerxes_the_Achaemenid": "None"
}

allMaps = [
        "Continents",
        "Continents_Plus",
        "Archipelago",
        "Fractal",
        "Shuffle",
        "Terra_Incognita",
    ]

mapInfoList = {
        "Continents":"The Continents Plus map is the default recommended map type, and features two major landmasses, with several small islands scattered in between. These islands often contain Distant Land resources which can be worked to produce Treasure Fleets.",
        "Continents_Plus":"The regular Continents map features two large landmasses, without the islands scattered in between, although there are occasionally a couple of them dotted around.",
        "Archipelago":"The Archipelago map is roughly divided into two distinct halves, but instead of two main continents, there are several disconnected or thinly connected land masses on each side. There's plenty of water and coastal tiles, favoring a naval focused campaign.",
        "Fractal":"Fractal map generation produces more randomly shaped land masses, which seems to result in fewer blunt edges/'unnatural' shapes, but less actual land area overall. There are still two major 'continent' areas and smaller islands between them, but continents may be split into several parts.",
        "Shuffle":"Shuffle maps use a randomized preset to generate the map. We're not sure yet exactly how these calculations are made, but based on the map generation script files, Archipelago, Continents, and Fractal are all possibilities.",
        "Terra_Incognita":"Terra Incognita generates a standard Continents map as the homeland landmass, and uses a randomized preset to generate the second landmass."
}

mapInfoLinks = {
        "Continents":"https://oyster.ignimgs.com/mediawiki/apis.ign.com/civilization-7/1/19/Continents-standard.jpg?width=2240",
        "Continents_Plus":"https://oyster.ignimgs.com/mediawiki/apis.ign.com/civilization-7/e/ef/Continents-plus-standard.jpg?width=2240",
        "Archipelago":"https://oyster.ignimgs.com/mediawiki/apis.ign.com/civilization-7/d/d3/Arch-standard.jpg?width=2240",
        "Fractal":"https://oyster.ignimgs.com/mediawiki/apis.ign.com/civilization-7/4/4e/Fractal-standard.jpg?width=2240",
        "Shuffle":"https://oyster.ignimgs.com/mediawiki/apis.ign.com/civilization-7/f/f0/Shuffle-standard.jpg?width=2240",
        "Terra_Incognita":"https://oyster.ignimgs.com/mediawiki/apis.ign.com/civilization-7/5/52/Terra-standard.jpg?width=2240"
}

mapFavoring = {
        "Continents": "Heavy land favored",
        "Continents_Plus": "Slightly land favored",
        "Archipelago": "Heavily naval favored",
        "Fractal": "Naval favored",
        "Shuffle": "Land favored",
        "Terra_Incognita": "Slightly land favored"

}

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
mustRecentNumLeaders = 0
mostRecentNumCivs = 0

gameHasOccured = False

hasSynced = False

civEmojis = []
leaderEmojis = []
civEmojiIDs = [None] * len(allCivs)
leaderEmojiIDs = [None] * len(allLeaders)


def replaceUnderscores(input):
    return input.replace("_", " ")


@bot.event
async def on_ready():
    print("Bot Ready")




@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command(name="sync")
async def sync(ctx):
    global hasSynced

    if ctx.author.id == OwnerID:
        hasSynced = True
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
        print("Clearing")
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


async def fetchAndFormatReactions(ctx, messageIDs, playerIDs):
    reactions = [None] * len(messageIDs)
    playerSet = playerIDs

    i = 0
    for messageID in messageIDs:
        message = await ctx.fetch_message(messageID)
        formatted = await formatReactions(message.reactions,playerSet)
        reactions[i] = formatted
        i += 1

    return reactions

def decipherIDs(message):
    IDs = re.findall(r"<@(\d+)>", message)
    IDs = [int(uid) for uid in IDs]

    return IDs

@bot.command(name="leaderlist", description="Lists all leaders")
async def leaderlist(ctx):
    output = "__Leader Options Are:__\n"
    for leader in allLeaders:
        output += leader + "\n"
    await ctx.send(output)

@bot.command(name="leaderinfo",description="Gives information about the leader")
async def leaderinfo(ctx, leader):

    if leader in allLeaders:
        mapEmbed = discord.Embed(
            title = replaceUnderscores(leader),
            description = leaderInfoList[leader] + "\n\nUnlocks: " + leaderUnlocks[leader],
            color = discord.Color.orange()
        )
        await ctx.send(embed = mapEmbed)
    else: 
        await ctx.send(f"\"{map}\" isn't an option, use /leaderlist for a list of options (use exact formatting)")


@bot.command(name="maplist", description="Lists all maps")
async def maplist(ctx):
    output = "__Map Options Are:__\n"
    for map in allMaps:
        output += map + "\n"
    await ctx.send(output)

@bot.command(name="mapinfo",description="Gives information about the map type")
async def mapinfo(ctx, map):
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
    

    if gameHasOccured:
        global mostRecentCivOptions
        global mostRecentLeaderOptions
        global mostRecentPlayers
        global mustRecentNumLeaders
        global mostRecentNumCivs

        print("Rerolling")
        tempCivs = mostRecentCivOptions.copy()
        tempLeaders = mostRecentLeaderOptions.copy()

        random.shuffle(tempCivs)
        random.shuffle(tempLeaders)

        for player in mostRecentPlayers:
                output = f"<@{player}>\n"

                output += "__Civ Options:__\n"
                for c in range(mostRecentNumCivs):
                    thisCiv = tempCivs.pop()
                    output += f"{civEmojiIDs[thisCiv]} - {replaceUnderscores(allCivs[thisCiv])}\n"

                output += "__Leader Options:__\n"
                for l in range(mustRecentNumLeaders):
                    thisLeader = tempLeaders.pop()
                    output += f"{leaderEmojiIDs[thisLeader]} - {replaceUnderscores(allLeaders[thisLeader])}\n"

                await ctx.send(output + "\n")
    else:
        await ctx.send("Run a vote first (use /vote)")

@bot.command(name="vote", description="Starts lobby vote")
async def vote(ctx):
    global hasSynced
    if not hasSynced:
        await sync(ctx)
    lobbyHostingChannel = 1351993272096260127
    if ctx.channel.id == lobbyHostingChannel:  # In lobby_hosting channel
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Game Lobby")
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
            await ctx.send(f"<#{1351989426951295056}> is empty")
            return
        if len(playerIDs) == 1:
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
            
        global gameHasOccured
        global mostRecentCivOptions
        global mostRecentLeaderOptions
        global mostRecentPlayers
        global mustRecentNumLeaders
        global mostRecentNumCivs
        
        gameHasOccured = True
        mostRecentCivOptions = postBanCivs.copy()
        mostRecentLeaderOptions = postBanLeaders.copy()
        mostRecentPlayers = playerIDs.copy()
        mustRecentNumLeaders = leaderOptions
        mostRecentNumCivs = civOptions

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





bot.run(Token)
