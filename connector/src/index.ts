import fetch from 'node-fetch';

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN as string;
const BOT_SERVICE_URL = process.env.BOT_SERVICE_URL as string;
const TELEGRAM_API_URL = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}`;

interface TelegramUpdate {
  update_id: number;
  message?: {
    message_id: number;
    from: { id: number };
    chat: { id: number };
    text?: string;
  };
}

// Function to get updates from Telegram
async function getUpdates(offset: number): Promise<TelegramUpdate[]> {
  try {
    const response = await fetch(
      `${TELEGRAM_API_URL}/getUpdates?offset=${offset}`
    );
    const data = await response.json();
    console.log('response', data);
    return data.result || [];
  } catch (error) {
    console.error('Error fetching updates:', error);
    return [];
  }
}

// Function to send messages to Telegram
async function sendMessage(chatId: number, text: string) {
  try {
    await fetch(`${TELEGRAM_API_URL}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: chatId, text }),
    });
  } catch (error) {
    console.error('Error sending message:', error);
  }
}

// Function to process messages
async function processMessages() {
  let lastUpdateId = 0;

  while (true) {
    const updates = await getUpdates(lastUpdateId + 1);

    for (const update of updates) {
      if (!update.message?.text) continue;

      const chatId = update.message.chat.id;
      const text = update.message.text;

      console.log(`Received message: ${text}`);

      // Forward message to the Bot Service
      // const response = await fetch(`${BOT_SERVICE_URL}/process`, {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({ telegram_id: chatId, text }),
      // });

      // const result = await response.json();
      // await sendMessage(chatId, result.response);

      lastUpdateId = update.update_id;
    }

    await new Promise((resolve) => setTimeout(resolve, 1000)); // Poll every second
  }
}

// Start the polling process
processMessages();
