import json

# Default filenames

WEAR_VALUES_FILE = "wear_values.wv"
BLACKLIST_FILE = "blacklist.bl"
SEARCHES_FILE = "searches.src"
LAST_THREAD_FILE = "reddit.lst"
LOG_FILE = "temp.tmp"
VAULT_FOLDER = "vault\\"
VAULT_EXTENSION = ".vlt"
INVENTORY_FOLDER = "inventories\\"
INVENTORY_EXTENSION = ".inv"
SEPARATOR = "|"

# Links

STEAM_ID = "76561198064554984"
API_KEY = "47FCBA5720449997E87F6CC0C988ADFE"
API_URL_HEAD = "http://API.steampowered.com/IEconItems_730/GetPlayerItems/v0001/?key="
API_URL_TAIL = "&SteamID="
PUBLIC_URL_HEAD = "http://steamcommunity.com/profiles/"
PUBLIC_URL_TAIL = "/inventory/json/730/2/?l=english"
FRIENDS_URL_HEAD = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?relationship=friend&key="
FRIENDS_URL_TAIL = "&steamid="
LOUNGE_THREAD_HEAD = "http://csgolounge.com/trade?t="
REDDIT_THREAD_HEAD = "https://pay.reddit.com/r/GlobalOffensiveTrade/new/?before=t3_"
REDDIT_HOT_PAGE = "https://pay.reddit.com/r/GlobalOffensiveTrade/"
LOUNGE_CONNECTER = "&p="

# Constants

WEAR_PREFIX = "Exterior: "
WEAR_TO_INT = {"Factory New": 1, "Minimal Wear": 2, "Field-Tested": 3, "Well-Worn": 4, "Battle-Scarred": 5}
INT_TO_WEAR = {1: "Factory New", 2: "Minimal Wear", 3: "Field-Tested", 4: "Well-Worn", 5: "Battle-Scarred"}
CONDITION_DETAILS = {"Exterior: Factory New": ["FN", [0.00, 0.07]], "Exterior: Minimal Wear": ["MW", [0.07, 0.15]], "Exterior: Field-Tested": ["FT", [0.15, 0.37]], "Exterior: Well-Worn": ["WW", [0.37, 0.44]], "Exterior: Battle-Scarred": ["BS", [0.44, 1.00]]}
REDDIT_HOT_THREADS = 25
REDDIT_OFFSET_1 = 1
REDDIT_OFFSET_2 = 7
REDDIT_TIMEOUT = 2
LOUNGE_TIMEOUT = 10
REDDIT_RETRY_LIMIT = 8
STEAM_RETRY_LIMIT = 30
LOUNGE_RETRY_LIMIT = 5
WEAPON_ATTRIBUTES = 6
WEAPON_ID_ID = 6
WEAPON_WEAR_ID = 1
HIGHLIGHT_FACTOR = 0.0005
REDDIT_THREAD_QUEUE_DEFAULT_COUNT = 55
REDDIT_TRICK_1 = 6
REDDIT_ID_QUEUE = "\"http://steamcommunity.com/profiles/"
REDDIT_ID_END = "\""
REDDIT_TIME_QUEUE = "timestamp\">"
REDDIT_TIME_END = " hour"
REDDIT_THREAD_QUEUE = "comments/"
REDDIT_THREAD_LENGTH = 6
LOUNGE_THREAD_ID_QUEUE = "addBookmark('"
LOUNGE_THREAD_ID_END = "'"
LOUNGE_ID_QUEUE = "profile?id="
LOUNGE_ID_END = "\""
REDDIT_HEADER = {"User-Agent": "pc:csgotrade:v4 by /u/noidgoten"}
REDDIT_ERROR = "developers"
STEAM_API_ERROR_1 = "Permission denied"
STEAM_API_ERROR_2 = "This profile is private."
STEAM_API_ERROR_3 = "{\n\n}"
STEAM_PUBLIC_ERROR = "null"
LOUNGE_ERROR = "Looks like there's no site that you´re looking for."
LOUNGE_COOKIE = {"PHPSESSID": "ihdc5kcjo544mhhsh3km1m6bb3	", "_utma": "210545287.1216707982.1422875650.1422879043.1423483897.3", "_utmb": "210545287.3.10.1423483897", "_utmc": "210545287", "token": "f621e3560759cde8d396ec2a919e10e4", "id": "76561198177102546", "tkz": "fe40485607ba9ec2b63bda9109532598", "_utmt": "1", "_utmz": "210545287.1422875650.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)", "_ga": "GA1.2.1216707982.1422875650"}
FUNCTION_NAME = "choice_"
GET_LIMIT_WEARS_ERROR = "Error in get_limit_wears"
STEAM_INTERNAL_ERROR = "Internal Server Error"

# Processed constants

MINMAX_WEAR = json.loads(open(WEAR_VALUES_FILE, "r").read())


# Messages

PRESS_MSG = "Press "
INVALID_MSG = "Invalid choice. Try again."
INPUT_PROMPT_MSG = "Your choice: "
OPTION_MSG = ["for a specific profile.", "to search an item on the Lounge + Reddit.", "to iterate all friends of input SteamID64 (including the root).", "to update the database.", "to iterate a lot of friends."]
SPLITTER = "*" * 256
REDDIT_ERROR_MSG = "Could not get reddit page."
WEIRD_REDDIT_PAGE_MSG = "The loaded page might not be what you wanted."
LOAD_SUCCESS = " has been successfully loaded."
TIMEOUT_OF_DEATH = "Reddit threw another timeout at you."
REDDIT_NULL_TEMPLATE = "WRONG"
OLD_FILE = "File too old."
LOUNGE_ERROR_MSG = "You fucked up."
SEARCHES_HEADER = "Preset searches: "
LOUNGE_MINER_MSG = "Paste the Lounge search link for your desired item."
LOUNGE_MINER_ITEM_CHOICE = "What item are you searching for?"
LOUNGE_MINER_START = "Lounge mining started for "
LOUNGE_PAGE_HEAD = "We're on page "
LOUNGE_PAGE_TAIL = " of the Lounge search results. Mining..."
LOUNGE_PAGE_SUCCESSFUL_HEAD = "Page "
LOUNGE_PAGE_SUCCESSFUL_TAIL = " successful."
LOUNGE_DONE_HEAD = "Lounge search results had "
LOUNGE_DONE_TAIL = " page(s), of which all have been mined.\n"
STEAM_PRIVATE_PROFILE = "Private profile. Permission denied."
STEAM_PERMISSION_DENIED = "{\n	\"result\": {\n		\"status\": 15,\n		\"statusDetail\": \"Permission denied\"\n	}\n}"
API_UNSUCCESSFUL = "API contents could not be loaded"
STEAM_UNKNOWN = "Problem unknown. You might wanna note it."
NO_BACKUP = "No backup could be found."
INVENTORY_ERROR = "No way to access the inventory at this point in time."

