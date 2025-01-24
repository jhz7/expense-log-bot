# Bot server

Acts as a proxy service forwarding inbpund message to the Bot Server and then sending its response back to the user.

## Set up

### LLM

- Once you have configured the telegram bot and already obtained the bot API key. Create the webhook [Instructions here](https://core.telegram.org/bots/api#setwebhook)

- Create a secret string. Something like a [UUID](https://www.uuidgenerator.net/) can help. This secret it's going to be sent to Telegram when creating the webhook, Telegram will send it to you on every request, so, you can validated and authorize.

  bash`curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>&secret_token=<YOUR_CREATED_SECRET>"`

- Ensure setting your Telegram Bot API key and your created secret in the .env file. Or pass this values as ENV variables directy to NodeJS when running.

### Server

- This project requires [Python](https://www.python.org/downloads/) version 3.10+ installation
- After installation. Optionally create a virtual env. Open a terminal and run

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the project dependencies

```bash
pip install -r requirements.txt
```
