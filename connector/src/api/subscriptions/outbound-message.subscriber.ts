import { SendResponseToUserGateway } from "gateways/send-response-to-user.gateway.js";
import { Subscriber } from "shared/pubsub/subscriber.js";
import { z } from "zod";

const Schema = z.object({
  chatId: z.number(),
  message: z.string(),
});

export class OutboundMessageSubscriber {
  constructor(
    private readonly subscriber: Subscriber,
    private readonly sendUserResponse: SendResponseToUserGateway
  ) {}

  run = async (): Promise<void> => {
    await this.subscriber.subscribe("async-handle-outbound-message", (data) =>
      this.messageHandler(data)
    );
  };

  private messageHandler = async (data: string): Promise<void> => {
    const validatedData = Schema.safeParse(JSON.parse(data));

    if (!validatedData.success) {
      console.error(
        `${this.constructor.name}: Invalid message received`,
        validatedData.error
      );
      return;
    }

    const { chatId, message } = validatedData.data;

    await this.sendUserResponse.send({ chatId, content: message });
  };
}
