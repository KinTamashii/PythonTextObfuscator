# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- DEFAULT INPUT MESSAGES ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------- Text that is inserted into the input box by default. --------------------------------- #
# ------------------------------------- One message is choosen at random from the list. ----------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_INPUT_MESSAGES = [
"When you enter some words here, and press that obfuscate button, it will become more screwed up the higher the number of translations.",
"Well, at least I did not go down without explaining myself first.",
"I came.",
"It’s time to dump her and move on.",
"Yeah AI that sounds pretty shit to me, Looks like BT ain't for me either.",
"Yeah, tell me the story of them big puppies.",
"Imagine for a second you were transposed into the karma driven world of Earl.",
"It looks like a sack that encloses with a drawstring.",
"Open your mouth!"
]


# ------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LINGVA WEBSITES ---------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------- Lingva is the frontend to Google Translate that makes rapid ------------------------------- #
# ----------------------- scraping of the platform possible without worrying about request limits. ------------------------ #
# ------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------- With each translation, the website is chosen randomly. -------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------- I have ommited the websites with the Hetzner host as they block excessive requests. ----------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
LINGVA_WEBSITES = ["lingva.ml", "translate.alefvanoon.xyz", "translate.igna.rocks"] # limited -> "translate.datatunnel.xyz" "lingva.pussthecat.org"


# ------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------- DEFAULT AMOUNT OF ITERATIONS --------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------- Amount of times the text is translated set by default. -------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_ITERATIONS_VALUE = 10


# ------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------- DEFAULT AMOUNT OF OBFUSCATIONS -------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------- Amount of times the text is obfuscated in the ------------------------------------ #
# ------------------------------------------ translations generator set by default. --------------------------------------- #
DEFAULT_OBFUSCATIONS_VALUE = 10


# ------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- DEFAULT LANGUAGE --------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------- Language the text is translated from and back into by default. ---------------------------- #
# -------------------------------- The language must exist within the languages dictionary. ------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_LANGUAGE = "English"


# ------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- DEFAULT SPLIT MODE -------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------- Split mode that the text is set to by default. ------------------------------------ #
# ----------------------------- The split mode dictates how text is split between the requests. --------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------- 0 & 1 are faster as less requests are made. -------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ---------------- 0 == Initial; Text is split by length before being passed into the obfuscate funtion. ------------------ #
# ------------------------------------------- Different languages for each piece. ----------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------ 1 == Continuous; Text is split by length inside the obfuscate function. ------------------------ #
# ---------------------------------------------- Same languages for each piece. ------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# --------------- 2 == Newline; Text is split by newlines and tabs. This is slower as more requests are made, ------------- #
# ---------------- but allows for more variety, as every single line is translated with different languages. -------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_SPLIT_MODE = 0


# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- DEFAULT OBFUSCATION MODE ---------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------- Obfuscation mode that the translations generator is set to by default. ------------------------ #
# ---- 0 == Repeat; Original text is obfuscated each time, so each result is made from the same amount of translations. --- #
# --- 1 == Continue; Text is translated continously, with each result used as the text for each subsequent obfuscation. --- #
# --------------- This means that the number of translations for each result is higher with each iteration. --------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_MULTI_OBFUSCATE_MODE = 0


# ------------------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------- DEFAULT SPLIT LENGTH ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------- Amount of characters to split the input text into. -------------------------------- #
# ------------------------------------ This only applies if the split mode is "0" (Length). ------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------ This should not exceed 5000. ------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_SPLIT_LENGTH = 5000


# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------- GOOGLE LANGUAGE GROUPS ------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------ Language groups that can be chosen in the language selector. ----------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------- When adding a language group it must contain only codes -------------------------------- #
# ----------------------------------- that exist within the Google Language Dictionary. ----------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
GOOGLE_LANGUAGE_GROUPS = {
'ALL': ['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'ny', 'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'rw', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne', 'no', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu'],
'Afro-Asiatic': ['am', 'ar', 'ha', 'iw', 'mt', 'so'],
'Austronesian': ['ceb', 'tl', 'haw', 'id', 'jw', 'mg', 'ms', 'mi', 'sm', 'su'],
'Baltic / Uralic': ['et', 'fi', 'hu', 'lv', 'lt'],
'Celtic / Paleo-Balkan': ['sq', 'hy', 'el', 'ga', 'gd', 'cy'],
'Dravidian / Austroasiatic': ['kn', 'km', 'ml', 'ta', 'te', 'vi'],
'Germanic': ['af', 'da', 'nl', 'en', 'fy', 'de', 'is', 'lb', 'no', 'sv', 'yi'],
'Indo-Aryan': ['bn', 'gu', 'hi', 'mr', 'ne', 'or', 'pa', 'sd', 'si', 'ur'],
'Iranian': ['ku', 'ps', 'fa', 'tg'],
'Isolated Languages': ['eu', 'eo', 'ka', 'ht', 'hmn', 'ja', 'ko', 'mn'],
'Italic': ['ca', 'co', 'fr', 'gl', 'it', 'la', 'pt', 'ro', 'es'],
'Niger–Congo': ['ny', 'ig', 'rw', 'st', 'sn', 'sw', 'xh', 'yo', 'zu'],
'Sino-Tibetan / Kra–Dai': ['my', 'zh-CN', 'zh-TW', 'lo', 'th'],
'Slavic': ['be', 'bs', 'bg', 'hr', 'cs', 'mk', 'pl', 'ru', 'sr', 'sk', 'sl', 'uk'],
'Turkic': ['az', 'kk', 'ky', 'tt', 'tr', 'tk', 'ug', 'uz']
}


# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------ DEFAULT GOOGLE LANGUAGE GROUP IN-USE ----------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------ Language groups that can be chosen in the language selector. ----------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------- The Language group must either exist in the  ------------------------------------- #
# ---------------------------------- Google Language Groups Dictionary or be set to None.  -------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ----------------------- If set to a valid group, the app will open the language selector at start ----------------------- #
# ------------------------------- and the languages in the selected group will be set active, ----------------------------- #
# ----------------------------------- while the remaining ones will be set to inactive. ----------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------- If set to None, the language selector will not open at start, and the languages will not be overwritten. -------- #
# ------------------------------------------------------------------------------------------------------------------------- #
DEFAULT_GOOGLE_LANGUAGE_GROUP = 'ALL'


# ------------------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------- ALL GOOGLE LANGUAGES ------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------- Remove a language name/code pair to completely delete it. ------------------------------- #
# ------------------------------------------ Do not add language codes that do -------------------------------------------- #
# ------------------------------------------- not exist within the translator. -------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Language names correspond to each code. --------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------ The bool determines if the language is activated by default ------------------------------ #
# ---------------------- however this is overwritten if a language group is selected other than None. --------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
GOOGLE_LANGUAGE_DICT = {
'Afrikaans': ['af', True],
'Albanian': ['sq', True],
'Amharic': ['am', True],
'Arabic': ['ar', True],
'Armenian': ['hy', True],
'Azerbaijani': ['az', True],
'Basque': ['eu', True],
'Belarusian': ['be', True],
'Bengali': ['bn', True],
'Bosnian': ['bs', True],
'Bulgarian': ['bg', True],
'Catalan': ['ca', True],
'Cebuano': ['ceb', True],
'Chichewa': ['ny', True],
'Chinese (Simplified)': ['zh-CN', True],
'Chinese (Traditional)': ['zh-TW', True],
'Corsican': ['co', True],
'Croatian': ['hr', True],
'Czech': ['cs', True],
'Danish': ['da', True],
'Dutch': ['nl', True],
'English': ['en', True],
'Esperanto': ['eo', True],
'Estonian': ['et', True],
'Filipino': ['tl', True],
'Finnish': ['fi', True],
'French': ['fr', True],
'Frisian': ['fy', True],
'Galician': ['gl', True],
'Georgian': ['ka', True],
'German': ['de', True],
'Greek': ['el', True],
'Gujarati': ['gu', True],
'Haitian Creole': ['ht', True],
'Hausa': ['ha', True],
'Hawaiian': ['haw', True],
'Hebrew': ['iw', True],
'Hindi': ['hi', True],
'Hmong': ['hmn', True],
'Hungarian': ['hu', True],
'Icelandic': ['is', True],
'Igbo': ['ig', True],
'Indonesian': ['id', True],
'Irish': ['ga', True],
'Italian': ['it', True],
'Japanese': ['ja', True],
'Javanese': ['jw', True],
'Kannada': ['kn', True],
'Kazakh': ['kk', True],
'Khmer': ['km', True],
'Kinyarwanda': ['rw', True],
'Korean': ['ko', True],
'Kurdish': ['ku', True],
'Kyrgyz': ['ky', True],
'Lao': ['lo', True],
'Latin': ['la', True],
'Latvian': ['lv', True],
'Lithuanian': ['lt', True],
'Luxembourgish': ['lb', True],
'Macedonian': ['mk', True],
'Malagasy': ['mg', True],
'Malay': ['ms', True],
'Malayalam': ['ml', True],
'Maltese': ['mt', True],
'Maori': ['mi', True],
'Marathi': ['mr', True],
'Mongolian': ['mn', True],
'Burmese': ['my', True],
'Nepali': ['ne', True],
'Norwegian': ['no', True],
'Odia (Oriya)': ['or', True],
'Pashto': ['ps', True],
'Persian': ['fa', True],
'Polish': ['pl', True],
'Portuguese': ['pt', True],
'Punjabi': ['pa', True],
'Romanian': ['ro', True],
'Russian': ['ru', True],
'Samoan': ['sm', True],
'Scots Gaelic': ['gd', True],
'Serbian': ['sr', True],
'Sesotho': ['st', True],
'Shona': ['sn', True],
'Sindhi': ['sd', True],
'Sinhala': ['si', True],
'Slovak': ['sk', True],
'Slovenian': ['sl', True],
'Somali': ['so', True],
'Spanish': ['es', True],
'Sundanese': ['su', True],
'Swahili': ['sw', True],
'Swedish': ['sv', True],
'Tajik': ['tg', True],
'Tamil': ['ta', True],
'Tatar': ['tt', True],
'Telugu': ['te', True],
'Thai': ['th', True],
'Turkish': ['tr', True],
'Turkmen': ['tk', True],
'Ukrainian': ['uk', True],
'Urdu': ['ur', True],
'Uyghur': ['ug', True],
'Uzbek': ['uz', True],
'Vietnamese': ['vi', True],
'Welsh': ['cy', True],
'Xhosa': ['xh', True],
'Yiddish': ['yi', True],
'Yoruba': ['yo', True],
'Zulu': ['zu', True]
}