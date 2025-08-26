import re
import random

commandPrefix = "!"

def replaceUnderscores(input):
    """Replace underscores with spaces"""
    return input.replace("_", " ")

def replaceSpaces(input):
    """Replace spaces with underscores"""
    return input.replace(" ", "_") 

def formatOptions(names, emojis):
    """Format names and emojis into a readable options string"""
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
    """Optimized function to find n largest values with their indices"""
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
        # Filter out zero counts
        picked = [i for i in picked if countList[i] != 0]

    if len(picked) > n:
        return picked[:n]
    else:
        return picked
    

def decipherIDs(message):
    """Extract user IDs from Discord mention format"""
    IDs = re.findall(r"<@(\d+)>", message)
    return [int(uid) for uid in IDs]


def extractEmojiID(emoji):
    """Extract emoji ID from Discord emoji format"""
    match = re.search(r"<:[A-Za-z_]+:(\d+)>", emoji)
    return match.group(1) if match else None

def extractLeader(message):
    """Extract leader name from leader info command"""
    match = re.search(rf"^{commandPrefix}leaderInfo\s+(.+)", message)
    return match.group(1) if match else "None"
    
def extractMap(message):
    """Extract map name from map info command"""
    match = re.search(rf"^{commandPrefix}mapInfo\s+(.+)", message)
    return match.group(1) if match else "None"


def extractWonder(message):
    """Extract wonder name from wonder info command"""
    match = re.search(rf"^{commandPrefix}wonderInfo\s+(.+)", message)
    return match.group(1) if match else "None"

def capitalizeWord(word):
    """Capitalize first letter and lowercase the rest"""
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

