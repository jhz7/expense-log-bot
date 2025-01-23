import fetch from "node-fetch";
import {
  OutboundMessage,
  SendResponseToUserGateway,
} from "gateways/send-response-to-user.gateway.js";

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN as string;
const TELEGRAM_API_URL = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}`;

export class HttpSendResponseToUserGateway
  implements SendResponseToUserGateway
{
  send = async ({ chatId, content }: OutboundMessage): Promise<void> => {
    await fetch(`${TELEGRAM_API_URL}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: chatId, text: content }),
    });
  };
}
