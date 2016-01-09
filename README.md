Rabbot
======

Rabbot is a twitch chat bot

* Rabbot keeps track of any stats (like **!death**) that the streamer wants kept track of.
* Rabbot can also create a poll to ask the chat a question and have them vote on the answer.
* When set as a chat moderator it can perform auto spam detection.

If you want to contact me about Rabbot (bug reports, feedback, or if you want it in your channel) send me an email at <matthewreed@mail.adelphi.edu>.


##Game
* **!game** Post the game currently being played.
* **!game good/bad** Vote whether you believe this game is entertaining to watch on-stream.
					 Voting a second time replaces your existing vote.
 
   **Mod-only commands**
* **!game override (NAME)** Force Rabbot to use (NAME) as the current game.
* **!game override off** Disable override, go back to getting current game from Twitch stream settings.
* **!game refresh** Force a refresh of the current Twitch game. (Normally this is updated at most once every 15 minutes)

##Stats
* **!(STAT)** Add 1 to (STAT) counter.
* **!(STAT) remove** Removes 1 from (STAT) counter.
* **!(STAT) count** Posts the current (STAT) count for current game. Auto called after stat update.
* **!stats** Posts all stats that are currently set up to be tracked.
		To add to this list, the **!(STAT) new** command must be used.

   **Mod-only commands**
* **!(STAT) add #** Adds # amount to (STAT)
* **!(STAT) remove #** Removes # from (STAT) counter.
* **!(STAT) new** Creates a new (STAT) counter if it has not been used in any game so far.
* **!(STAT) set #** Sets (STAT) to #
 

##Vote
* **!vote #** Vote on choice #. Each person can change their vote as many times while the poll is open, but they will only be counted once. 
* **!vote result** Check what choice is currently winning in an open poll, **OR** What choice won in the last open poll.
* **!vote view** Post the question and choices of the current open poll.


   **Mod-only commands**
* **!vote close** Close the current open poll.
* **!vote open (QUESTION;CHOICE1;CHOICE2;...)** Open a new poll. Question and all choices must be separated by **;**

##Misc
* **!help** Posts a link to this page.
* **!help (COMMAND)** Posts a link to this page and scroll to section for (COMMAND).
* **!advice** Rabbot will post some useful advice.

 **Mod-only commands**
* **!modcheck** Updates the mod list if a mod has been added or removed.

   **Others**
* **!(Depends)** Posts a static response to a command. Or random response from list.
Each command can have different access levels.
* **Admin** = Only usable by streamer or bot admin.
* **Mod** = Only usable by mods on stream.
* **All** = Usable by anyone.

 Feel free to contact me to add a command to this list.
