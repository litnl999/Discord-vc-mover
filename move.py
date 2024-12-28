import discord
from discord.ext import commands
import asyncio

# Bot configuration
TOKEN = 'BOTTOKEN'
PREFIX = '!'

AUTHORIZED_USERS = [
    USERID,
]

# Channel IDs for moving user
CHANNEL_1_ID = CHANNELID1
CHANNEL_2_ID = CHANNELID2

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True


bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Bot is ready to use!') 
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        error_msg = await ctx.send("You don't have the required permissions to use this command!")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        error_msg = await ctx.send("Missing required arguments! Usage: !move_users @user amount")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
    else:
        error_msg = await ctx.send(f"An error occurred: {str(error)}")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()

@bot.command()
async def move_users(ctx, member: discord.Member, amount: int):

    if ctx.author.id not in AUTHORIZED_USERS:
        error_msg = await ctx.send("You are not authorized to use this command!")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
        return


    if amount <= 0:
        error_msg = await ctx.send("Please provide a positive number for the amount of moves!")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
        return

    
    if not member.voice:
        error_msg = await ctx.send(f"{member.name} is not in a voice channel!")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
        return

    original_channel = member.voice.channel

    channel1 = ctx.guild.get_channel(CHANNEL_1_ID)
    channel2 = ctx.guild.get_channel(CHANNEL_2_ID)


    if not channel1 or not channel2:
        error_msg = await ctx.send("One or both channels are not properly configured!")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
        return

    try:
        start_msg = await ctx.send(f"Starting to move {member.name} {amount} times...")
        
        for i in range(amount):

            await member.move_to(channel2)
            await asyncio.sleep(0.1)
            
            await member.move_to(channel1)
            await asyncio.sleep(0.1)
        

        await member.move_to(original_channel)
        

        await start_msg.delete()
        
        # Send and then delete the completion message
        complete_msg = await ctx.send(f"Successfully moved {member.name} {amount} times!")
        await asyncio.sleep(5)
        await complete_msg.delete()
        
        # Delete the original command message
        await ctx.message.delete()
    
    except discord.Forbidden:
        error_msg = await ctx.send("I don't have permission to move users!")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()
    except Exception as e:
        error_msg = await ctx.send(f"An error occurred while moving the user: {str(e)}")
        await asyncio.sleep(5)
        await error_msg.delete()
        await ctx.message.delete()

# Run the bot
bot.run(TOKEN)
