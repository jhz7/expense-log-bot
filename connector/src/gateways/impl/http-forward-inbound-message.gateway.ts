import fetch from "node-fetch";
import { z } from "zod";
import {
  ForwardInboundMessageGateway,
  InboundMessage,
} from "../forward-inbound-message.gateway.js";

type RequestDto = {
  message: string;
  user_external_id: string;
};

const ResponseSchema = z.object({
  message: z.string().nullable(),
});

const BOT_SERVICE_URL = process.env.BOT_SERVICE_URL as string;

export class HttpForwardInboundMessageGateway
  implements ForwardInboundMessageGateway
{
  forward = async (message: InboundMessage): Promise<string | undefined> => {
    const response = await fetch(BOT_SERVICE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(<RequestDto>{
        message: message.content,
        user_external_id: message.userId,
      }),
    }).then((res) => res.json());

    const { message: result } = ResponseSchema.parse(response);

    return result || undefined;
  };
}
