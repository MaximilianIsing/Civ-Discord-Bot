from helpers import *

antiquityCivs = [
        "Aksum",
        "Assyria",
        "Carthage",
        "Egypt",
        "Greece",
        "Han",
        "Khmer",
        "Maurya",
        "Maya",
        "Mississippian",
        "Persia",
        "Rome"
    ]
explorationCivs = [
        "Abbasid",
        "Bulgaria",
        "Chola",
        "Hawaii",
        "Inca",
        "Majapahit",
        "Ming",
        "Mongolia",
        "Norman",
        "Shawnee",
        "Songhai",
        "Spain"
]
modernCivs = [
        "America",
        "Buganda",
        "French_Empire",
        "Great_Britain",
        "Meiji_Japan",
        "Mexico",
        "Mughal",
        "Nepal",
        "Prussia",
        "Qing",
        "Russia",
        "Siam"
]

allCivs = antiquityCivs + explorationCivs + modernCivs
civDict = {civ: index for index, civ in enumerate(allCivs)}

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
        "Xerxes_the_Achaemenid"
    ]
leaderDict = {leader: index for index, leader in enumerate(allLeaders)}
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
        "Ada_Lovelace": "Great Britain",
        "Amina": "Songhai, Bugandan",
        "Ashoka_World_Conqueror": "Chola, Nepal",
        "Ashoka_World_Renouncer": "Chola, Nepal",
        "Augustus": "None",
        "Benjamin_Franklin": "America",
        "Catherine_the_Great": "Russia",
        "Charlemagne": "Norman",
        "Confucius": "Ming, Qing",
        "Friedrich_Baroque": "Prussia",
        "Friedrich_Oblique": "Prussia",
        "Harriet_Tubman": "America",
        "Hatshepsut": "None",
        "Himiko_High_Shaman": "Meiji Japan",
        "Himiko_Queen_of_Wa": "Meiji Japan",
        "Ibn_Battuta": "Abbasid",
        "Isabella": "Spain, Mexico",
        "Jose_Rizal": "Hawaii",
        "Lafayette": "French Empire",
        "Machiavelli": "None",
        "Napoleon_Emperor": "French Empire",
        "Napoleon_Revolutionary": "French Empire",
        "Pachacuti": "Inca",
        "Simon_Bolivar": "Mexico",
        "Tecumseh": "Shawnee, America, Mexico",
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
        "Pangeaea_Plus"
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
        "Continents": "Heavily land favored",
        "Continents_Plus": "Slightly land favored",
        "Archipelago": "Heavily naval favored",
        "Fractal": "Naval favored",
        "Shuffle": "Land favored",
        "Terra_Incognita": "Slightly land favored"

}

mapEmojis = ["🇨", "🇺", "🇦", "🇫", "🇸", "🇹","🇵"]


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

turnTimerOptions = [
        "Disabled",
        "Stanard",
        "Dynamic"
    ]

turnTimerEmojis = [
        "❌",
        "⏰",
        "⏱️"
    ]




numLeaderOptions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣","5️⃣","6️⃣","7️⃣","8️⃣"]

maxNumLeaderOptions = len(numLeaderOptions)

numCivOptions =  ["1️⃣", "2️⃣"]

class Wonder:
    def __init__(self, age, name, cost, civ, unlock, effect, condition):
        self.age = age
        self.name = name
        self.cost = cost
        self.civ = civ
        self.unlock = unlock
        self.effect = effect
        self.condition = condition


antiquityWonders = [
    Wonder("Antiquity","Angkor Wat", 450, "Khmer", "Civic: Philosophy", "+3 Happiness. +1 Specialist limit in this Settlement.", "Adjacent to a River tile."),
    Wonder("Antiquity","Byrsa", 375, "Carthage", "Tech: Sailing", "+2 Gold. Trade Routes from this Settlement cannot be plundered. All tiles in this City adjacent to Coast receive a Wall if eligible for it.", "Adjacent to Coast."),
    Wonder("Antiquity","Colosseum", 450, "Rome", "Civic: Entertainment", "+3 Culture. +2 Happiness on Quarters in this Settlement.", "Adjacent to a District."),
    Wonder("Antiquity","Colossus", 450, "None", "Civic: Skilled Trades", "+3 Gold. +3 Resource Capacity in this Settlement. +1 Economic Attribute point.", "On Coast adjacent to land."),
    Wonder("Antiquity","Dur Sharrukin", 275, "None", "Civic: Discipline", "Acts like a Fortified District. +3 Combat Strength to all Fortified Districts in all Settlements.", "On a Flat tile."),
    Wonder("Antiquity","Emile Bell", 275, "None", "Civic: Code of Laws Mastery", "Gain a unique Endeavor, Ginseng Agreement, which grants Food in both Leaders' Capital. +1 Diplomatic Attribute point.", "On a Rough tile."),
    Wonder("Antiquity","Gate of All Nations", 275, "Persia", "Civic: Discipline Mastery", "+2 Support on all Wars.", "Adjacent to a District."),
    Wonder("Antiquity","Great Stele", 275, "Aksum", "Tech: Writing", "+200 Gold every time a Wonder is completed in this Settlement, including the Great Stele.", "On a Flat tile."),
    Wonder("Antiquity","Haamonga a Maui", 375, "None", "Tech: Navigation", "+2 Culture. +1 Culture and +1 Food on Fishing Boats in this Settlement. +1 Cultural Attribute point.", "On a Grassland or Tropical tile adjacent to Coast."),
    Wonder("Antiquity","Hanging Gardens", 275, "None", "Tech: Irrigation", "+1 Food on Farms in this Settlement. +10% growth rate in all cities. +1 Expansionist Attribute point.", "Adjacent to a River."),
    Wonder("Antiquity","Mausoleum of Theodoric", 450, "None", "Civic: Organized Military", "+3 Production. +100% yields and HP from pillaging. +1 Militaristic Attribute point.", "Adjacent to Coast."),
    Wonder("Antiquity","Monks Mound", 450, "Mississippian", "Civic: Commerce", "+4 Food. +4 Resource Capacity in this Settlement.", "Adjacent to a River."),
    Wonder("Antiquity","Mundo Perdido", 275, "Maya", "Civic: Mysticism Mastery", "+1 Happiness and +1 Science on Tropical tiles in this Settlement.", "On a Tropical tile."),
    Wonder("Antiquity","Nalanda", 450, "None", "Civic: Literacy", "+3 Science. +1 Codex. Has 2 Codex slots. +1 Scientific Attribute point.", "On a Plains tile."),
    Wonder("Antiquity","Oracle", 375, "Greece", "Civic: Public Life", "+2 Culture. When gaining rewards from a Narrative Event, gain additional +10 Culture per Age.", "On a Rough tile."),
    Wonder("Antiquity","Petra", 375, "None", "Civic: Code of Laws", "+2 Gold. +1 Gold and +1 Production for every Desert tile in this Settlement.", "On a Desert tile."),
    Wonder("Antiquity","Pyramid of The Sun", 450, "None", "Tech: Mathematics", "+3 Culture. +3 Culture on each Quarter in this Settlement.", "On a Flat tile adjacent to a District."),
    Wonder("Antiquity","Pyramids", 275, "Egypt", "Tech: Masonry", "+1 Gold and +1 Production on minor and Navigable River tiles in this Settlement.", "On a Desert adjacent to a Navigable River tile."),
    Wonder("Antiquity","Sanchi Stupa", 375, "Maurya", "Civic: Citizenship Mastery", "+2 Happiness. +1 Culture for excess Happiness in this Settlement.", "On a Plains tile."),
    Wonder("Antiquity","Terracotta Army", 375, "None", "Civic: Tactics", "+2 Production. Grants a free Army Commander when built. +25% Army experience.", "On a Grassland tile."),
    Wonder("Antiquity","Weiyang Palace", 375, "Han", "Civic: Citizenship", "+6 Influence.", "On a Grassland tile."),
]
explorationWonders = [
    Wonder("Exploration","Borobudur", 475, "Majapahit", "Civic: Bureaucracy", "+3 Happiness. +2 Food and +2 Happiness on Quarters.", "Adjacent to a Coast tile."),
    Wonder("Exploration","Brihadeeswarar Temple", 475, "Chola", "Civic: Diplomatic Service", "+3 Influence. All Buildings with an active adjacency receive +1 Happiness adjacency with Navigable Rivers.", "On a Minor River or adjacent to a Navigable River."),
    Wonder("Exploration","El Escorial", 475, "Spain", "Civic: Colonialism Mastery", "+3 Happiness. Has 3 Relic slots. +1 Settlement Limit. +4 Happiness on cities within 7 tiles of this Wonder.", "On a Rough tile."),
    Wonder("Exploration","Erdene Zuu", 550, "Mongolia", "Civic: Imperialism Mastery", "+4 Culture. Creating a Cavalry Unit grants Culture equal to 25% of its cost.", "On Flat Plains, Flat Tundra, or Flat Desert tile."),
    Wonder("Exploration","Forbidden City", 400, "Ming", "Civic: Authority Mastery", "+2 Culture. +2 Culture and +2 Gold on all Fortification buildings in this Settlement.", "Adjacent to a District."),
    Wonder("Exploration","Hale o Keawe", 400, "Hawaii", "Civic: Inspiration", "+2 Culture. Constructing a building on Coast grants Culture equal to 50% of its cost. Has 3 Relic slots.", "Adjacent to Coast, but not adjacent to Tundra."),
    Wonder("Exploration","House of Wisdom", 475, "Abbasid", "Civic: Society Mastery", "+3 Science. Gains 3 Relics. +2 Science on Great Works. Has 3 Relic slots.", "Adjacent to an Urban district."),
    Wonder("Exploration","Machu Pikchu", 550, "Inca", "Tech: Urban Planning", "+4 Gold. Increased Resource Capacity in this Settlement. +4 Culture and +4 Gold on all tiles adjacent to this Wonder.", "On a Tropical Mountain tile."),
    Wonder("Exploration","Notre Dame", 550, "None", "Civic: Social Class Mastery", "+4 Happiness. All Specialists provide +3 Culture during celebrations. Start a celebration immediately upon completion.", "Adjacent to a River and a District."),
    Wonder("Exploration","Rila Monastery", 550, "Bulgaria", "Tech: Heraldry", "+4 Culture. Has 3 Relic Slots. Receive a Relic every time you build a Wonder, including this one.", "Not adjacent to a District."),
    Wonder("Exploration","Serpent Mound", 550, "Shawnee", "Tech: Astronomy", "+4 Influence. +3 Science and +2 Production to all unique improvements in this Settlement.", "On a Grassland tile."),
    Wonder("Exploration","Shwedagon Zedi Daw", 550, "None", "Tech: Education", "+4 Science. +2 Science on all Rural tiles in this Settlement that have at least 1 Happiness. +1 Wildcard Attribute Point.", "Adjacent to a Lake."),
    Wonder("Exploration","Tomb of Askia", 400, "Songhai", "Civic: Mercantilism", "+2 Gold. +2 Resource Capacity in this Settlement. +2 Gold and +2 Production in this Settlement for every Resource assigned to it.", "On a Desert tile."),
    Wonder("Exploration","White Tower", 400, "Norman", "Civic: Sovereignty Mastery", "+4 Happiness. +4 Happiness in this Settlement for every Tradition slotted in your Government.", "Adjacent to a City Hall."),
]
modernWonders = [
    Wonder("Modern","Battersea Power Station", 1000, "Great Britain", "Tech: Electricity Mastery", "+4 Production. When training a Naval Unit, receive an additional Naval Unit of the same type.", "Adjacent to water."),
    Wonder("Modern","Boudhanath", 1000, "Nepal", "Civic: Nationalism", "+4 Influence. Increase your Relationship with all other leaders by 20.", "On a Tropical tile and adjacent to a Mountain."),
    Wonder("Modern","Brandenburg Gate", 1400, "Prussia", "Civic: Militarism Mastery", "+6 Production. No Happiness penalty from War Weariness. +5 Happiness in conquered Settlements.", "Adjacent to a District."),
    Wonder("Modern","Chengde Mountain Resort", 1400, "Qing", "Civic: Hegemony Mastery", "+6 Gold. +5% Culture for each civilization you have a Trade Route with.", "Adjacent to a Mountain."),
    Wonder("Modern","Dogo Onsen", 1000, "Meiji Japan", "Civic: Social Question", "+4 Happiness. This Settlement gains 1 Population upon entering a celebration.", "Adjacent to a Coast tile."),
    Wonder("Modern","Doi Suthep", 1000, "Siam", "Civic: Political Theory", "+4 Influence. +5 Culture and +5 Gold for each City-State you are Suzerain of.", "On a Rough tile."),
    Wonder("Modern","Eiffel Tower", 1200, "French Empire", "Tech: Radio", "+5 Culture. +2 Culture and +2 Happiness on Quarters in this Settlement.", "Adjacent to a District."),
    Wonder("Modern","Hermitage", 1000, "Russia", "Civic: Modernization", "+4 Culture. +10% Culture in cities with a Great Work. Has 3 Great Work slots.", "On a Tundra tile."),
    Wonder("Modern","Manhattan Project", 1200, "None", "Ideology (Military Legacy Path)", "Grants a Nuclear Weapon and unlocks Operation Ivy project.", "No placement requirement."),
    Wonder("Modern","Muzibu Azaala Mpanga", 1000, "Buganda", "Civic: Natural History", "+4 Food. +2 Food on all Lake tiles. +2 Culture and +2 Happiness on all Lake tiles in this Settlement.", "Adjacent to a Lake."),
    Wonder("Modern","Oxford University", 1000, "None", "Civic: Academics", "+4 Science. Grants 2 free technologies. +1 Wildcard Attribute point.", "Adjacent to a District."),
    Wonder("Modern","Palacio de Bellas Artes", 1200, "Mexico", "Civic: Globalism Mastery", "+5 Culture. +2 Happiness on Great Works. +10% Happiness in this Settlement. Has 3 Artifact Slots.", "Adjacent to an Urban District."),
    Wonder("Modern","Red Fort", 1000, "Mughal", "Tech: Military Science", "+4 Gold. Acts as a Fortified District. +50 HP to this tile and all City Centers.", "Adjacent to a District."),
    Wonder("Modern","Statue of Liberty", 1400, "America", "Civic: Capitalism Mastery", "+6 Happiness. Spawns 4 Migrants.", "On a Coast tile adjacent to land."),
    Wonder("Modern","Taj Mahal", 1200, "None", "Civic: Nationalism Mastery", "+5 Gold. +50% Celebration duration. +1 Wildcard Attribute point.", "No placement requirement."),
]

allWonders = antiquityWonders + explorationWonders + modernWonders

allWonderIDs = [replaceSpaces(wonder.name) for wonder in allWonders]

wonderDict = {wonder: index for index, wonder in enumerate(allWonderIDs)}


class commandCorrection:
    def __init__(self, input, correction):
        self.input = input
        self.correction = correction

commandCorrections = [
    commandCorrection("mapinfo", "mapInfo"),
    commandCorrection("MapInfo", "mapInfo"),
    commandCorrection("maplist", "mapList"),
    commandCorrection("MapList", "mapList"),
    commandCorrection("wonderinfo", "wonderInfo"),
    commandCorrection("WonderInfo", "wonderInfo"),
    commandCorrection("wonderlist", "wonderList"),
    commandCorrection("WonderList", "wonderList"),
    commandCorrection("leaderlist", "leaderList"),
    commandCorrection("leaderinfo", "leaderInfo"),
    commandCorrection("LeaderInfo", "leaderInfo"),
    commandCorrection("civlist", "civList"),
    commandCorrection("CivList", "civList"),
    commandCorrection("reroll", "reRoll"),
    commandCorrection("ReRoll", "reRoll"),
    commandCorrection("revote", "reRoll"),
    commandCorrection("reVote", "reRoll"),
    commandCorrection("cancelvote", "cancelVote"),
    commandCorrection("CancelVote", "cancelVote"),
    commandCorrection("clearvote", "cancelVote"),
    commandCorrection("clearVote", "cancelVote"),
    commandCorrection("ClearVote", "cancelVote"),
    commandCorrection("bannedleaders", "bannedLeaders"),
    commandCorrection("bannedLeaders", "bannedLeaders"),
    commandCorrection("BannedLeaders", "bannedLeaders"),
    commandCorrection("permabanned", "bannedLeaders"),
    commandCorrection("permaBanned", "bannedLeaders"),
    commandCorrection("leaderBans", "bannedLeaders"),
    commandCorrection("leaderbans", "bannedLeaders"),
    commandCorrection("LeaderBans", "bannedLeaders"),
    commandCorrection("forcevote", "forceVote"),
    commandCorrection("ForceVote", "forceVote"),
    commandCorrection("forcevote", "forceVote"),
    commandCorrection("ForceVote", "forceVote"),
    commandCorrection("endVote", "forceVote"),
    commandCorrection("EndVote", "forceVote"),
    commandCorrection("endvote", "forceVote"),
    commandCorrection("forceEnd", "forceVote"),
    commandCorrection("ForceEnd", "forceVote"),
    commandCorrection("forceend", "forceVote")
    
]

correctedInputs = [command.input for command in commandCorrections]

hardBannedLeaderIDs = [2,11,13]
hardBannedCivIDs = [1]

lobbyHostingChannels = [1351993272096260127, 1362542399905202300]
voiceHostingChannels = {
    1351993272096260127: 1362542552376410252,
    1362542399905202300: 1351989426951295056
}
excludededUsers= { 
    #944016826751389717,
    #1351985363609976853
}

guildID = 1351787046720503808
civGuildID = 1362491827478986752
wonderGuildID = 1362574955375493291

OwnerID = 424980696264867880

doneVotingCheck = 2 # Num of seconds between checks

maxReactionsPerMessage = 20