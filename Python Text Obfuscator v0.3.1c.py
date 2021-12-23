#!/usr/bin/env python
# coding: utf-8
from tkinter import *
from tkinter import Tk
import sys, os
import subprocess

script_dir = os.path.dirname(sys.argv[0])
selenium_dir=os.path.join(script_dir, 'scripts/Selenium Obfuscator.py')
urllib_dir=os.path.join(script_dir, 'scripts/Urllib Obfuscator.py')

master = Tk()
master.title('Python Text Obfuscator v0.3.1c')
master.geometry("288x60")

def Selenium_Script_Open():
    subprocess.call(['python3', selenium_dir])
def Urllib_Script_Open():
    subprocess.call(['python3', urllib_dir])

Selenium_Script=Button(master, height=3, width=12, text="Selenium Obfuscator\n(w/ Excel Obfuscator)", command=lambda: Selenium_Script_Open())
Urllib_Script=Button(master, height=3, width=12, text="Urllib Obfuscator\n(Faster)", command=lambda: Urllib_Script_Open())
Selenium_Script.grid(row=0, column=0)
Urllib_Script.grid(row=0, column=1)

master.mainloop()
