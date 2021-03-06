import discord, db_handler as dbh, copy
from asyncio import Lock
from discord.ext import commands
from typing import Union
import functions
from converters import ChannelElseInt


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        name='prefix', aliases=['p'], brief='Set prefix',
        description='Set prefix for server'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def set_prefix(self, ctx, prefix, space: bool = False):
        if prefix == '':
            await ctx.send("That cannot be the prefix")
            return
        new_prefix = f"{prefix}{' ' if space else ''}"
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['prefix'] = new_prefix
        await ctx.send(f"Set prefix to `{new_prefix}`")


    @commands.group(
        name='defaults', aliases=['d'], description='Set the default settings when starboards are added',
        brief='Manage default starboard settings'
    )
    @commands.guild_only()
    async def defaults(self, ctx):
        if ctx.invoked_subcommand == None:
            settings = dbh.database.db['guilds'][ctx.guild.id]['default_settings']
            embed = discord.Embed(title='Starboard Defaults', color=0xFCFF00)
            msg = ''
            msg += f"**requiredStars:** {settings['required_stars']}\n"
            msg += f"**requiredToLose:** {settings['required_to_lose']}\n"
            msg += f"**selfStar:** {settings['self_star']}\n"
            msg += f"**linkEdits:** {settings['link_edits']}\n"
            msg += f"**linkDeletes:** {settings['link_deletes']}\n"
            embed.description = msg
            await ctx.send(embed=embed)


    @defaults.command(
        name='selfstar', aliases=['ss'], description='Set the default for allowing self-stars',
        brief='Set default for self-star'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggle_self_star(self, ctx, self_star: bool):
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['default_settings']['self_star'] = self_star
        await ctx.send(f"Set selfStar to {self_star}.")


    @defaults.command(
        name='requiredstars', aliases=['rs'], description='Set the default for minimum stars for message',
        brief='Set default for required-stars'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def required_stars(self, ctx, count: int):
        if count <= dbh.database.db['guilds'][ctx.message.guild.id]['default_settings']['required_to_lose']:
            await ctx.send("requiredStars cannot be less than or equal to requiredToLose")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['default_settings']['required_stars'] = count
        await ctx.send(f"The default for requiredStars has been set to {count}")


    @defaults.command(
        name='requiredtolose', aliases=['rtl'], defaults='Set the default for maximum stars before message is removed',
        brief='Set default for required-to-lose'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def required_to_lose(self, ctx, count: int):
        if count >= dbh.database.db['guilds'][ctx.message.guild.id]['default_settings']['required_stars']:
            await ctx.send("requiredToLose cannot be greater than or equal to requiredStars.")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.message.guild.id]['default_settings']['required_to_lose'] = count
        await ctx.send(f"The default for requiredToLose has been set to {count}.")

    @defaults.command(
        name='linkedits', aliases=['le'], description='Set the default for linking message edits',
        brief='Set default for link-deletes'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggle_link_edits(self, ctx, link_edits: bool):
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.message.guild.id]['default_settings']['link_edits'] = link_edits
        await ctx.send(f"The default for linkEdits has been set to {link_edits}")

    @defaults.command(
        name='linkdeletes', aliases=['ld'], description='Set the default for linking message deletes',
        brief='Set default for link-edits'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def toggle_link_deletes(self, ctx, link_deletes: bool):
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.message.guild.id]['default_settings']['link_deletes'] = link_deletes
        await ctx.send(f"The default for linkDeletes has been set to {link_deletes}")


    @commands.group(
        name='starboard', aliases=['s'], invoke_without_command=True, description='Managed starboards',
        brief='Manage starboards'
    )
    @commands.guild_only()
    async def channel(self, ctx, channel:discord.TextChannel=None):
        if ctx.invoked_subcommand == None:
            msg = ''
            if channel is None:
                settings = dbh.database.db['guilds'][ctx.guild.id]['channels']
                if ctx.guild.id not in dbh.database.locks:
                    dbh.database.locks[ctx.guild.id] = Lock()
                async with dbh.database.locks[ctx.guild.id]:
                    for channel_id in dbh.database.db['guilds'][ctx.guild.id]['channels']:
                        channel_object = discord.utils.get(ctx.guild.channels, id=channel_id)
                        if channel_object is None:
                            msg += f"Deleted Channel; ID: {channel_id}\n"
                            continue
                        emoji_str = await functions.get_emoji_str(ctx.guild, settings[channel_id]['emojis'])
                        msg += f"{channel_object.mention}: {emoji_str}\n"
            else:
                settings = dbh.database.db['guilds'][ctx.guild.id]['channels']
                channel_object = discord.utils.get(ctx.guild.channels, id=channel.id)
                emoji_str = await functions.get_emoji_str(ctx.guild, settings[channel.id]['emojis'])
                msg += f"{channel_object.mention}: {emoji_str}\n"
                msg += f"**----requiredStars:** {settings[channel.id]['required_stars']}\n"
                msg += f"**----requiredToLose:** {settings[channel.id]['required_to_lose']}\n"
                msg += f"**----selfStar:** {settings[channel.id]['self_star']}\n"
                msg += f"**----linkEdits:** {settings[channel.id]['link_edits']}\n"
                msg += f"**----linkDeletes:** {settings[channel.id]['link_deletes']}\n"
            if msg == '':
                msg = 'No starboards have been set. Use `<prefix> starboard add <channel>` to add one.'
            embed = discord.Embed(title='Starboards', description=msg, color=0xFCFF00)
            await ctx.send(embed=embed)


    @channel.command(
        name='selfstar', aliases=['ss'], description='Set self-star for specific starboard',
        brief='Set self-star for starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel_self_star(self, ctx, channel: discord.TextChannel, allow: bool):
        if channel == None:
            await ctx.send("I could not find any channel with that name or id")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['self_star'] = allow
        await ctx.send(f"Set selfStar to {allow} for {channel.mention}")


    @channel.command(
        name='linkedits', aliases=['le'], description='Set link-edits for specific starboard',
        brief='Set link-edits for starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel_link_edits(self, ctx, channel: discord.TextChannel, link_edits: bool):
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['link_edits'] = link_edits
        await ctx.send(f"Set linkEdits to {link_edits} for {channel.mention}")


    @channel.command(
        name='linkdeletes', aliases=['ld'], description='Set link-deletes for specific starboard',
        brief='Set link-deletes for starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel_link_deletes(self, ctx, channel: discord.TextChannel, link_deletes: bool):
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['link_deletes'] = link_deletes
        await ctx.send(f"Set linkDeletes to {link_deletes} for {channel.mention}")


    @channel.command(
        name='add', aliases=['+', 'a'], description='Add a new starboard',
        brief='Add starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def add_channel(self, ctx, channel: discord.TextChannel):
        if channel == None:
            await ctx.send("I could not find any channel with that name or id")
            return

        try:
            dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]
        except KeyError:
            if ctx.guild.id not in dbh.database.locks:
                dbh.database.locks[ctx.guild.id] = Lock()
            async with dbh.database.locks[ctx.guild.id]:
                dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id] = copy.deepcopy(dbh.database.db['guilds'][ctx.guild.id]['default_settings'])
                dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['emojis'] = []
                dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['messages'] = {}
            await ctx.send(f"Added starboard {channel.mention}")
            return
        await ctx.send(f"{channel.mention} is already a starboard")


    @channel.command(
        name='remove', aliases=['-', 'delete', 'd', 'r'], description='Remove a starboard',
        brief='Remove starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def remove_channel(self, ctx, channel: ChannelElseInt):
        if channel == None:
            await ctx.send("I could not find any channel with that name or id")
            return

        try:
            channel_id = channel if isinstance(channel, int) else channel.id
            if ctx.guild.id not in dbh.database.locks:
                dbh.database.locks[ctx.guild.id] = Lock()
            async with dbh.database.locks[ctx.guild.id]:
                del dbh.database.db['guilds'][ctx.guild.id]['channels'][channel_id]
            await ctx.send(f"{channel_id if isinstance(channel, int) else channel.mention} is no longer a starboard")
        except KeyError:
            await ctx.send("That channel is not a starboard")


    @channel.command(
        name='addemoji', aliases=['ae'], description='Add emoji for specific starboard',
        brief='Add emoji'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def starboard_add_emoji(self, ctx, channel: discord.TextChannel, in_emoji):
        emoji = await functions.get_emoji(ctx.guild, in_emoji)
        if type(emoji) is discord.Emoji:
            emoji = emoji.id
        try:
            if ctx.guild.id not in dbh.database.locks:
                dbh.database.locks[ctx.guild.id] = Lock()
            async with dbh.database.locks[ctx.guild.id]:
                dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['emojis'].append(emoji)
            await ctx.send(f"Added {in_emoji} to {channel.mention}")
        except KeyError:
            await ctx.send(f"{channel.mention} is not a starboard.")


    @channel.command(
        name='removeemoji', aliases=['re'], description='Removed emoji for specific starboard',
        brief='Remove emoji'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def starboard_remove_emoji(self, ctx, channel: discord.TextChannel, in_emoji):
        emoji = await functions.get_emoji(ctx.guild, in_emoji)
        if type(emoji) is discord.Emoji:
            emoji = emoji.id
        try:
            if ctx.guild.id not in dbh.database.locks:
                dbh.database.locks[ctx.guild.id] = Lock()
            async with dbh.database.locks[ctx.guild.id]:
                found = False
                if emoji in dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['emojis']:
                    dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['emojis'].remove(emoji)
                    found = True
                else:
                    try:
                        if int(emoji) in dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['emojis']:
                            dbh.database.db['guilds'][ctx.guild.id]['channels'][channel.id]['emojis'].remove(int(emoji))
                            found = True
                    except Exception as e:
                        print(e)
            if found:
                await ctx.send(f"Removed {in_emoji} from {channel.mention}")
            else:
                await ctx.send(f"Could not find that emoji in {channel.mention}")
        except KeyError:
            await ctx.send(f"Either {in_emoji} is not linked to {channel.mention} or {channel.mention} is not a starboard.")


    @channel.command(
        name='requiredstars', aliases=['rs'], description='Set minimum stars for message to appear on starboard for specific starboard',
        brief='Set required-stars for starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel_required_stars(self, ctx, channel: discord.TextChannel, count: int):
        if channel == None:
            await ctx.send("I could not find any channel with that name or id")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            if count <= dbh.database.db['guilds'][ctx.message.guild.id]['channels'][channel.id]['required_to_lose']:
                await ctx.send("requiredStars cannot be less than or equal to requiredToLose")
                return
            dbh.database.db['guilds'][ctx.message.guild.id]['channels'][channel.id]['required_stars'] = count
        await ctx.send(f"Set requiredStars to {count}")


    @channel.command(
        name='requiredtolose', aliases=['rtl'], description='Set minimum stars before message is removed for specific starboard',
        brief='Set required-to-lose for starboard'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def channel_required_to_lose(self, ctx, channel: discord.TextChannel, count: int):
        if channel == None:
            await ctx.send("I could not find any channel with that name or id")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            if count >= dbh.database.db['guilds'][ctx.message.guild.id]['channels'][channel.id]['required_stars']:
                await ctx.send("requiredToLose cannot be greater than or equal to requiredStars")
                return
            dbh.database.db['guilds'][ctx.message.guild.id]['channels'][channel.id]['required_to_lose'] = count
        await ctx.send(f"requiredToLose has been set to {count}")

    @commands.group(
        name='mediachannel', aliases=['mc'], description='Manage media channels, where the bot automatically reacts to messages with an emoji.',
        brief='Manage media channels', invoke_without_command=True
    )
    @commands.guild_only()
    async def media_channels(self, ctx, channel: discord.TextChannel=None):
        string = ''
        if channel is None:
            if ctx.guild.id not in dbh.database.locks:
                dbh.database.locks[ctx.guild.id] = Lock()
            async with dbh.database.locks[ctx.guild.id]:
                for media_channel_id in dbh.database.db['guilds'][ctx.guild.id]['media_channels']:
                    media_channel = discord.utils.get(ctx.guild.channels, id=media_channel_id)
                    if media_channel is not None:
                        emojis = dbh.database.db['guilds'][ctx.guild.id]['media_channels'][media_channel_id]['emojis']
                        emoji_str = await functions.get_emoji_str(ctx.guild, emojis)
                        string += f"{media_channel.mention}: {emoji_str}\n"
                    else:
                        string += f"Deleted Channel; ID: {media_channel_id}"
                if string == '':
                    string = "You have no media channels set. Use `<prefix> mediachannel add <channel>` to add one."
        else:
            settings = dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]
            emojis = settings['emojis']
            emoji_str = await functions.get_emoji_str(ctx.guild, emojis)
            string = f"{channel.mention}: {emoji_str}\n**----mediaOnly:** {settings['media_only']}"
        embed = discord.Embed(title='Media Channels', description=string, color=0xFCFF00)
        await ctx.send(embed=embed)

    @media_channels.command(
        name='add', aliases=['a', '+'], brief='Add a media channel', description='Add a media channel'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def add_media_channel(self, ctx, channel: discord.TextChannel):
        if channel is None:
            await ctx.send("I could not find a channel with that name or id")
            return
        if channel.id in dbh.database.db['guilds'][ctx.guild.id]['media_channels']:
            await ctx.send("That is already a media channel")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id] = {
                'emojis': [],
                'media_only': False
            }
            await ctx.send("Added media channel")

    @media_channels.command(
        name='remove', aliases=['r', '-'], brief='Remove media channel', description='Remove media channel'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def remove_media_channel(self, ctx, channel: ChannelElseInt):
        if channel is None:
            await ctx.send("I could not find a channel with that name or id")
            return

        channel_id = channel if isinstance(channel, int) else channel.id
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            if channel_id not in dbh.database.db['guilds'][ctx.guild.id]['media_channels']:
                await ctx.send("That does not appear to be a media channel")
                return
            del dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel_id]
            await ctx.send(f"{channel if isinstance(channel, int) else channel.mention} is no longer a media channel")

    @media_channels.command(
        name='addemoji', aliases=['ae'], brief='Add an emoji to media channel',
        description='Adds an emoji for the bot to automatically react to all messages sent in the media channel'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def media_channel_add_emoji(self, ctx, channel: discord.TextChannel, in_emoji):
        emoji = await functions.get_emoji(ctx.guild, in_emoji)
        if type(emoji) is discord.Emoji:
            emoji = emoji.id
        if channel is None:
            await ctx.send("I could not find a channel with that name or id")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            if channel.id not in dbh.database.db['guilds'][ctx.guild.id]['media_channels']:
                await ctx.send("That is not a media channel")
                return
            dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]['emojis'].append(emoji)
            await ctx.send(f"Added {in_emoji} to {channel.mention}")

    @media_channels.command(
        name='removeemoji', aliases=['re'], brief='Remove an emoji from media channel',
        description='Remove an emoji from media channel'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def media_channel_remove_emoji(self, ctx, channel: discord.TextChannel, in_emoji):
        emoji = await functions.get_emoji(ctx.guild, in_emoji)
        if type(emoji) is discord.Emoji:
            emoji = emoji.id
        if channel is None:
            await ctx.send("I could not find a channel with that name or id")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            if channel.id not in dbh.database.db['guilds'][ctx.guild.id]['media_channels']:
                await ctx.send("That is not a media channel")
                return
            found = False
            if emoji in dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]['emojis']:
                dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]['emojis'].remove(emoji)
                found = True
            else:
                try:
                    if int(emoji) in dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]['emojis']:
                        dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]['emojis'].remove(int(emoji))
                        found = True
                except Exception as e:
                    print(e)
            if found:
                await ctx.send(f"Removed {in_emoji} from {channel.mention}")
            else:
                await ctx.send(f"Could not find that emoji in {channel.mention}")

    @media_channels.command(
        name='mediaonly', aliases=['mo', 'imagesonly'], brief='Set mediaOnly for media channel',
        description='Set wether or not a media channel allows messages without images'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def media_channel_media_only(self, ctx, channel: discord.TextChannel, allow: bool):
        if channel is None:
            await ctx.send("I could not find a channel with that name or id")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        async with dbh.database.locks[ctx.guild.id]:
            if channel.id not in dbh.database.db['guilds'][ctx.guild.id]['media_channels']:
                await ctx.send("That is not a media channel")
                return
            dbh.database.db['guilds'][ctx.guild.id]['media_channels'][channel.id]['media_only'] = allow
            await ctx.send(f"Set mediaOnly to {allow} for {channel.mention}")