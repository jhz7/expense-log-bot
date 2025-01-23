import { z } from "zod";
import { Router } from "express";
import { HttpForwardInboundMessageGateway } from "gateways/impl/http-forward-inbound-message.gateway.js";
import { HttpSendResponseToUserGateway } from "gateways/impl/http-send-response-to-user.gateway.js";
import { InboundMessageDispatcherService } from "services/inbound-message-dispatcher.service.js";

const router = Router();

const WebHookSchema = z
  .object({
    message_id: z.number(),
    from: z.object({
      id: z.number(),
      first_name: z.string(),
      last_name: z.string(),
      is_bot: z.boolean(),
    }),
    chat: z.object({
      id: z.number(),
    }),
    date: z.number(),
    text: z.string(),
  })
  .optional();

const sendBackToUser = new HttpSendResponseToUserGateway();
const forwardInboundMsg = new HttpForwardInboundMessageGateway();

const service = new InboundMessageDispatcherService(
  sendBackToUser,
  forwardInboundMsg
);

router.post("/", async (req, res) => {
  const message = req.body.message;
  console.log("Received message:", message);

  try {
    const parsedMessage = WebHookSchema.parse(message);

    if (parsedMessage) {
      await service.dispatch({
        chatId: parsedMessage.chat.id,
        userId: parsedMessage.from.id.toString(),
        content: parsedMessage.text,
      });
    }
  } catch (error) {
    console.error("Error dispatching message:", error);
  }
  res.sendStatus(200);
});

export default router;
