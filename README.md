# PythonTextObfuscator
Takes a string and puts it through different languages in Google Translate a requested amount of times, returning nonsense.
![Example](https://user-images.githubusercontent.com/77307334/152076751-3c058117-dff9-4a58-a6de-e62f0e61e380.png)
![Example](https://user-images.githubusercontent.com/77307334/152076769-42a3fcc1-9b1c-45d6-83fd-1a58e361a132.png)
![Example](https://user-images.githubusercontent.com/77307334/152076775-79ba754d-a2d1-458e-9770-d17c279c3c55.png)


# Requirements:

    python3.10
    
    aiohttp
    
    regex
    
    pandas
    
# Usage:

    python3.10 "Python Text Obfuscator Main.py"
    
# Changes in v0.4:

### Translations are retrieved from a front-end to Google Translate called Lingva, which removes the issue with being blocked for doing too many requests.

### Translations are done in an asynchronous function using aiohttp instead of a process pool, which is optimal for large bulk translations.

### Removed selenium obfuscation.

# Additions:

### Importing and saving text files.
    
### Language Selector to activate or deactivate any individual language.
### Language setting for the result.
    
### Three different split methods:
#### Initial
    Text is split by length before being passed into the obfuscate function.
    Faster as less requests are made.
    Different languages for each piece.
    Tabs not preserved.
#### Continuous
    Text is split by length inside the obfuscate function.
    Faster as less requests are made.
    Same languages for each piece.
    Tabs not preserved.
#### Newline
    Text is split by newlines and tabs.
    Slower as more requests are made.
    Every single line is translated with different languages.
    Tabs preserved.
### Translation Generator which creates a .csv file containing multiple translations of the same text:
    Repeat mode obfuscates the original text each time, adding the result in each new column.
    Continue mode obfuscates the results from each subsequent obfuscation, adding the result in each new column.
