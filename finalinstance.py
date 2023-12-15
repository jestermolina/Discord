#Import of the class libraries to interact with discord, import the token file, interact with operating system and randomly generate something

import discord
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

print(ec2_metadata.region)
print(ec2_metadata.instance_id)

'''Load the .env file that contains the discord bot token using load_dotenv(). To create the discord bot client, I used discord.Bot(). Retreive the token from the .env file and converts it into a string'''

client = discord.Bot()
token = str(os.getenv('TOKEN'))

'''Created a client event that is initiated once the discord bot connects to the discord server. Once the bot is connected, it will print the messages of the bot logging in, the region, instance id and public ip address'''

@client.event 
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
    print(f'EC2 Region: {ec2_metadata.region}')
    print(f'EC2 Instance ID: {ec2_metadata.instance_id}')
    print(f'Public IP Address: {ec2_metadata.public_ipv4}')

'''Created another client event that is initiated once a message is sent into the channel where the bot has access to. This event also retrieves information such as username, channel name, and what the message is for the instance terminal.'''

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    #This statement is used to prevent the bot from responding to itself
    print(f'Message {user_message} by {username} on {channel}')

    if message.author == client.user:
        return
    
    #In this if statement, the bot can only respond to channels random, the covenant, and general. The specific channel from the server must be specified for the bot to respond. 
    if channel == 'random' or 'the-covenant' or 'general':

        #The try and else blocks are used as an error handler to give an error message if the bot cannot connect or loses connection from the server.
        try:
            #In the try block there are if, elif, and else statements housing the promts and responses.
            if user_message.lower() == "hello" or user_message.lower() == "hi":
                await message.channel.send(f'Hello {username}')
                return
            
            elif user_message.lower() == "hello world!":
                await message.channel.send(f'Hello!')
            
            elif user_message.lower() == "tell me about my server":#If the bot receives this message, it pulls information from the ec2 metadata and responds accordingly.
                await message.channel.send(f'EC2 Region: {ec2_metadata.region}\nEC2 Instance ID: {ec2_metadata.instance_id}\nIP Address: {ec2_metadata.public_ipv4}')#To make the response from the bot look more organized, I added a \n to start a new line for each section of its response.
            
            elif user_message.lower() == "bye":
                await message.channel.send(f'Bye {username}')
            
            #This handles any other inputs not matching the conditions above
            else:
                await message.channel.send(f"Sorry, I don't understand")
        #If the try function fails, cannot connect to the server, the except block becomes true and posts this response.
        except Exception as e:
            await message.channel.send(f"An error has occured: {e}")

#This allows the bot to run and connect to the discord using the discord token.
client.run(token)

