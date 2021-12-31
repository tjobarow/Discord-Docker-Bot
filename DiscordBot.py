import discord, logging, os
from DockerToolbox import DockerToolbox

#Configuring logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord.log',encoding='utf-8',mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

ALLOWED_USER_LIST = ["tjobarow#5849","Seth#7954"]

#Create Instance of Bot Client
client = discord.Client()

#Create instance of DockerToolbox Class
dtb = DockerToolbox()

#The @client.event will register this as an async event for the client.
@client.event
#When the bot is up and running we print a message to signify so.
async def on_ready():
    print(f"Bot is working and logged in as {client.user}")

#Wait for messages to be sent
@client.event
async def on_message(message):

    #If message starts with "!"
    if message.content.startswith("!"):
        #We do not want to process messages from the bot itself. So we only process messages if message author is not the client (bot) username.
        if message.author != client.user:
            #Since this bot will issue docker API requests, we implment an "allowed users" model. If the discord user has been hardcoded into the apps allow list they can issue commands. 
            if str(message.author) in ALLOWED_USER_LIST:
                
                ###################
                # This section will create a string that lists ALL containters that are returned from the DockerToolbox class.
                # It then sends this as a message onto the text channel.
                ###################
                if "list" in str(message.content):
                    container_str = ""
                    container_index = 1
                    #Need to call the DockerToolbox listContainers() method to update the CONTAINER_LIST and CONTAINER_IDs list.
                    dtb.listContainers()
                    for container in dtb.CONTAINER_LIST:
                        #container_str=""
                        container_str += f"**Container #{container_index}**\n"
                        container_str += f"**ID:** {container['Id']}\n"
                        container_str += f"**Names:** {container['Names'][0]}\n"
                        container_str += f"**State:** {container['State']}\n"
                        container_str += f"**Status:** {container['Status']}\n"
                        container_str+="------------------------------------------------------------------\n"
                        #await message.channel.send(container_str)
                        container_index+=1
                    await message.add_reaction("💻")
                    await message.add_reaction("💯")
                    await message.channel.send(container_str)
                
                ###################
                # This section will restart a docker container using the DockerToolbox class. It requires a container ID as a parameter.
                # It checks that the container ID is valid (in list of container IDs from the DockerToolbox Class)
                # It will notify the user of successful restart.
                # It will notify the user if it FAILED to restart as well.
                ###################
                if "restart" in str(message.content):
                    provided_id = str(message.content.split(" ")[1])
                    if provided_id not in dtb.CONTAINER_IDS:
                        await message.channel.send(f"The provided ID {provided_id} **is not** a valid container ID.")
                    else:
                        result = dtb.restartContainer(provided_id)
                        if result:
                            await message.add_reaction("✅")
                            await message.channel.send(f"The container with ID {provided_id} was successfully restarted.\nPlease check the **!list** command to verify that it is running.")
                        else:
                            await message.add_reaction("❌")
                            await message.channel.send(f"The container with ID {provided_id} **FAILED TO RESTART**.\nPlease check the **!list** command to verify that the container is running before attempting to restart.\n\n*Contact the system administrator if the container is running but this command is failing to restart it.")
                
                
                ###################
                # This section will START a docker container using the DockerToolbox class. It requires a container ID as a parameter.
                # It checks that the container ID is valid (in list of container IDs from the DockerToolbox Class)
                # It will notify the user of successful restart.
                # It will notify the user if it FAILED to restart as well.
                ###################
                if "start" in str(message.content) and "restart" not in str(message.content):
                    provided_id = str(message.content.split(" ")[1])
                    if provided_id not in dtb.CONTAINER_IDS:
                        await message.channel.send(f"The provided ID {provided_id} **is not** a valid container ID.")
                    else:
                        result = dtb.startContainer(provided_id)
                        if result:
                            await message.add_reaction("✅")
                            await message.channel.send(f"The container with ID {provided_id} was successfully started.\nPlease check the **!list** command to verify that it is running.")
                        else:
                            await message.add_reaction("❌")
                            await message.channel.send(f"The container with ID {provided_id} **FAILED TO START**.\n\n*Contact the system administrator if the container is running but this command is failing to restart it.")
                
                ###################
                # This section will reply with list of available commands and their syntax. 
                ###################
                if "help" in str(message.content):
                    help_str = """There are currently four supported commands:\n**!help** - Provides a list of available commands and syntax examples.\n**!list** - Lists ALL containers on the Docker remote host. This is where you retreive IDs for other commands.\n**!restart <<ID>>** - Restarts the container associated with the ID sent\n**!start <<ID>>** - Starts the container associated with the ID sent\n"""
                    await message.channel.send(help_str)
            
            else:
                mention_user = message.author.mention
                await message.channel.send(f"{mention_user}, you are not within the list of approved users to manage game server containers.")

#The client.run() method launches the bot. Takes the secret token from discord as parameter.
client.run(os.environ['DISCORD_BOT_TOKEN'])
