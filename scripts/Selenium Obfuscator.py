#!/usr/bin/env python
# coding: utf-8
from tkinter import *
from tkinter import Tk, Canvas, Frame, BOTH
from tkinter import filedialog as fd
import time
import random
import sys, os
import pandas as pd
from urllib.parse import quote
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidArgumentException, InvalidSessionIdException
options = Options() # Creates options for webdriver(s).
options.add_argument("-private")
#options.add_argument("--headless") # Sets webdrivers to headless mode when these options are applied.
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument('--disable-application-cache')
#options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
options.headless = False # Sets webdrivers to headless mode when these options are applied.



Drivers = {}

# Language Codes & Names
Languages = ['af','sq','am','ar','hy','az','eu','be','bn','bs','bg','ca','ceb','ny','zh-CN','zh-TW','co','hr','cs','da','nl','en','eo','et','tl','fi','fr','fy','gl','ka','de','el','gu','ht','ha','haw','iw','hi','hmn','hu','is','ig','id','ga','it','ja','jw','kn','kk','km','ko','rw','ku','ky','lo','la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne','no','or','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn','sd','si','sk','sl','so','es','su','sw','sv','tg','ta','tt','te','th','tr','tk','uk','ur','ug','uz','vi','cy','xh','yi','yo','zu','auto']
Language_Names = ['Afrikaans','Albanian','Amharic','Arabic','Armenian','Azeerbaijani','Basque','Belarusian','Bengali','Bosnian','Bulgarian','Catalan','Cebuano','Chichewa','Chinese (Simplified)','Chinese (Traditional)','Corsican','Croatian','Czech','Danish','Dutch','English','Esperanto','Estonian','Filipino','Finnish','French','Frisian','Galician','Georgian','German','Greek','Gujarati','Haitian Creole','Hausa','Hawaiian','Hebrew','Hindi','Hmong','Hungarian','Icelandic','Igbo','Indonesian','Irish','Italian','Japanese','Javanese','Kannada','Kazakh','Khmer','Kinyarwanda','Korean','Kurdish','Kyrgyz','Lao','Latin','Latvian','Lithuanian','Luxembourgish','Macedonian','Malagasy','Malay','Malayalam','Maltese','Maori','Marathi','Mongolian','Burmese','Nepali','Norwegian','Odia (Oriya)','Pashto','Persian','Polish','Portuguese','Punjabi','Romanian','Russian','Samoan','Scots Gaelic','Serbian','Sesotho','Shona','Sindhi','Sinhala','Slovak','Slovenian','Somali','Spanish','Sundanese','Swahili','Swedish','Tajik','Tamil','Tatar','Telugu','Thai','Turkish','Turkmen','Ukrainian','Urdu','Uyghur','Uzbek','Vietnamese','Welsh','Xhosa','Yiddish','Yoruba','Zulu','Any']


# Hex list for urls.
hex_list = ['%0','%1','%2','%3','%4','%5','%6','%7','%8','%9','%A','%B','%C','%D','%E','%F']

# Print Messages
message_base = '\nTranslation {Piece %d} %d of %d: %s to %s (%f seconds)\n\n'

result_piece_message_base = '\nTranslation Result {Piece %d}: from %s (%f seconds)\n\n'

result_message_base = '\n\nTranslation Result: (%f seconds)'

# Creates tkinter window.
master = Tk()
master.geometry("1440x900")
master.title('Selenium Obfuscator (v0.3.1c)')


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

'''Takes a string of text and puts it into google translate, translating between an input language code,
and an output language code, using a webdriver.
'''
def GoogleTranslate(text_input, driver, output_language_code="auto", input_language_code="auto"):
    while True:
        try:
            driver.get("https://translate.google.com/?sl="+input_language_code+"&tl="+output_language_code+"&text="+quote(text_input[:2048]))
            break
        except Exception as e:
            print(e)
            time.sleep(5)
    try: # Agrees to Google Data Policy if applicable.
        driver.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span").click()
    except NoSuchElementException:
        pass
    translation = None
    while translation == None:
        try:
            print('Translating...')
            translation = WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[5]/div/div[1]').text)
        except TimeoutException:
            print("TimeoutException has occured. Retrying...")
            driver.refresh()
            print('Browser refreshed!')
            pass
    return translation.replace("\n "," ").replace(" ...","...").replace("  "," ")




# Translates an excel document given an input/output language and directory.
def GoogleExcelTranslate(input_language_code, output_language_code, excel_input_directory, excel_output_directory, trans_driver, message, start_time_message):
    # Generates Google Translate Link for webdriver.
    trans_driver.get("https://translate.google.com/?sl="+input_language_code+"&tl="+output_language_code+"&op=docs")
    while True:
        try:
            try: # Agrees to Google Data Policy if applicable.
                trans_driver.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span").click()
            except NoSuchElementException:
                pass
            try:
                upload_element = WebDriverWait(trans_driver, 10).until(lambda trans_driver: trans_driver.find_element(By.ID, 'i34')) # Looks for the File Browser Element.
                upload_element.send_keys(excel_input_directory) # Uploads the excel document from the given directory.
                # Begins translation.
                trans_driver.find_element(By.XPATH, "/html/body/c-wiz/div/div[2]/c-wiz/div[3]/c-wiz/div[2]/c-wiz/div/div/form/div[2]/div[2]/div/button/span").click()
            except:
                pass
            TranslatedExcelTable = WebDriverWait(trans_driver, 10).until(lambda trans_driver: trans_driver.find_element(By.XPATH, "/html/body/table")) # Waits until table appears.
            OriginalTable = pd.read_excel(excel_input_directory, header=None) # Uses the original excel data retrieved as a basis for its translation status.
            print(OriginalTable)
            TranslatedTable = pd.read_html(TranslatedExcelTable.get_attribute('outerHTML'), header=None)[0]
            loop_time = time.time()
            while TranslatedTable.shape[0] < OriginalTable.shape[0]:
                TranslatedExcelTable = trans_driver.find_element(By.XPATH, "/html/body/table")
                TranslatedTable = pd.read_html(TranslatedExcelTable.get_attribute('outerHTML'), header=None)[0]
                print(OriginalTable.shape[0])
                print(TranslatedTable.shape[0])
            counter = OriginalTable.shape[0]*OriginalTable.shape[1]
            while counter > OriginalTable.shape[0]*OriginalTable.shape[1]//20: # Updates the translated table html data until the translation is complete.
                counter = 0
                TranslatedExcelTable = trans_driver.find_element(By.XPATH, "/html/body/table")
                TranslatedTable = pd.read_html(TranslatedExcelTable.get_attribute('outerHTML'), header=None)[0]
                for i in range(OriginalTable.shape[0]):
                    for j in range(OriginalTable.shape[1]):
                        OriginalString = OriginalTable.iloc[i][j]
                        NewString = TranslatedTable.iloc[i][j]
                        print(OriginalString)
                        print(NewString)
                        if OriginalString == NewString and OriginalString != 'nan':
                            counter += 1
                print(counter)
            print(message + "%s seconds." % (time.time() - start_time_message)) # Prints time that has passed since translations have begun.
            print(pd.read_html(TranslatedExcelTable.get_attribute('outerHTML')))
            TranslatedExcelDataFrame = pd.read_html(TranslatedExcelTable.get_attribute('outerHTML'))[0]
            TranslatedExcelDataFrame.to_excel(excel_output_directory,index=False,header=False) # Creates translated document.
            break
        except InvalidSessionIdException:
                break
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            try:
                err_405 = trans_driver.find_element(By.XPATH, '/html/body/p[1]').text
                print(err_405)
                trans_driver.quit()
                break
            except:
                pass
            print(e)


# Sets relevent variables for entry widgets.
translation_amount_entry_var=IntVar
excel_pathway_entry_string_var=StringVar


# Creates entry widgets for values in the obfuscate function.
excel_pathway_entry = Entry(master, textvariable=excel_pathway_entry_string_var, width=70)
original_text_text = Text(master, borderwidth=0, height=60, width=101)
original_text_text.insert(1.0,"When you enter some words here, and press that obfuscate button, it will become more screwed up the higher the number of translations.")
translation_amount_entry = Entry(master, textvariable=translation_amount_entry_var, width=10)
translation_amount_entry.insert(0,"5")


def Obfuscate(translation_tuple):
    translating_text_piece, translation_amount, start_time, newlines_count, order_num = translation_tuple # Tuple is split into its components.
    while True:
        try:
            Drivers['driver_{}'.format(order_num)] = webdriver.Firefox(options=options)
            break
        except InvalidArgumentException:
            break
        except Exception as e:
            print(e)
    Random_List = [109] + random.sample(range(0,109), translation_amount) # Random integers are created to implement random values from Language lists.

    # Translations are done between current languages to new language on each iteration amount of times requested (translation_amount).
    for i in range(translation_amount):
        message = message_base % (order_num, i+1, translation_amount, Language_Names[Random_List[i]], Language_Names[Random_List[i+1]], time.time() - start_time)
        translating_text_piece = GoogleTranslate(translating_text_piece, Drivers['driver_{}'.format(order_num)], Languages[Random_List[i+1]], Languages[Random_List[i]])
        print(message+translating_text_piece) # A Message indicates progress and shows the order number of the piece of the text.

    translating_text_piece = GoogleTranslate(translating_text_piece, Drivers['driver_{}'.format(order_num)], 'en', Languages[Random_List[-1]]) # Text is translated back into english.
    result_piece_message = result_piece_message_base % (order_num, Language_Names[Random_List[-1]], time.time() - start_time)
    result = translating_text_piece
    Drivers['driver_{}'.format(order_num)].quit()
    print(result_piece_message+result) # Another Message indicates that the last translation for this piece of text has been completed.
    return result, newlines_count, order_num


# Puts a string through google translate multiple times and returns a hilarious result.
def Obfuscator(original_text,translation_amount):
    Translating_Text_List = basic_text_split(original_text,1792) # Original Text is split into smaller pieces that can fit into the Google Translate url.

    start_time = time.time() # Timer is started.
    
    Translation_Tuple_List = [] # Tuples are created to store strings in list to translates, as well as the amount of translations, start time, and order number.
    for i in range(len(Translating_Text_List)):
        Translation_Tuple_List += ((Translating_Text_List[i],translation_amount,start_time,Translating_Text_List[i].count("\n"),i),)

    results = ThreadPool(10).imap_unordered(Obfuscate, Translation_Tuple_List) # Each piece of text is obfuscated seperately without order to increase speed.

    Result_List = [] # List is created to format results.

    for result, newlines_count, order_num in results:
        Result_List += ((result,newlines_count,str(order_num).zfill(len(str(len(Translating_Text_List))))),)

    Final_Tuple_List = sorted(Result_List, key=lambda x: x[-1]) # Result list is ordered with the order numbers.
    
    Final_Results = [] # Final Results List is created to remove the order part of each tuple.
    for i in Final_Tuple_List: # Order number is removed since the list is already ordered.
        target_string_count = i[1] # Original amount of linebreaks.
        dif = target_string_count - i[0].count('\n') # Difference between translation and original amount of linebreaks.
        String_Lines = i[0].split('\n')
        fixed_result = i[0] # As long as there is no change in the amount of linebreaks, the result remains unchanged.
        Revised_String_Lines = []

        if dif > 0: # Adds the difference of linebreaks to the result.
            dif_counter = 0
            line_counter = 0
            max = len(String_Lines)
            while dif_counter < dif:
                String_Lines_Words = String_Lines[line_counter].split(' ')
                Revised_String_Lines += [" ".join(String_Lines_Words[:len(String_Lines_Words)//2])]+[" ".join(String_Lines_Words[len(String_Lines_Words)//2:])]
                dif_counter += 1
                line_counter += 1
                if dif_counter == dif:
                    Revised_String_Lines += String_Lines[line_counter:]
                elif line_counter == max:
                    max = len(Revised_String_Lines)
                    String_Lines = Revised_String_Lines
                    Revised_String_Lines = []
                    line_counter = 0
            fixed_result = "\n".join(Revised_String_Lines)
        if dif < 0: # Removes the difference of linebreaks from the result.
            Revised_String_Lines += [" ".join(String_Lines[:-dif+1])] + String_Lines[-dif+1:]
            fixed_result = "\n".join(Revised_String_Lines)
        
        Final_Results += (fixed_result,)

    return " ".join(Final_Results), start_time


# Puts an Excel Spreadsheet through google translate multiple times and returns a hilarious result.
def excel_obfuscator(translation_amount):
    ExcelDriver = webdriver.Firefox(options=options) # Creates webdriver for translation.
    excel_file_path = excel_pathway_entry.get()
    start_time = time.time() # Starts timer for translations.
    current_language = ["auto"] # List is created to keep track of what to enter for input and output languages, begining with auto.
    current_path = [excel_file_path] # List is created to keep track of what to enter for input and output pathways, begining with the original directory.
    directory_component = excel_file_path.split(".")
    file_name = excel_file_path.split("/")[-1].split(".")[0]
    obfuscation_directory = directory_component[0] + " Obfuscation/"
    if not os.path.exists(obfuscation_directory):
        os.makedirs(obfuscation_directory)
    for i in range(translation_amount):
        random_language = random.randrange(0,108) # Random integer is chosen from 0 to 108.
        current_language.append(Languages[random_language]) # Integer is used to choose a language from the Languages list.
        padding_amount = "{:0"+str(len(str(translation_amount)))+"d}"
        loop_integer = padding_amount.format(i+1)
        new_directory = obfuscation_directory + file_name + " Translation_" + loop_integer + " (" + current_language[i] + " to " + current_language[i+1] + ").xlsx"
        current_path.append(new_directory) # New pathway is put on the end of the list.
        print(new_directory)
        # Translates between two languages, using the previous pathway as the document to translate, and creating a new document in the new pathway.
        message = "Translation " + str(i) + " of " + str(translation_amount) + " [" + current_language[i+1] + "]: "
        try:
            while True:
                try:
                    GoogleExcelTranslate(current_language[i], current_language[i+1], current_path[i], current_path[i+1], ExcelDriver, message, start_time)
                    break
                except InvalidSessionIdException:
                    print('Browser Crashed')
                    ExcelDriver = webdriver.Firefox(options=options)
                except TimeoutException:
                    isrunning = 0
                    print("A TimeoutException has occured during translation. You may wish to connect to a different location using a VPN to reset Google's limit.")
                    ExcelDriver.close()
                    break
            print(current_language[i+1]+": %s seconds." % (time.time() - start_time)) # Prints time that has passed since translations have begun.
        except FileNotFoundError or InvalidArgumentException:
            pass
    en_directory = obfuscation_directory + file_name + " Translation_Result" + " (from " + current_language[-1] + ").xlsx"
    print(en_directory)
    message = "Translation " + str(translation_amount) + " of " + str(translation_amount) + " [en]: "
    # Takes the final document from previous translation and returns it in English in the final directory.
    try:
        while True:
            try:
                GoogleExcelTranslate(current_language[-1], 'en', current_path[-1], en_directory, ExcelDriver, message, start_time)
                break
            except InvalidSessionIdException:
                print('Browser Crashed')
                ExcelDriver = webdriver.Firefox(options=options)
            except TimeoutException:
                isrunning = 0
                print("A TimeoutException has occured during translation. You may wish to connect to a different location using a VPN to reset Google's limit.")
                ExcelDriver.close()
                break
        print("en: %s seconds." % (time.time() - start_time)) # Prints time that has passed since translations have begun to last translation.
    except FileNotFoundError or InvalidArgumentException:
        print("Obfuscation failed.")
    ExcelDriver.close()


# Creates result box for final translation.
translation_text_text = Text(master, borderwidth=0, width=101, height=60)
translation_text_text.grid(row=5, column=1)

def translate_function_update():
    translation_text_text.delete(1.0, END) # Deletes text in the text box.
    # Returns a string put through google translate an amount of times and sets it the final_result variable.
    final_result, start_time = Obfuscator(original_text_text.get("1.0","end-1c"),int(translation_amount_entry.get()))
    finish_time = time.time()-start_time
    result_message = result_message_base % finish_time
    print(final_result+result_message)
    translation_text_text.insert(1.0, final_result) # Adds final translation into the result box.

# Selects an Excel Spreadsheet.
def select_excel_file():
    excelfilepath = fd.askopenfilename(title='Open an Excel Document', initialdir='/', filetypes=(('Excel Files', '*.xlsx'),('All files', '*.*')))
    excel_pathway_entry.delete(0,END)
    excel_pathway_entry.insert(0,excelfilepath)

#Creates button to obfuscate text from the Original string and the Amount of Translations integer.
ObfuscateButton = Button(master, text="Obfuscate", width=20, command=lambda: translate_function_update())

#Creates button to select an excel file.
ExcelFileButton = Button(master, text='Excel Pathway', command=select_excel_file)

#Creates button to obfuscate an excel document from the Amount of Translations integer.
ExcelObfuscateButton = Button(master, text="Excel Spreadsheet Obfuscate", width=20, command=lambda: excel_obfuscator(int(translation_amount_entry.get())))

# Sets the positions of the widgets on the canvas.
Label(master, text="Amount of Translations").grid(row=0,columnspan=2)
ExcelFileButton.grid(row=0,column=1)
translation_amount_entry.grid(row=1,columnspan=2)
excel_pathway_entry.grid(row=1,column=1, sticky=E)
ObfuscateButton.grid(row=2,columnspan=2)
ExcelObfuscateButton.grid(row=2,column=1)
Label(master, text="Original Text").grid(row=3,column=0)
Label(master, text="Translated Text").grid(row=3,column=1)
original_text_text.grid(row=5, column=0)

master.mainloop()