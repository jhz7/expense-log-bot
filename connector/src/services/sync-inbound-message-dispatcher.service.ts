import {
  SyncForwardInboundMessageGateway,
  InboundMessage,
} from "gateways/sync-forward-inbound-message.gateway.js";
import {
  OutboundMessage,
  SendResponseToUserGateway,
} from "gateways/send-response-to-user.gateway.js";
import { IdGenerator } from "shared/id/id.generator.js";

export class SyncInboundMessageDispatcherService {
  constructor(
    private readonly idGenerator: IdGenerator,
    private readonly sendResponseToUser: SendResponseToUserGateway,
    private readonly forwardInboundMessage: SyncForwardInboundMessageGateway
  ) {}

  async dispatch({
    userId,
    chatId,
    content,
  }: InboundMessageService.Request): Promise<void> {
    const messageId = await this.idGenerator.get();

    const outboundContent = await this.forwardInboundMessage.forward({
      userId,
      content,
      messageId,
    });

    if (outboundContent) {
      const outboundMessage: OutboundMessage = {
        chatId,
        content: outboundContent,
      };

      return this.sendResponseToUser.send(outboundMessage);
    }
  }
}

export namespace InboundMessageService {
  export type Request = InboundMessage & {
    chatId: number;
  };
}
