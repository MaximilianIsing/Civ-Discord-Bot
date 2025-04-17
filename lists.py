antiquityCivs = [
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