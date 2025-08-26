import re
import random

commandPrefix = "!"

def replaceUnderscores(input):
    return input.replace("_", " ")

def replaceSpaces(input):
    return input.replace(" ", "_") 

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

    for r, reaction in enumerate(reactionList):
       userReactions = [user async for user in reaction.users()]
       countList[r] += sum(1 for user in userReactions if user.id in allPlayers)
    return countList

async def fetchAndFormatReactions(ctx, messageIDs, playerIDs):
    loadingBarMessage = list("▱" * len(messageIDs))
    loadingBar = await ctx.send("".join(loadingBarMessage))

    reactions = [None] * len(messageIDs)
    playerSet = set(playerIDs)

    i = 0
    for messageID in messageIDs:
        message = await ctx.fetch_message(messageID)
        formatted = await formatReactions(message.reactions, playerSet)

        loadingBarMessage[i] = "▰"
        await loadingBar.edit(content = "".join(loadingBarMessage))
        reactions[i] = formatted
        i += 1
        
    await loadingBar.delete()
    return reactions

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
    

def decipherIDs(message):
    IDs = re.findall(r"<@(\d+)>", message)
    IDs = [int(uid) for uid in IDs]

    return IDs


def extractEmojiID(emoji):
    match = re.search(r"<:[A-Za-z_]+:(\d+)>", emoji)
    return match.group(1)

def extractLeader(message):
    match = re.search(rf"^{commandPrefix}leaderInfo\s+(.+)", message)
    if match:
        return match.group(1)
    else:
        return "None"
    
def extractMap(message):
    match = re.search(rf"^{commandPrefix}mapInfo\s+(.+)", message)
    if match:
        return match.group(1)
    else:
        return "None"


def extractWonder(message):
    match = re.search(rf"^{commandPrefix}wonderInfo\s+(.+)", message)
    if match:
        return match.group(1)
    else:
        return "None"

def capitalizeWord(word):
    return word[0].upper() + word[1:].lower()

def autoCapitalize(message):
    exceptions = ["Of", "A", "O","De"]

    words = message.split('_')
    result = []
    for word in words:
        if word:
            if capitalizeWord(word) in exceptions:
                formatted_word = word.lower()
            else:
                formatted_word = word[0].upper() + word[1:].lower()
            result.append(formatted_word)
    return '_'.join(result)

