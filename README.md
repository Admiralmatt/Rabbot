Rabbot
======

Rabbot is a twitch chat bot

* Rabbot keeps track of any stats (like **!death**) that the streamer wants kept track of.

If you want to contact me about Rabbot (bug reports, feedback, or if you want it in your channel) send me an email <admiralmatt107@gmail.com>.


##Game
* **!game** Post the game currently being played.
 
   **Mod-only commands**
* **!game override (NAME)** Force Rabbot to use (NAME) as the current game.
* **!game override off** Disable override, go back to getting current game from Twitch stream settings.
* **!game refresh** Force a refresh of the current Twitch game. (normally this is updated at most once every 15 minutes)

##Stats
* **!(STAT)** Add 1 to (STAT) counter.
* **!(STAT) remove** Removes 1 from (STAT) counter.
* **!(STAT) count** Posts the current (STAT) count for current game. Auto called after stat update.

   **Mod-only command**
* **!(STAT) add #** Adds # amount to (STAT)
* **!(STAT) new** Creates a new (STAT) counter if it has not been used in any game so far.
* **!(STAT) set #** Sets (STAT) to #

##Misc
* **!help** Posts a link to this page.
* **!(Depends)** Posts a static response to a command. Or random response from list.
All commands and responces are listed in data file.
Each command can have different access levels.
