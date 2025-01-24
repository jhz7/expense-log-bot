import { Router, Request, Response } from "express";
import { HttpForwardInboundMessageGateway } from "gateways/impl/http-forward-inbound-message.gateway.js";
import { HttpSendResponseToUserGateway } from "gateways/impl/http-send-response-to-user.gateway.js";
import { InboundMessageDispatcherService } from "services/inbound-message-dispatcher.service.js";
import { WebHookSchema } from "./webhook.schema.js";
import { authorizeTelegram } from "./authorize-telegram.middleware.js";
import { redisConnection } from "shared/redis/index.js";
import { RedisForwardInboundMessageGateway } from "gateways/impl/redis-forward-inbound-message.gateway.js";
import { AsyncInboundMessageDispatcherService } from "services/async-inbound-message-dispatcher.service.js";

const router = Router();

const sendBackToUser = new HttpSendResponseToUserGateway();
const forwardInboundMsg = new HttpForwardInboundMessageGateway();
const asyncForwardInboundMsg = new RedisForwardInboundMessageGateway();
const service = new InboundMessageDispatcherService(
  sendBackToUser,
  forwardInboundMsg
);

const service2 = new AsyncInboundMessageDispatcherService(
  asyncForwardInboundMsg
);

router.use(authorizeTelegram);

const read = () => {
  const conn = redisConnection();

  conn.subscribe("async-handle-inbound-message", (err, count) => {
    if (err) {
      console.error("Failed to subscribe:", err);
    } else {
      console.log(`Subscribed to ${count} Redis channels.`);
    }
  });

  conn.on("message", async (channel, message) => {
    console.log("Received channel from Bot:", channel);
    console.log("Received response from Bot:", message);
  });
};

router.post("/", async (req: Request, res: Response) => {
  try {
    const parsedMessage = WebHookSchema.parse(req.body);
    console.log("Webhook message received:", parsedMessage);

    if (parsedMessage.message) {
      await service2.dispatch({
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

read();

export default router;
