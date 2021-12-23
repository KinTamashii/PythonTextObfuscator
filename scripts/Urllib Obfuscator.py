#!/usr/bin/env python
from tkinter import *
from tkinter import Tk, Canvas, Frame, BOTH
import random
from multiprocessing.pool import ThreadPool
from urllib.request import Request, urlopen
import urllib.parse
from urllib.error import HTTPError
import html
import time
import sys, os





# Creates tkinter window.
master = Tk()
master.geometry("1440x900")
master.title('Python Text Obfuscator v0.3.1c (urllib)')


# Sets relevent variables for entry widgets.
translation_amount_entry_var=IntVar

# Creates entry widgets for values in the obfuscate function.
original_text_text = Text(master, borderwidth=0, height=60, width=101)
original_text_text.insert(1.0,"When you enter some words here, and press that obfuscate button, it will become more screwed up the higher the number of translations.")
translation_amount_entry = Entry(master, textvariable=translation_amount_entry_var, width=10)
translation_amount_entry.insert(0,"5")

# Creates result box for final translation.
translation_text_text = Text(master, borderwidth=0, width=101, height=60)
translation_text_text.grid(row=5, column=1)


ref = [
    'https://duckduckgo.com/',
    'https://www.google.com/',
    'https://www.bing.com/',
    'https://www.yandex.ru/',
    'https://search.yahoo.com/',
    'https://www.facebook.com/',
    'https://twitter.com/',
    'https://www.youtube.com/'
]
# Header agent is needed to successfully get the translation from Google Translate.
script_dir = os.path.dirname(sys.argv[0])
user_agents_dir = script_dir+'/useragents.txt'

f = open(user_agents_dir)

agents = f.read().split('\n')

proxy_counter = 0


# Global Constants
ProxyMode = False
# Language Codes & Names
Languages = ['af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca','ceb','ny','zh-CN','zh-TW','co','hr','cs','da','nl','en','eo','et','tl','fi','fr','fy','gl','ka','de','el','gu','ht','ha','haw','iw','hi','hmn','hu','is','ig','id','ga','it','ja','jw','kn','kk','km','ko','rw','ku','ky','lo','la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne','no','or','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn','sd','si','sk','sl','so','es','su','sw','sv','tg','ta','tt','te','th','tr','tk','uk','ur','ug','uz','vi','cy','xh','yi','yo','zu','auto']
Language_Names = ['Afrikaans','Albanian','Amharic','Arabic','Armenian','Azeerbaijani','Basque','Belarusian','Bengali','Bosnian','Bulgarian','Catalan','Cebuano','Chichewa','Chinese (Simplified)','Chinese (Traditional)','Corsican','Croatian','Czech','Danish','Dutch','English','Esperanto','Estonian','Filipino','Finnish','French','Frisian','Galician','Georgian','German','Greek','Gujarati','Haitian Creole','Hausa','Hawaiian','Hebrew','Hindi','Hmong','Hungarian','Icelandic','Igbo','Indonesian','Irish','Italian','Japanese','Javanese','Kannada','Kazakh','Khmer','Kinyarwanda','Korean','Kurdish','Kyrgyz','Lao','Latin','Latvian','Lithuanian','Luxembourgish','Macedonian','Malagasy','Malay','Malayalam','Maltese','Maori','Marathi','Mongolian','Burmese','Nepali','Norwegian','Odia (Oriya)','Pashto','Persian','Polish','Portuguese','Punjabi','Romanian','Russian','Samoan','Scots Gaelic','Serbian','Sesotho','Shona','Sindhi','Sinhala','Slovak','Slovenian','Somali','Spanish','Sundanese','Swahili','Swedish','Tajik','Tamil','Tatar','Telugu','Thai','Turkish','Turkmen','Ukrainian','Urdu','Uyghur','Uzbek','Vietnamese','Welsh','Xhosa','Yiddish','Yoruba','Zulu','Any']


# Hex list for urls.
hex_list = ['%0','%1','%2','%3','%4','%5','%6','%7','%8','%9','%A','%B','%C','%D','%E','%F']

#Option menu for "fix" translation mode selection.
Translation_Modes = [False,True]
current_mode = BooleanVar(master)
current_mode.set(Translation_Modes[0]) # Default Language

translation_mode_menu = OptionMenu(master, current_mode, *Translation_Modes)


# Print Messages
message_base = '\nTranslation {Piece %d} %d of %d: %s to %s (%f seconds)\n\n'

result_piece_message_base = '\nTranslation Result {Piece %d}: from %s (%f seconds)\n\n'

result_message_base = '\n\nTranslation Result: (%f seconds)'




def basic_text_split(string, max_characters): # Splits text into segments by max number of characters, without cutting words in half.
    line_list = [] # Creates a list for the words on individual lines.
    lines_result = [] # Creates a list for all the lines.
    split_string = string.split(" ")
    character_counter = 0 # Keeps track of the total length of concatenated words.
    for i in split_string: # Word in list is added to line if the resulting total number of characters is less than the max specified.
        character_counter += len(i)+1
        if character_counter <= max_characters:
            line_list += (i,)
        else:
            lines_result += (" ".join(line_list),)
            character_counter = len(i)
            line_list = [i]
    lines_result += (" ".join(line_list),)
    while '' in lines_result: # Removes empty pieces of list.
        lines_result.remove('')
    return lines_result

def GoogleTranslate(text_input, output_language_code="auto", input_language_code="auto"): # Translates string from one language to another (auto is default).
    # Link cannot be longer than 2048 characters or else an error will occur, and thus the text must be cut off in the case it becomes longer.
    global proxy_counter
    global ProxyMode
    link = ("http://translate.google.co.in/m?tl=%s&sl=%s&q=%s" % (output_language_code, input_language_code, urllib.parse.quote(text_input[:2048])))[:16411]
    if link[-1] == "%":
        link = link[:-1]
    if link[-2:] in hex_list:
        link = link[:-2]
    request = Request(link, headers={
                'User-Agent': random.choice(agents),
                'Referer': random.choice(ref),
                'Accept-Encoding': 'gzip;q=0,deflate;q=0',
                'Connection': 'Keep-Alive',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Cache-directive': 'no-cache',
                'Pragma': 'no-cache',
}) # Request is made to Google Translate using the Header.
    while True:
        try:
            raw_data = urlopen(request).read().decode("utf-8") # Raw data is converted to text.
            break
        except HTTPError as err: # Fallback if Google blocks the requests.
            if err.code == 400:
                print(link)
                link = link[:-1]
                if link[-1] == "%":
                    link = link[:-1]
                if link[-2:] in hex_list:
                    link = link[:-2]
            else:
                print(str(err)+"\nYou have been rate limited. Please switch locations on your VPN.")
                time.sleep(10)
            request = Request(link, headers={
                'User-Agent': random.choice(agents),
                'Referer': random.choice(ref),
                'Accept-Encoding': 'gzip;q=0,deflate;q=0',
                'Connection': 'Keep-Alive',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Cache-directive': 'no-cache',
                'Pragma': 'no-cache',
            })
    result = html.unescape(raw_data[raw_data.find('<div class="result-container">')+30:raw_data.find('</div><div class="links-container">')]) # Result is found.
    return result


def Obfuscate(translation_tuple):
    translating_text_piece, translation_amount, start_time, newlines_count, newline_pos, order_num = translation_tuple # Tuple is split into its components.

    Random_List = [109] + random.sample(range(0,109), translation_amount) # Random integers are created to implement random values from Language lists.

    # Translations are done between current languages to new language on each iteration amount of times requested (translation_amount).
    for i in range(translation_amount):
        message = message_base % (order_num, i+1, translation_amount, Language_Names[Random_List[i]], Language_Names[Random_List[i+1]], time.time() - start_time)
        translating_text_piece = GoogleTranslate(translating_text_piece, Languages[Random_List[i+1]], Languages[Random_List[i]])
        print(message+translating_text_piece) # A Message indicates progress and shows the order number of the piece of the text.

    translating_text_piece = GoogleTranslate(translating_text_piece, 'en') # Text is translated back into english.
    result_piece_message = result_piece_message_base % (order_num, Language_Names[Random_List[-1]], time.time() - start_time)
    result = translating_text_piece
    print(result_piece_message+result) # Another Message indicates that the last translation for this piece of text has been completed.
    return result, newlines_count, newline_pos, order_num

def Obfuscator(original_text,translation_amount,newline_mode):
    text_2 = original_text.replace('\r','')
    print(newline_mode)
    if newline_mode == False:
        Translating_Text_List = basic_text_split(text_2,1792) # Original Text is split into smaller pieces that can fit into the Google Translate url.
    if newline_mode == True:
        Translating_Text_List = text_2.replace('\n',u'\n\uffff').split(u'\uffff')
    print(Translating_Text_List)
    start_time = time.time() # Timer is started.

    Translation_Tuple_List = [] # Tuples are created to store strings in list to translates, as well as the amount of translations, start time, and order number.
    for i in range(len(Translating_Text_List)):
        Translating_Text_Part = Translating_Text_List[i]
        status = 0
        while Translating_Text_Part[-1] == '\n':
            Translating_Text_Part = Translating_Text_Part[:-1]
            status += 1
        Translation_Tuple_List += ((Translating_Text_Part,translation_amount,start_time,status,Translating_Text_Part.count('\n'),i),)

    results = ThreadPool(50).imap_unordered(Obfuscate, Translation_Tuple_List) # Each piece of text is obfuscated seperately without order to increase speed.

    Result_List = [] # List is created to format results.

    for result, newlines_status, newline_pos, order_num in results:
        Result_List += ((result,newlines_status,newline_pos,str(order_num).zfill(len(str(len(Translating_Text_List))))),)

    Final_Tuple_List = sorted(Result_List, key=lambda x: x[-1]) # Result list is ordered with the order numbers.
    
    Final_Results = [] # Final Results List is created to remove the order part of each tuple.
    for i in Final_Tuple_List: # Order number is removed since the list is already ordered.
        final_msg_part = i[0]
        Final_Results += (final_msg_part+('\n'*(i[1]+i[2]-final_msg_part.count('\n'))),)
    result = " ".join(Final_Results).replace('\n ','\n')
    
    Original_List = text_2.split('\n')
    Result_List = result.split('\n')
    Unfinished_List = []
    Unfinished_Num = []
    for r in range(len(Original_List)):
        if Original_List[r] != '' and Original_List[r] != ' ' and Result_List[r] == '':
            Unfinished_List += (Original_List[r],)
            Unfinished_Num += (r,)
    if len(Unfinished_List) > 0:
        unfinished = '\n'.join(Unfinished_List)
        unfinished_result, start_time = Obfuscator(unfinished,translation_amount,newline_mode)
        Unfinished_Result_List = unfinished_result.split('\n')
        for n in range(len(Unfinished_Result_List)):
            print(Unfinished_List[n],Unfinished_Num[n])
            Result_List = Result_List[:Unfinished_Num[n]] + [Unfinished_Result_List[n]] + Result_List[Unfinished_Num[n]+1:]
        result = '\n'.join(Result_List)

    return result, start_time




def translate_function_update():
    translation_text_text.delete(1.0, END) # Deletes text in the text box.
    # Returns a string put through google translate an amount of times and sets it the final_result variable.
    final_result, start_time = Obfuscator(original_text_text.get("1.0","end-1c"),int(translation_amount_entry.get()),current_mode.get())
    finish_time = time.time()-start_time
    result_message = result_message_base % finish_time
    print(final_result+result_message)
    translation_text_text.insert(1.0, final_result) # Adds final translation into the result box.


#Creates button to obfuscate text from the Original string and the Amount of Translations integer.
ObfuscateButton = Button(master, text="Obfuscate", width=20, command=lambda: translate_function_update())

# Sets the positions of the widgets on the canvas.
Label(master, text="Amount of Translations").grid(row=0,columnspan=2)
translation_amount_entry.grid(row=1,columnspan=2)
Label(master, text="0 = Split By Length\tTranslation Mode\t1 = Split By Newline").grid(row=0,column=1)
translation_mode_menu.grid(row=1,column=1)
Label(master, text="Split By Length is faster and uses less requests. Optimal for long strings.\nSplit By Newline is slower and uses more requests, but produces more variety.").grid(row=2,column=1)
ObfuscateButton.grid(row=2,columnspan=2)
Label(master, text="Original Text").grid(row=3,column=0)
Label(master, text="Translated Text").grid(row=3,column=1)
original_text_text.grid(row=5, column=0)

master.mainloop()