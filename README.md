# spinning-wheel-challenge

A tool to aid Overwatch content creator mL7 determine what are the top upvoted user-submitted challenges in his community Discord server for his Spinning Wheel Challenge.

## Invite Link

To invite the bot your server, [click here](https://discord.com/api/oauth2/authorize?client_id=1118986175928090624&permissions=68672&scope=bot).

## Maintenance

Use the following command to upgrade packages in `requirements.txt`:

```bash
pip install -U -r requirements.txt
```

## Installation

These instructions are mostly for myself, so I can remember how to re-install the project.

### Development Environment

After cloning the repo, create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Now you can install the packages using the requirements file:

```bash
pip install -r requirements.txt
```

The following command creates a `.env` file containing our environment variables:

```bash
echo -e "DISCORD_TOKEN=\nCHANNEL_ID=\nUSER_ID=\n" >> .env
```

### Create the bot account and invite it to your Server

Head to <https://discord.com/developers/applications> and Create a New Application.

After creating your application, head to the Bot tab and create a new bot.

Then add the bot to a server using the OAuth2 tab, scroll down to scopes, check bot and visit the generated URL.

### Environment Variables

To obtain the `CHANNEL_ID` and `USER_ID`, enable Developer Mode on Discord. User Settings > Advanced > Developer Mode.

* `DISCORD_TOKEN` can be found in the Bot tab. Copy it and append to our `.env` file.
* `CHANNEL_ID` can be obtained by right-clicking the channel and selecting "Copy ID"
* `USER_ID` can be obtained by right-clicking the user and selecting "Copy ID"

### Run the script

To run the script for the bot, simply run

```bash
python3 bot.py
```

## Running the bot as a process

I use PM2 to run the bot as a process in the background.

To install PM2:

```bash
npm install -g pm2
```

In the project directory, start the bot:

```bash
pm2 start bot.py --interpreter=/usr/bin/python3
```

### Useful commands

```bash
pm2 list                list all pm2 processes
pm2 stop bot.py         stop the bot
pm2 restart bot.py      restart the bot
```

### Troubleshooting

#### ModuleNotFoundError

When starting the bot for the first time, if you get the following error:

```bash
ModuleNotFoundError: No module named 'discord'
```

Run the command:

```bash
pm2 start bot.py --interpreter python3 --interpreter-args -u
```

This will flush everything [[Stackoverflow]](<https://stackoverflow.com/a/49466103>).
