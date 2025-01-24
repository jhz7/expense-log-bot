import { Publisher } from "shared/pubsub/publisher.js";

const INBOUND_MSG_SUB = process.env.INBOUND_MSG_SUB;

if (!INBOUND_MSG_SUB) {
  throw new Error("INBOUND_MSG_SUB env varibale is required");
}

export class AsyncInboundMessageDispatcherService {
  constructor(private readonly publisher: Publisher) {}

  async dispatch({
    chatId,
    content,
    userId,
  }: AsyncInboundMessageDispatcherService.Request): Promise<void> {
    await this.publisher.publish(INBOUND_MSG_SUB!, {
      chat_id: chatId,
      message: content,
      user_external_id: userId,
    });
  }
}

export namespace AsyncInboundMessageDispatcherService {
  export type Request = {
    chatId: number;
    userId: string;
    content: string;
  };
}
