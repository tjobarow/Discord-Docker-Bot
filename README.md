# Docker Discord Bot - Control Containers Through Discord Text Channels

## What is it?
This bot allows for a hard-coded list of "allowed users" to execute docker container commands via Discord Chat and Docker Remote API. This was built because I am hosting some game server containers, and sometimes they need to be restarted to update their software. I am not always available to do so, so now my friends are able to do it on their own. 

*Note - The only functionality this currently allows is to list all containers running, restart a container, or start a container. It does not allow for removing a container, etc.*
*Note - This is currently under development and is not accessible for public use, sorry.*

## What can it do?
There are currently four supported commands:
!help - Provides a list of available commands and syntax examples. 
!list - Lists ALL containers on the Docker remote host.
!restart <<ID>> - Restarts the container associated with the ID sent
!start <<ID>> - Starts the container associated with the ID sent


## Prerequistes
Before you run bot:
Have your Discord application secret handy. 
Make sure the docker remote API has been enabled on the target host. Make note of IP/FQDN & Port (typically 2375).

## How to build the container image
1. Edit the "Dockerfile_Redacted" file to include the Docker Remote API URL, and Discord secret as ENV variables. The bot will retreive these at runtime. 

```ENV DOCKER_BASE_URL = <DOCKER REMOTE API ENDPOINT/URL, I.E HTTP://127.0.0.1:2375>```

```ENV DISCORD_BOT_TOKEN = <PLACE KEY HERE>```

2. Change the "Dockerfile_Redacted" name to just "Dockerfile"
3. Create a directory on the host machine to use for persistent log storage
        e.g: mkdir -p /var/log/discord_bot
4. Build the image. This command should be ran from the Docker_Discord_Bot directory. Copy the image ID for step 5.
        docker build -t tjobarow/docker_discord_bot:docker-discord-v1 .
5. Run a container based on the image. Make sure to replace the local directory volume, with the one you created in step 3. 
        docker run -d --name discord_bot -v /absolute/path/to/log/folder:/app/logs <IMAGE ID>
6. The bot should now be operational. 
