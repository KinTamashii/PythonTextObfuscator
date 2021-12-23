# PythonTextObfuscator
Takes a string and puts it through different languages in Google Translate a requested amount of times, returning nonsense.

Requirments:
  python3
  For the Selenium Obfuscator:
    -Selenium
    -Firefox
    -Geckodriver
    
In the Selenium Obfuscator:
  -The major benefit is that you can translate excel documents, the downside is that after 10 or so document translations, Google blocks your ip for a while.
  -Translation is generally slower and more limited using selenium as a browser tab is being used to scrape the data. Also beware of RAM usage.
  -May no longer be supported in the future due to its drawbacks.

In the Urllib Obfuscator:
  -Translation is generally faster and uses very little resources as only html is downloaded through a request. Multiprocessing also allows simultanious requests and can be used to the full extent without worrying about RAM usage.
  —Split by length is faster and uses less requests (better for longer texts)
  —Split by newline is slower and uses more requests but adds much more translation variety.
  -Reminder: Since google has a url request limit, you'll need to switch VPN locations when the request limit is hit.
    ——Don't worry too much though, as it takes quite a bit of requests to get to that point, and the block only lasts for around an hour.
