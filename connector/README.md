# Connector server

Acts as a proxy service forwarding inbpund message to the Bot Server and then, sending its response back to the user.

## Set up

### Telegram webhook

- Create a secret string. Something like a [UUID](https://www.uuidgenerator.net/) can help. This secret it's going to be sent to Telegram when creating the webhook, Telegram will send it to you on every request, so, you can validated and authorize.

- Use ngrok or other equivalent to expose your Connector server on the web. This step is necessary in order to configure a webhook in Telegram

```bash
ngrok http localhost:3000
```

- Once you have configured the telegram bot and already obtained the bot API key. Create the webhook [Instructions here](https://core.telegram.org/bots/api#setwebhook)

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TELEGRAM_BOT_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>&secret_token=<YOUR_CREATED_SECRET>"
```

- Ensure setting your Telegram Bot API key and your created secret in the .env file. Or pass this values as ENV variables directy to NodeJS when running.

### Server

For local code adjustments

- This project requires [NodeJS](https://nodejs.org/en) version 22 installation

- After installing. Open a terminal in the connector folder and execute

```bash
npm install
```

- Set your Bot Server URL (local or production ready based on your running environment) in the .env file.

## GOTO

[Bot service](../bot/README.md)
