import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import sys
import random
import math
import os

mode = "Talk"
prefix = "/"
greetings = ["hello","hi","howdy","whats up","what's up","sup","hey"]

Client = discord.Client()
client = commands.Bot(command_prefix = prefix)


@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    message.content = str(message.content)
    if any(msg+" testbot" in message.content.lower() for msg in greetings):
        if message.author.id in ("430358551974772739","460966585549717514"):
            await client.send_message(message.channel, "Hello Master!")
        elif "441392915986776064" in [role.id for role in message.author.roles]:
            await client.send_message(message.channel, "Hello Admin <@"+message.author.id+">!")
        else:
            await client.send_message(message.channel, "Hello <@"+message.author.id+">!")
    elif message.content == prefix+"DIE" and message.author.id == "430358551974772739":
        await client.send_message(message.channel, "OOF")
        sys.exit()
    elif message.content.lower() == prefix+"guess":
        high = 128
        trials = 7
        num = random.randint(1,high)
        skipped = False
        eff = 0
        acteff = 1
        acteffsub = 0
        guesses = [0,129]
        logicals = list(range(1,129))
        await client.send_message(message.channel, "Hello <@"+message.author.id+">!  Let's play a guessing game!  Im thinking of a number between 1 and 128. Take a guess! (1/"+str(trials)+")")
        for i in range(trials):
            while True:
                guess = await client.wait_for_message(author=message.author)
                try:
                    guess.content = int(guess.content)
                    if guess.content in list(range(1,high+1)):
                        guesses.append(guess.content)
                    if guess.content > num and guess.content < max(guesses):
                        guesses.remove(max(guesses))
                    elif guess.content < num and guess.content > min(guesses):
                        guesses.remove(min(guesses))
                    if guess.content in logicals and guess.content != math.ceil(((max(logicals)+min(logicals))/2)) and guess.content != math.floor(((max(logicals)+min(logicals))/2)):
                        eff += abs(((max(logicals)+min(logicals))/2)-abs(guess.content-(max(logicals)+min(logicals))/2))/((max(logicals)+min(logicals))/2)
                        acteff *= abs(((max(logicals)+min(logicals))/2)-abs(guess.content-(max(logicals)+min(logicals))/2))/((max(logicals)+min(logicals))/2)
                        #print((((max(logicals)+min(logicals))/2)-abs(guess.content-(max(logicals)+min(logicals))/2)))
                        #print(((max(logicals)+min(logicals))/2))
                        #print(abs(((max(logicals)+min(logicals))/2)-abs(guess.content-(max(logicals)+min(logicals))/2))/((max(logicals)+min(logicals))/2)) 
                    elif guess.content == math.ceil(((max(logicals)+min(logicals))/2)) or guess.content == math.floor(((max(logicals)+min(logicals))/2)):
                        eff += 1
                        #print("RAN")
                    elif not guess.content in logicals:
                        '''
                        acteff *= 0.000000000000001
                        if abs(acteff) < 0.000000000000001:
                            acteff = 0
                        #print(acteff)
                        '''
                        acteffsub += 1/trials
                        pass
                    else:
                        #print(guess.content == math.ceil(((max(logicals)+min(logicals))/2)),guess.content == math.floor(((max(logicals)+min(logicals))/2)))
                        #print(guess.content, (max(logicals)+min(logicals))/2)
                        #print(logicals)
                        pass
                    logicals = list(range(min(guesses)+1,max(guesses)))
                    #1,2,3,4,5,6,7
                    #5
                    #1/4
                    break
                except:
                    if guess.content.lower() == "skip" and message.author.id == "430358551974772739":
                        await client.send_message(message.channel, "You were right!")
                        await client.send_message(message.channel, "You guessed it in 0 tries!")
                        skipped = True
                        break
            if skipped:
                break
            if guess.content == num:
                await client.send_message(message.channel, "You were right!")
                await client.send_message(message.channel, "You guessed it in "+str(i+1)+" tries!")
                await client.send_message(message.channel, "Average Guess Efficiency: "+str(eff/(i+1)*100)+"%")
                await client.send_message(message.channel, "Real Guess Efficiency: "+str((acteff**(1/(i+1))-acteffsub)*100)+"%")
                break
            elif i != trials-1:
                if guess.content > num:
                    await client.send_message(message.channel, "Too high! Try again("+str(i+2)+"/"+str(trials)+")")
                elif guess.content < num:
                    await client.send_message(message.channel, "Too low!  Try again("+str(i+2)+"/"+str(trials)+")")
            else:
                await client.send_message(message.channel, "You're a failure :/")
                await client.send_message(message.channel, "The number was: "+str(num))
                await client.send_message(message.channel, "Average Guess Efficiency: "+str(eff/(i+1)*100)+"%")
                await client.send_message(message.channel, "Real Guess Efficiency: "+str((acteff**(1/(i+1))-acteffsub)*100)+"%")
    elif message.content.lower().startswith(prefix+"countdown"):
        args = message.content.split()
        num = int(args[1])
        msg = await client.send_message(message.channel, num)
        while num > 1:
            num -= 1
            await asyncio.sleep(1)
            await client.edit_message(msg, num)
    elif message.content.lower().startswith("i'm") or message.content.lower().startswith("im"):
        pass
        #args = message.content.split()
        #args = " ".join(args[1:])
        #await client.send_message(message.channel, "Hello "+args+", I'm Dad!")
    elif message.content.lower() == prefix+"ping":
        await client.send_message(message.channel, "Pong! <@"+message.author.id+">")

@client.event
async def on_message_delete(message):
    await client.send_message(client.get_channel("441431242546872320"), "The message:\n'"+message.content+"'\nby <@"+message.author.id+"> has been deleted")


client.run(os.environ["TOKEN"])
