import { Router, Request, Response } from "express";
import { HttpForwardInboundMessageGateway } from "gateways/impl/http-forward-inbound-message.gateway.js";
import { HttpSendResponseToUserGateway } from "gateways/impl/http-send-response-to-user.gateway.js";
import { InboundMessageDispatcherService } from "services/inbound-message-dispatcher.service.js";
import { WebHookSchema } from "./webhook.schema.js";
import { authorizeTelegram } from "./authorize-telegram.middleware.js";

const router = Router();

const sendBackToUser = new HttpSendResponseToUserGateway();
const forwardInboundMsg = new HttpForwardInboundMessageGateway();
const service = new InboundMessageDispatcherService(
  sendBackToUser,
  forwardInboundMsg
);

router.use(authorizeTelegram);

router.post("/", async (req: Request, res: Response) => {
  try {
    const parsedMessage = WebHookSchema.parse(req.body.message);

    if (parsedMessage.message) {
      setImmediate
      await service.dispatch({
        chatId: parsedMessage.message.chat.id,
        content: parsedMessage.message.text,
        userId: `${parsedMessage.message.from.id}`,
      });
    }
  } catch (error) {
    console.error("Error dispatching message:", error);
  } finally {
    res.sendStatus(204);
  }
});

export default router;
