from config import *
from util import *
from urllib.parse import quote, unquote
import random
import aiohttp
import asyncio
import sys, os
import time
import regex
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


script_dir = os.path.dirname(sys.argv[0])
cache_file_dir = script_dir+"/cache/cache.txt"


rev_sp_nl = regex.compile('(?r)[ \n]') # Search the string in reverse for either a space or newline.
rev_url_sp_nl = regex.compile('(?r)(%20|%0A)') # Search the string for a hex code that does not match a space or newline.
not_sp_nl = regex.compile('[^ \n]') # Search the string for a character that does not match a space or newline.
rev_not_sp_nl = regex.compile('(?r)[^ \n]') # Search the string in reverse for a character that does not match a space or newline.


nl_tab = regex.compile('[\n\t]') # Search the string in reverse for either a tab or newline.
not_sp_nl_tab = regex.compile('[^ \n\t]') # Search the string for a character that does not match a space, tab, or newline.
rev_not_sp_nl_tab = regex.compile('(?r)[^ \n\t]') # Search the string in reverse for a character that does not match a space, tab, or newline.


class gui():
    def __init__(self):
        
        # Unpack the language information from config.py.
        self.GOOGLE_LANGUAGE_DICT = GOOGLE_LANGUAGE_DICT
        self.GOOGLE_LANGUAGE_GROUPS = GOOGLE_LANGUAGE_GROUPS
        self.current_language_group = DEFAULT_GOOGLE_LANGUAGE_GROUP
        self.GOOGLE_LANGUAGE_NAMES = []
        self.GOOGLE_LANGUAGE_ALL = []
        self.GOOGLE_LANGUAGE_USE = []
        for name in self.GOOGLE_LANGUAGE_DICT:
            self.GOOGLE_LANGUAGE_NAMES += (name,)
            self.GOOGLE_LANGUAGE_ALL += (GOOGLE_LANGUAGE_DICT[name][0],)
            if self.GOOGLE_LANGUAGE_DICT[name][1] == True:
                self.GOOGLE_LANGUAGE_USE += (GOOGLE_LANGUAGE_DICT[name][0],)

        self.GOOGLE_LANGUAGE_GROUP_NAMES = [group for group in GOOGLE_LANGUAGE_GROUPS]

        # Information for translations generator gui.
        self.current_obfucations_value = DEFAULT_OBFUSCATIONS_VALUE
        self.current_multi_obfuscate_mode = DEFAULT_MULTI_OBFUSCATE_MODE


        self.version = "v0.4"

        # Window Setup
        self.window = tk.Tk()
        self.window.title(f"Python Text Obfuscator {self.version}")
        self.window['padx'] = 5
        self.window['pady'] = 5

        # Screen dimensions.
        window_width = 960
        window_height = 400

        x_pos = int((self.window.winfo_screenwidth()/2) - (window_width/2))
        y_pos = int((self.window.winfo_screenheight()/2) - (window_height/2))-200

        self.window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar)
        # File Menu
        filemenu.add_command(label="Open", command= lambda: self.open_file())
        filemenu.add_command(label="Save", command= lambda: self.save())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)



        # Control the obfuscator.
        cmd_frame = ttk.Frame(self.window)
        cmd_frame.grid(row=0, column=0)

        # Begins obfuscation.
        self.obfuscate_button = ttk.Button(cmd_frame, text="Obfuscate", command= lambda: self.begin_translation()) # self.start_translation_thread()
        self.obfuscate_button.grid(row=0, column=0)

        # Sets amount of translations.
        self.iterations_spinbox_value = tk.IntVar(self.window)
        self.iterations_spinbox_value.set(DEFAULT_ITERATIONS_VALUE)
        self.iterations_spinbox = ttk.Spinbox(cmd_frame, width=4, from_=0, to_=float('inf'), textvariable=self.iterations_spinbox_value)
        self.iterations_spinbox.grid(row=0, column=1)

        # Sets language to translate to/from.
        self.language_combobox = ttk.Combobox(cmd_frame, state="readonly", width=10)
        self.language_combobox.grid(row=0, column=2)
        self.language_combobox['values'] = self.GOOGLE_LANGUAGE_NAMES
        self.language_combobox.current(self.GOOGLE_LANGUAGE_NAMES.index(DEFAULT_LANGUAGE))

        # Choose between the modes to split the translation (as the maximum length per request is 5000 characters).
        self.split_mode_combobox = ttk.Combobox(cmd_frame, state="readonly", width=8)
        self.split_mode_combobox.grid(row=0, column=3)
        self.split_mode_combobox['values'] = ["Initial", "Continuous", "Newline"]
        self.split_mode_combobox.current(DEFAULT_SPLIT_MODE)

        # Select which languages will be randomly chosen from. Any language can be enabled or disabled but the obfuscation will fail if none are selected.
        self.language_selector_button = ttk.Button(cmd_frame, text="Language Selector", command= lambda: language_selector(self))
        self.language_selector_button.grid(row=0, column=4)

        self.translation_generator_button = ttk.Button(cmd_frame, text="Translation Generator", command= lambda: translation_generator(self))
        self.translation_generator_button.grid(row=0, column=5)

        # Clear the text from the output box as the user cannot modify it otherwise.
        self.output_text_clear_button = ttk.Button(cmd_frame, text="Clear Output", command= lambda: self.clear_output_text())
        self.output_text_clear_button.grid(row=0, column=6)

        # Text frame.
        text_frame = ttk.Frame(self.window)
        text_frame.grid(row=1, column=0, sticky=tk.NSEW)

        # Input area for the text.
        self.input_text = tk.Text(text_frame)
        self.input_text.grid(row=0, column=0, sticky=tk.NSEW)
        self.input_text.insert(1.0,random.choice(DEFAULT_INPUT_MESSAGES))

        # Result area for the obfuscated text.
        self.output_text = tk.Text(text_frame, state='disabled')
        self.output_text.grid(row=0, column=1, sticky=tk.NSEW)

        text_frame.grid_rowconfigure(0,weight=1)
        text_frame.grid_columnconfigure(0,weight=1)
        text_frame.grid_columnconfigure(1,weight=1)

        self.window.grid_rowconfigure(0,weight=0)
        self.window.grid_rowconfigure(1,weight=1)
        self.window.grid_columnconfigure(0,weight=1)
        
        # Automatically set languages to the chosen language group in config.py unless it is set to None.
        if self.current_language_group != None:
            language_selector(self).change_checkbuttons_group()
        self.window.mainloop()

    def open_file(self):
        file_dir = filedialog.askopenfilename(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                title="Please select a file:",
                                filetypes=[("Text Files", ".txt")])
        if file_dir != '':
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(file_dir[:file_dir.rindex("/")+1])
            cache_file.close()


            self.input_text.delete(1.0, 'end')
            self.input_text.insert(1.0,open(file_dir, 'r').read())

    def save(self):
        file_dir = filedialog.asksaveasfilename(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                title="Please name your file:",
                                filetypes=[("Text Files", ".txt")])
        if file_dir != '':
            cache_file = open(cache_file_dir, 'w')
            cache_file.write(file_dir[:file_dir.rindex("/")+1])
            cache_file.close()

            open(file_dir, 'w').write(self.output_text.get("1.0",'end-1c'))


    # Show progress of translate by number of translations completed divided by the number of translations to complete.
    # This gets less accurate as the amount of translations increase, but as long as the update is occurring to the window,
    # the user can know that the translation hasn't failed.
    def update_progress(self):
        if self.FULL >= self.counter > 0:
            self.window.title(f"Python Text Obfuscator {self.version} - {(self.counter*100//self.FULL)} % Complete - Time Passed: {time.time() - self.start_time:.2f} - Approx. Time Left: {((time.time() - self.start_time)/(self.counter/self.FULL))-(time.time() - self.start_time):.2f}")
        if self.translating == True:
            self.window.update()
            self.window.after(1000, self.update_progress)
        else:
            self.window.after(1000, self.window.title(f"Python Text Obfuscator {self.version}"))
            

    # Begins the obfuscation.
    def begin_translation(self):
        # Disable the following widgets so the user cannot use them until the obfuscation is complete.
        self.obfuscate_button['state'] = 'disabled'
        self.output_text_clear_button['state'] = 'disabled'
        self.input_text['state'] = 'disabled'

        # Set variables related to measuring translation progress.
        self.start_time = time.time()
        self.counter = 0
        self.FULL = 1
        self.translating = True
        self.update_progress()

        itr = self.iterations_spinbox_value.get() # Amount of translations.

        if self.split_mode_combobox.current() == 0: # Initial Mode

            result = asyncio.run( self.obfuscate_length_split(self.input_text.get("1.0",'end-1c'), itr, self.GOOGLE_LANGUAGE_ALL[self.language_combobox.current()]) ) # Obfuscate Asynchronously

        elif self.split_mode_combobox.current() == 1: # Continuous Mode

            self.FULL = itr+1 # FULL is not set in the obfuscate function itself, so this must be set.
            result = asyncio.run( self.obfuscate(None, self.input_text.get("1.0",'end-1c'), itr, self.GOOGLE_LANGUAGE_ALL[self.language_combobox.current()]) ) # Obfuscate Asynchronously

        else: # Newline Mode

            result = asyncio.run( self.obfuscate_newline_split(self.input_text.get("1.0",'end-1c'), itr, self.GOOGLE_LANGUAGE_ALL[self.language_combobox.current()]) ) # Obfuscate Asynchronously

        # While the output textbox is temporarily enabled, the result is inserted.
        self.output_text['state'] = 'normal'
        self.output_text.delete(1.0, 'end')
        self.output_text.insert(1.0, result)
        self.output_text['state'] = 'disabled'

        # Enable the widgets disabled during the obfuscation.
        self.input_text['state'] = 'normal'
        self.output_text_clear_button['state'] = 'normal'
        self.obfuscate_button['state'] = 'normal'

        # End progress estimation.
        self.translating = False

        print(time.time()-self.start_time)


    # ----------------------------------------------------------------------------------------------------------------------------------------
    # The text in this function is split by the length set in config.py (The default is 5000, which is also the maximum.)
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # During the splitting process, it looks for newlines or spaces to split at (preventing words from breaking),
    # and the split characters are stored in a list to add after the translation is complete, ensuring that
    # Google Translate will not mess up the formatting.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # Unfortunately this process will not preserve tabs, as tabs are deleted by Google Translate.
    # The solution to this requires a different approach which defeats the purpose of this mode
    # (which is to minimize the number of requests by maximizing the length).
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # Luckily newlines and spaces are handled properly, which should suit the needs of most translations, small and large.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # After it is split, it is passed into the obfuscate function, where each piece is translated asynchronously and with different languages.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    async def obfuscate_length_split(self, text, itr, lang='en'):
        # Area with only spaces, tabs, or newlines before text -> "pre_text".
        start_ind = not_sp_nl_tab.search(text).start()
        pre_text = text[:start_ind]
        
        # Area with only spaces, tabs, or newlines after text -> "post_text".
        end_ind = rev_not_sp_nl.search(text).end()
        post_text = text[end_ind:]

        # Text to translate.
        text = text[start_ind:end_ind]

        text = text.replace('/','⁄') # Replace slashes because Lingva Translate's API can't handle quoted slashes in queries. :/
        rind = ind = 0
        text_len = len(text)
        Text_List = [] # Text pieces stored here.
        Split_List = [] # Split chars stored here.
        while True:
            ind += DEFAULT_SPLIT_LENGTH
            if ind >= text_len:
                Text_List += (text[rind:ind],) # Text
                Split_List += ('',) # Last part is always empty.
                break
            real_length_dif = len(text[rind:ind].encode('utf-16'))//2 - DEFAULT_SPLIT_LENGTH  # Find the length of the text in utf-16 since Google Translate counts emoji's as multiple characters under this standard.
            if real_length_dif > 0:
                ind -= real_length_dif
            if text[ind] not in [" ","\n"]:
                if "\n" in text[rind:ind] or " " in text[rind:ind]:
                    ind = rev_sp_nl.search(text[:ind]).start() # Get to space or newline.
                    next_pos = ind+not_sp_nl.search(text[ind:]).start() # End of split.
                    ind = rev_not_sp_nl.search(text[:ind]).end() # Start of split.
                else: # If no spaces or newlines available, split at current position.
                    next_pos = ind
            else:
                next_pos = ind+not_sp_nl.search(text[ind:]).start() # End of split.
                ind = rev_not_sp_nl.search(text[:ind]).end() # Start of split.
            Text_List += (text[rind:ind],) # Text
            Split_List += (text[ind:next_pos],) # Split (newlines and spaces) or (empty).
            ind = rind = next_pos


        # Find the total amount of translations to complete the requested obfuscuation.
        self.FULL = len(Text_List)*(itr+1)


        print('starting obfuscation')
        async with aiohttp.ClientSession() as session: # Run asynchronous requests for each text piece in the list to speed up result retrieval.
            tasks = [asyncio.ensure_future(self.obfuscate(session, text_piece, itr, lang)) for text_piece in Text_List]

            Results = await asyncio.gather(*tasks)

        return pre_text+''.join([x for y in zip(Results, Split_List) for x in y]).replace('⁄','/')+post_text # Combine results with split chars.



    # ----------------------------------------------------------------------------------------------------------------------------------------
    # The text in this function is split by newline and tab characters.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # During the splitting process, it looks for newlines and tabs to split the text at, and any characters (newline, tabs, or spaces) within
    # the split regions are held in the split list to add after the translation, preventing formatting issues from Google Translate.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # This process preserves the formatting of texts with newlines and tabs, while also providing a greater variety in the translations,
    # as each individual line or tabsplit piece has a unique set of translations for the obfuscation.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # Unfortunately, the downside to this is that the number of requests will tend to be far higher than the split by length approach,
    # which leads to a longer translation time. Use this if you are willing to wait longer for a cleaner result with more variety.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    # After it is split, it is passed into the obfuscate function, where each piece is translated asynchronously and with different languages.
    # ----------------------------------------------------------------------------------------------------------------------------------------
    async def obfuscate_newline_split(self, text, itr, lang='en'):
        # Area with only spaces, tabs, or newlines before text -> "pre_text".
        start_ind = not_sp_nl_tab.search(text).start()
        pre_text = text[:start_ind]
        
        # Area with only spaces, tabs, or newlines after text -> "post_text".
        end_ind = rev_not_sp_nl_tab.search(text).end()
        post_text = text[end_ind:]

        # Text to translate.
        text = text[start_ind:end_ind]

        text = text.replace('\r','').replace('/','⁄') # Replace slashes because Lingva Translate's API can't handle quoted slashes in queries. :/

        Text_List = [] # Text pieces stored here.
        Split_List = [] # Split chars stored here.
        rind = ind = 0

        while True:
            if not ("\n" in text[ind:] or "\t" in text[ind:]):
                Text_List += (text[rind:],) # Text
                Split_List += ('',) # Last part is always empty.
                break
            ind = nl_tab.search(text[ind:]).start()+ind # Start of split.
            Text_List += (text[rind:ind],) # Text
            next_pos = not_sp_nl_tab.search(text[ind:]) # End of split.
            if next_pos == None:
                next_pos = len(text) # End of text.
                Split_List += (text[ind:next_pos],) # Split
                break
            next_pos = next_pos.start()+ind # End of split.
            Split_List += (text[ind:next_pos],) # Split.
            rind = ind = next_pos # Reset indicies.

        if Text_List[0] == '': # Delete first string from translation if empty.
            Text_List = Text_List[1:]
        
        # Find the total amount of translations to complete the requested obfuscuation.
        self.FULL = len(Text_List)*(itr+1)

        print('starting obfuscation')
        async with aiohttp.ClientSession() as session: # Run asynchronous requests for each text piece in the list to speed up result retrieval.
            tasks = [asyncio.ensure_future(self.obfuscate(session, text_piece, itr, lang)) for text_piece in Text_List]

            Results = await asyncio.gather(*tasks)

        return pre_text+''.join([x for y in zip(Results, Split_List) for x in y]).replace('⁄','/')+post_text # Run asynchronous requests for each text piece in the list to speed up result retrieval.


    async def get_translation(self, session, url): # Gets translation for obfuscate function.
        while True:
            try:
                async with session.get(url) as response:
                    try:
                        return (await response.json())['translation'].replace('/','⁄')
                    except Exception as e:
                        url += '%2E'
                        print(url, e)
                        time.sleep(1)
            except (aiohttp.ServerDisconnectedError, aiohttp.ClientResponseError,aiohttp.ClientConnectorError) as e:
                print(url, e)
                await asyncio.sleep(1)


    async def obfuscate(self, session, text, itr, lang='en'):
        # Area with only spaces, tabs, or newlines before text -> "pre_text".
        start_ind = not_sp_nl_tab.search(text).start()
        pre_text = text[:start_ind]
        
        # Area with only spaces, tabs, or newlines after text -> "post_text".
        end_ind = rev_not_sp_nl.search(text).end()
        post_text = text[end_ind:]

        # Text to translate.
        text = text[start_ind:end_ind]


        if "/" in text:
            text = text.replace('\r','').replace('/','⁄') # Replace slashes because Lingva Translate's API can't handle quoted slashes in queries. :/
        Languages_List = [lang] # List for languages to translate text through.
        last_ind = 0
        for i in range(itr): # Adds languages to list.
            if Languages_List[i-1] in self.GOOGLE_LANGUAGE_USE:
                last_ind = self.GOOGLE_LANGUAGE_USE.index(Languages_List[i-1]) # Last language index.
            Languages_List += (random.choice(self.GOOGLE_LANGUAGE_USE[:last_ind]+self.GOOGLE_LANGUAGE_USE[last_ind+1:]),) # Randomly choose language that wasn't chosen last.
        Languages_List += (lang,)
        last_lang = Languages_List[0] # First language.

        for cur_lang in Languages_List[1:]: # Iterate through language list, translating between each.
            if text[0] == ".": # Lingva has a problem with queries starting in periods. :(
                text = " " + text
            url = f"https://{random.choice(LINGVA_WEBSITES)}/api/v1/{last_lang}/{cur_lang}/{quote(text)}"

            if len(text) > DEFAULT_SPLIT_LENGTH or len(url) > 16331 or session == None: # Split text if it's too big.

                url_base_ind = url.rindex("/",0,52)+1

                url_base = url[:url_base_ind]
                url_query = url[url_base_ind:]
                query_length = len(url_query)
                max_length = 16331 - len(url_base)

                rind = ind = 0
                Translate_List = []
                Split_List = []
                while True:
                    ind += max_length

                    # Find the length of the text in utf-16 since Google Translate counts emoji's as multiple characters under this standard.
                    while len(unquote(url_query[rind:ind]).encode('utf-16'))//2 > DEFAULT_SPLIT_LENGTH:
                        ind = ind-((ind-rind)//2)
                    if ind >= query_length:
                        Translate_List += (url_base+url_query[rind:ind],)
                        Split_List += ('',)
                        break
                    if url_query[ind] != "%":
                        ind -= 1
                        if url_query[ind] != "%":
                            ind -= 1
                    if url_query[ind-3:ind] not in ("%20","%0A"):
                        if "%20" in url_query[rind:ind] or "%0A" in url_query[rind:ind]:
                            ind = rev_url_sp_nl.search(url_query[rind:ind]).end()+rind # Start of split.
                            next_ind = ind # End of split.
                            while url_query[next_ind:next_ind+3] in ("%20","%0A"):
                                next_ind += 3
                            while url_query[ind-3:ind] in ("%20","%0A"):
                                ind -= 3
                        else:
                            next_ind = ind
                    else:
                        next_ind = ind
                        while url_query[next_ind:next_ind+3] in ("%20","%0A"):
                            next_ind += 3
                        while url_query[ind-3:ind] in ("%20","%0A"):
                            ind -= 3
                    Translate_List += (url_base+url_query[rind:ind],)
                    Split_List += (unquote(url_query[ind:next_ind]),)
                    ind = rind = next_ind

                async with aiohttp.ClientSession() as sub_session: # Run asynchronous requests for each text piece in the list to speed up result retrieval.
                    tasks = [asyncio.ensure_future(self.get_translation(sub_session, sub_url)) for sub_url in Translate_List]

                    Results = await asyncio.gather(*tasks)

                    text = ''.join([x for y in zip(Results, Split_List) for x in y]) # Result.

            else: # Text is translated normally.
                last_lang = cur_lang
                while True:
                    try:
                        async with session.get(url) as response:
                            try:
                                text = (await response.json())['translation'].replace('/','⁄')
                                break
                            except Exception as e:
                                url += '%2E'
                                print(url, e)
                                time.sleep(1)
                    except (aiohttp.ServerDisconnectedError, aiohttp.ClientResponseError, aiohttp.ClientConnectorError) as e:
                        print(url, e)
                        await asyncio.sleep(1)

            last_lang = cur_lang
            self.counter += 1
            self.window.update() # Update tkinter window to allow progress display in title.

        return pre_text+text+post_text


    def clear_output_text(self): # Clear text in output box.
        self.output_text['state'] = 'normal'
        self.output_text.delete(1.0, 'end')
        self.output_text['state'] = 'disabled'


class language_selector(): # Choose which languages to use while translating.
    def __init__(self, parent):
        self.parent = parent

        # Window Setup
        self.window = tk.Toplevel(self.parent.window)

        # Screen dimensions.
        window_width = 940
        window_height = 300

        x_pos = int((self.window.winfo_screenwidth()/2) - (window_width/2))
        y_pos = int((self.window.winfo_screenheight()/2) - (window_height/2))+200

        self.window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        self.parent.language_selector_button.configure(command= lambda: self.window.focus_force()) # Prevent spawning multiple windows; instead brings window to focus.

        
        if not self.parent.window.attributes('-fullscreen'): # Allow resize if the parent is in fullscreen only.
            self.window.resizable(False, False)
            
        self.window.title('Language Selector')
        
        # Contains Language Group
        self.cmd_frame = tk.Frame(self.window)

        # Contains Languages
        self.checkbox_frame = tk.Frame(self.window)

        self.Checkbuttons = [] # Checkbuttons for Languages.
        self.Labels = [] # Display Languages Names.

        self.group_combobox = ttk.Combobox(self.cmd_frame, state="readonly")
        self.group_combobox.grid(row=0, column=0)
        self.group_combobox['values'] = self.parent.GOOGLE_LANGUAGE_GROUP_NAMES
        if self.parent.current_language_group in self.parent.GOOGLE_LANGUAGE_GROUP_NAMES:
            self.group_combobox.current(self.parent.GOOGLE_LANGUAGE_GROUP_NAMES.index(self.parent.current_language_group))
        self.group_combobox.bind("<<ComboboxSelected>>", lambda _: self.change_checkbuttons_group())
        
        for i in range(len(self.parent.GOOGLE_LANGUAGE_ALL)): # Create and place widgets.
            cur_checkbutton = ttk.Checkbutton(self.checkbox_frame, command=lambda: self.update_languages())
            cur_checkbutton.grid(row=i % 13, column=2*(i//13 % 9))
            cur_checkbutton.state(['!alternate'])
            cur_label = ttk.Label(self.checkbox_frame, text=self.parent.GOOGLE_LANGUAGE_NAMES[i])
            cur_label.grid(row=i % 13, column=2*(i//13 % 9)+1, sticky=tk.W)
            self.Checkbuttons += (cur_checkbutton,)
            self.Labels += (cur_label,)

        self.cmd_frame.grid(row=0, column=0)
        self.checkbox_frame.grid(row=1, column=0)

        self.update_checkbuttons()
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

    def update_checkbuttons(self): # Set checkbuttons to correct value.
        for i in range(len(self.parent.GOOGLE_LANGUAGE_ALL)):
            if self.parent.GOOGLE_LANGUAGE_ALL[i] in self.parent.GOOGLE_LANGUAGE_USE:
                ck_state = 'selected'
            else:
                ck_state = '!selected'
            self.Checkbuttons[i].state([ck_state])

    def change_checkbuttons_group(self): # Change which checkbuttons are active based on what group is selected in the combobox.
        self.parent.current_language_group = self.group_combobox.get()
        for i in range(len(self.parent.GOOGLE_LANGUAGE_ALL)):
            if self.parent.GOOGLE_LANGUAGE_ALL[i] in self.parent.GOOGLE_LANGUAGE_GROUPS[self.parent.current_language_group]:
                ck_state = 'selected'
            else:
                ck_state = '!selected'
            self.Checkbuttons[i].state([ck_state])
        self.update_languages()

    def update_languages(self): # Change languages in GOOGLE_LANGUAGE_USE list.
        self.parent.GOOGLE_LANGUAGE_USE = []
        for i in range(len(self.parent.GOOGLE_LANGUAGE_ALL)):
            if 'selected' in self.Checkbuttons[i].state():
                self.parent.GOOGLE_LANGUAGE_USE += (self.parent.GOOGLE_LANGUAGE_ALL[i],)

    def on_close(self): # Return parent spawn button's original function.
        self.window.destroy()
        self.parent.language_selector_button.configure(command= lambda: language_selector(self.parent))
        self.parent.window.deiconify()

class translation_generator():
    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(self.parent.window)
        self.window.title("Generator")

        # Screen dimensions.
        window_width = 150
        window_height = 85

        x_pos = int((self.window.winfo_screenwidth()/2) - (window_width/2))
        y_pos = int((self.window.winfo_screenheight()/2) - (window_height/2))

        self.window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Prevent spawning multiple windows; instead brings window to focus.
        self.parent.translation_generator_button.configure(command= lambda: self.window.focus_force())

        if not self.parent.window.attributes('-fullscreen'): # Allow resize if the parent is in fullscreen only.
            self.window.resizable(False, False)

        # Begins obfuscation.
        self.multi_obfuscate_button = ttk.Button(self.window, text="Multi-Obfuscate", command= lambda: self.multi_obfuscation()) # self.start_translation_thread()
        self.multi_obfuscate_button.grid(row=0, column=0, columnspan=2)


        # Choose between the modes to iterate the obfuscations; (Repeat translations of the original each time, or continue translating each result.)
        self.multi_obfuscation_mode_combobox = ttk.Combobox(self.window, state="readonly", width=8)
        self.multi_obfuscation_mode_combobox.grid(row=1, column=0, columnspan=2)
        self.multi_obfuscation_mode_combobox['values'] = ["Repeat","Continue"]
        self.multi_obfuscation_mode_combobox.current(self.parent.current_multi_obfuscate_mode)

        self.translations_label = ttk.Label(self.window, text="Obfuscations")
        self.translations_label.grid(row=2, column=0)

        # Sets amount of obfuscations.
        self.obfuscation_iterations_spinbox_value = tk.IntVar(self.window)
        self.obfuscation_iterations_spinbox_value.set(self.parent.current_obfucations_value)
        self.obfuscation_iterations_spinbox = ttk.Spinbox(self.window, width=4, from_=0, to_=float('inf'), textvariable=self.obfuscation_iterations_spinbox_value)
        self.obfuscation_iterations_spinbox.grid(row=2, column=1)


        self.window.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

    def multi_obfuscation(self): # Creates a csv file containing the original and each translations in columns.
        file_dir = filedialog.asksaveasfilename(parent=self.window,
                                initialdir=get_initial_directory(cache_file_dir),
                                title="Please name your file:",
                                filetypes=[("Comma Seperated Values", ".csv")])
        
        if file_dir != '':
            # Disable during obfuscations.
            self.multi_obfuscate_button['state'] = 'disabled'


            cache_file = open(cache_file_dir, 'w')
            cache_file.write(file_dir[:file_dir.rindex("/")+1])
            cache_file.close()

            original_string = self.parent.input_text.get("1.0",'end-1c') # Original Text

            tr_df = pd.DataFrame({"Original": original_string.split('\n')}) # Original text added in new dataframe.

            # Amount of times to obfuscate the text -> Amount of translation results -> Amount of columns written
            obfuscation_itr = self.obfuscation_iterations_spinbox_value.get()

            current_itr = itr = self.parent.iterations_spinbox_value.get() # Amount of times text is translated.

            multi_obfuscation_mode = self.multi_obfuscation_mode_combobox.current()

            # If set to continue, the amount of times the text has been translated will change per column, as the text from the last obfuscation is translated next.
            if multi_obfuscation_mode:
                current_itr = 0

            for i in range(1, obfuscation_itr+1):
                
                tr_df.to_csv(file_dir, encoding='utf-16', sep="\t", index=False, header=True) # Dataframe written to file.
                self.window.title(f"{str(i)}/{str(obfuscation_itr)}")
                self.parent.begin_translation()
                result = self.parent.output_text.get("1.0",'end-1c')

                # If set to continue, the text from the last obfuscation is put in the input textbox for translation,
                # and the amount of times the text has been translated is updated.
                if multi_obfuscation_mode:
                    current_itr += itr
                    self.parent.input_text.delete(1.0, 'end')
                    self.parent.input_text.insert(1.0, result)

                tr_df[f"Translation {str(i)}: (x{current_itr})"] = result.split('\n') # Result is added to data frame.

            tr_df.to_csv(file_dir, encoding='utf-16', sep="\t", index=False, header=True) # Dataframe written to file. Complete.
            self.multi_obfuscate_button['state'] = 'normal' # Re-enable.
            self.window.title("Generator")
        

    def on_close(self): # Return parent spawn button's original function and get information about current gui values for later.
        self.parent.current_multi_obfuscate_mode = self.multi_obfuscation_mode_combobox.current()
        self.parent.current_obfucations_value = self.obfuscation_iterations_spinbox_value.get()
        self.window.destroy()
        self.parent.translation_generator_button.configure(command= lambda: translation_generator(self.parent))
        self.parent.window.deiconify()

if __name__ == '__main__':       
    gui()
