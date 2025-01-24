import { Publisher } from "shared/pubsub/publisher.js";

export class AsyncInboundMessageDispatcherService {
  constructor(private readonly publisher: Publisher) {}

  async dispatch({
    chatId,
    content,
    userId,
  }: AsyncInboundMessageDispatcherService.Request): Promise<void> {
    await this.publisher.publish("async-handle-inbound-message", {
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
