
# CCBot

This is a discord bot for a french server called La Terre Promise (LTP). I'm releasing the source code to show the progress, feel free to open issues/PRs if you want nonetheless.

## Features

This bot was made to have connectivity with discord and a minecraft server using pterodactyl as a panel. You can see more about the features in the screenshots section below.
Features include:
- A status channel where an embed containing some info about the server is updated every 20 seconds.
- A console channel (recommended to be made private) where all of the pterodactyl console is outputted (updates every 5 seconds). You can set 'cadmins' (console admins) and 'cloweradmins' (console lower admins) to send commands in the console directly from the console channel using ```.command``` (for example ```.say Hello World!```). Admins can send any command they want, whereas lower admins can only send the commands defined in the ```cadmins.json``` file.
- A whitelist channel and a usernames channel. The users in discord can send their minecraft usernames in thee usernames channel, while they wait to be whitelisted. When someone (an admin in most cases) enters a username in the whitelist channel, the username is whitelisted in the minecraft server and the user is notified via a discord DM.
- A graph channel where (currently) 3 graphs are sent. One for the number of online players this last hour (updated every minute), one for the number of players online in the last day (updated every hour) and one showing the minutes played of the 10 most active players (updated every minute). Currently the graphs aren't very good looking, but this is something I plan to improve.
- A message sent to the admin channel whenever the server doesn't respond 3 times (5 seconds interval between each ping). This warning will be soon able to be disabled using the ```ccb no-notify``` command.
- A way to DM users directyl with the bot. You use ```ccb open_dm <discord_id>``` and a new channel is automatically created in a DMs category (defined in ```.env```). Then, every message/attachment sent in the channel/DM will be sent to the other part. Note that if you start your message with ```_``` on the channel (ex: _this individual is suspect), this won't be sent to the user in the DM.
- Bot presence: switches between "Watching <players> players online on the server" to "Watching <accounts> accounts online on the discord server" every 10 seconds.
- A ```ccb ping```, ```ccb dmping``` and ```ccb reload filename``` for easier development of the bot.
- A ```ccb say``` command to make the bot say something.



## Environment Variables

To run this bot on your machine, you'll need to create a ```.env``` file based on the structure of ```.env.example```. It should be pretty self-explanatory.

> [!WARNING]
> Currently, the bot was only made to be used in LTP, and not filling **all** the ```.env``` fields might make the script crash, even if you don't want to use all the features in it.


## Screenshots
<img src="https://github.com/user-attachments/assets/ecaca717-42fb-4baa-8955-2c292583d45d" height=300>
<img src="https://github.com/user-attachments/assets/08ced55d-07da-405c-b356-7ed14f7be505" height=300>
<img src="https://github.com/user-attachments/assets/3b3d55f4-5ce3-4e4e-8168-3334b150794e" width=600>
<img src="https://github.com/user-attachments/assets/968970dd-7af4-445c-84dc-f60e40fd98be" width=600>
<img src="https://github.com/user-attachments/assets/17ad58f3-f5eb-48ab-9e72-aac114ea4faa" width=600>
<img src="https://github.com/user-attachments/assets/95d5e906-f0e3-4ee5-91c4-dc3874b7514e" width=300>
<img src="https://github.com/user-attachments/assets/d85336ea-692d-4cbd-9675-a168781ee044" width=300>


