import { Router, Request, Response } from "express";
import { WebHookSchema } from "./webhook.schema.js";
import { authorizeTelegram } from "./authorize-telegram.middleware.js";
import { AsyncInboundMessageDispatcherService } from "services/async-inbound-message-dispatcher.service.js";
import { RedisPublisher } from "shared/pubsub/impl/redis.publisher.js";
import { UlidIdGenerator } from "shared/id/impl/ulid-id.generator.js";

const router = Router();

const publisher = new RedisPublisher();
const idGenerator = new UlidIdGenerator();

const service = new AsyncInboundMessageDispatcherService(
  publisher,
  idGenerator
);

router.use(authorizeTelegram);

router.post("/", async (req: Request, res: Response) => {
  try {
    const parsedMessage = WebHookSchema.parse(req.body);
    console.log("Webhook message received:", parsedMessage);

    if (parsedMessage.message) {
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
