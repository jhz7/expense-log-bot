import {
  ForwardInboundMessageGateway,
  InboundMessage,
} from "gateways/forward-inbound-message.gateway.js";
import {
  OutboundMessage,
  SendResponseToUserGateway,
} from "gateways/send-response-to-user.gateway.js";

export class InboundMessageDispatcherService {
  constructor(
    private readonly sendResponseToUser: SendResponseToUserGateway,
    private readonly forwardInboundMessage: ForwardInboundMessageGateway
  ) {}

  async dispatch({
    userId,
    chatId,
    content,
  }: InboundMessageService.Request): Promise<void> {
    const outboundContent = await this.forwardInboundMessage.forward({
      userId,
      content,
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
