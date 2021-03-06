# StarBot
⚠️Warning⚠️: This bot uses dictionaries as its "database". I've recently learned more about SQL, so I decided to rewrite my bot. Most likely this bot will no longer be maintained. You can find the new bot [here](https://github.com/CircuitSacul/Starboard).

StarBot is a free, advanced, and highly-customizable starboard bot. This documentation gives you a quick start to using the bot, as well as listing all the available commands. If you see a problem, please let me know. You can use the bots `suggest` command, or you can join the support server. My discord username is `@CircuitSacul#5585`.

[Invite StarBot to your server](https://discord.com/api/oauth2/authorize?client_id=700796664276844612&permissions=117824&scope=bot)

[Join the support server](https://discord.gg/3gK8mSA)

## Bot Features:
 - Supports multiple starboards
 - Supports multiple normal and custom emojis for *each* starboard
 - Has default settings and per-starboard settings
 - Image-only channels
 - Auto-star channels
 - Server leaderboard
 - User stats
 - Completely free

(I plan to bring many more features, such as role awards, advanced whitelisting and blacklisting, etc. If you have any suggestions for what features you would like to see, you can use the `suggest <suggestion>` command.)

## How to Read This:
Some things you should know before reading the docs:
 - Don't actually type `<, >, [, ]`
 - Words found inside of these symbols (`[argument]]` or `<argument>`) are called arguments.
 - Arguments inside square brackets (`[argument]`) are optional arguments. You *can* set them, but you don't *have* to.
 - Arguments inside `<, >` (`<argument>`) are required arguments. You *must* set these, and not doing so will cause an error
 - If you see multiple arguments inside of brackets (`[channel_id|channel_name]`), that means that you *can* set *one* or none of those arguments (never more than 1).
 - If you see multiple arguments inside of `<, >` (`<seconds|hours>`), that means you *must* set one of the arguments, no more, no less.
 - I added command aliases to make using the bot quicker. After each command, there is a description, example usage, as well as aliases.
   - commandName: Command description `commandName <how> <to> <use>` `cn <h> <t> <u>`

Here is an example command: Say you wanted to make the bot repeat the word "hello" 10 times. The command to do this is `!repeat <word> [number_of_times=1]`. You would type `!repeat hello 10`. Notice how one of the arguments is inside of the `</>`, while another is inside of the `[/]`? The ones inside the square brackets are `optional arguments`. They have a default value, so you don't always have to type it out. For example, typing `!repeat hello` would repeat the word 1 time, because the default value for `number_of_times` is 1. The other argument, inside of the `</>`, is a required argument. If you don't set it, it will raise an error.

## Setup:
This bot is easy to set up and get going. The following directions are very specific and mostly so you can see how it works, but also gives you an idea of how to configure it for your needs. If you need further help, you can join the [support server](https://discord.gg/3gK8mSA).
 1. [Invite](https://discord.com/api/oauth2/authorize?client_id=700796664276844612&permissions=117824&scope=bot) the bot to your server.
 2. Create a channel called `#starboard` (or whatever you want to name it)
 3. Type `sb starboard add <channel>` to add the starboard.
 4. Type `sb starboard requiredstars <starboard> 1` (Setting the number of stars for a message to get on the starboard to 1, so you can test it easily.
 5. Type `sb starboard selfstar <starboard> true` (This allows you to star your own messages, otherwise it would be hard to test the bot)
 6. Now, we need to add an emoji. In this case, we are going to use the `star` emoji. Type `sb starboard addemoji <starboard> :star:`
 7. Now send a message in the channel, and react with the `star` emoji. It should appear on the starboard!

## Other Settings You Can Change:
 - requiredStars: How many points it needs before it appears on your starboard. 
   - Specific Starboard: `sb starboard requiredstars <starboard> <number_of_stars>`
   - Default Setting: `sb defaults requiredstars <number_of_stars>`
 - requiredToLose: How *few* stars a message needs to have before it gets *removed* from a starboard.
   - Specific Starboard: `sb starboard requiredtolose <starboard> <number_of_stars>`
   - Default Setting: `sb defaults requiredtolose <number_of_stars>`
- selfStar: Wether or not a user can star their own messages.	
   - Specific Starboard: `sb starboard selfstar <starboard> <true|false>`	
   - Default Setting: `sb defaults selfstar <true|false>`	
 - linkEdits: Wether or not the starboard message should update if the original message get's edited.	
   - Specific Starboard: `sb starboard linkedits <starboard> <true|false>`	
   - Default Setting: `sb defaults linkedits <true|false>`	
 - linkDeletes: Whether or not the starboard message should be deleted if the original message is deleted.	
   - Specific Starboard: `sb starboard linkdeltes <starboard> <true|false>`	
   - Default Setting: `sb defaults linkdeletes <true|false>`	
 - Emojis: (Default is no emoji, and cannot be changed)	
   - Add: `sb starboard addemoji <starboard> <emoji>`	
   - Remove: `sb starboard removeemoji <starboard> <emoji>`	

## Complete Command List:	
 - No Category:	
   - help: Get help with commands `help [commands|category]`
   - info: Bot stats	`info`
   - links: Get helpful links	`links`
   - ping: Get bot latency `ping`
   - suggest: Send suggestion to me	`suggest <suggestion>`
 - Settings:	
   - starboard: List starboards	`starboard` `s`
     - add: Add a starboard	`starboard add <channel>` `s a <channel>`
     - remove: Remove a starboard	`starboard remove <starboard>` `s r <starboard>`
     - addemoji: Add emoji to starboard	`starboard addemoji <starboard> <emoji>` `s ae <starboard> <emoji>`
     - removeemoji: Remove emoji from starboard	`starboard removeemoji <starboard> <emoji>` `s re <starboard> <emoji>`
     - linkdeletes: Set link-deletes for starboard	`starboard linkdeletes <starboard> <true|false>` `s ld <starboard> <true|false>`
     - linkedits: Set link-edits for starboard	`starboard linkedits <starboard> <true|false>` `s le <starboard> <true|false>`
     - requiredstars: Set required-stars for starboard	`starboard requiredstars <starboard> <required_stars>` `s rs <starboard> <required_stars`
     - requiredtolose: Set required-to-lose for starboard	`starboard requiredtolose <starboard> <required_to_lose>` `s rtl <starboard> <required_to_lose>`
     - selfstar: Set self-star for starboard	`starboard selfstar <starboard> <true|false>` `s ss <starboard> <true|false>`
   - defaults: View default settings for starboards	`defaults` `d`
     - linkdeletes: Set default for linkDeletes	`defaults linkdeletes <true|false>` `d ld <true|false>`
     - linkedits: Set default for linkEdits	`defaults linkedits <true|false>` `d le <true|false>`
     - requiredstars: Set default for requiredStars	`defaults requiredstars <required_stars>` `d rs <required_stars>`
     - requiredtolose: Set default for requiredToLose	`defaults requiredtolose <required_to_lose>` `d rtl <required_to_lose>`
     - selfstar: Set default for selfStar	`defaults selfstar <true|false>` `d ss <true|false>`
   - mediachannel: List all media-channels `mediachannel` `mc`
     - add: Add a new media channel `mediachannel add <channel>` `mc a <channel>`
     - remove: Remove a media channel `mediachannel remove <channel>` `mc r <channel>`
     - mediaonly: Wether or not to delete messages that don't include attachments `mediachannel mediaonly <channel> <true|false>` `mc mo <channel> <true|false>`
     - addemoji: Adds an emoji for the bot to automatically to react to all messages with `mediachannel addemoji <channel> <emoji>` `mc ae <channel> <emoji>`
     - removeemoji: Removes an emoji from media channel `mediachannel removeemoji <channel> <emoji>` `mc re <channel> <emoji>`
   - prefix: Change bot prefix `prefix <prefix> [has_space=False]`
 - Utility:
   - recount: Recounts the emojis on a message `recount <channel> <message_id>`
 - Leaderboard:
   - leaderboard: View the top users of the server and other stats `leaderboard` `lb`
     - reset: Reset the leaderboard for a server `leaderboard reset` `lb reset`
   - user: View stats for a user, such as stars given, received, etc. `user [username, id, or mention]` `u [username, id, or mention]`
