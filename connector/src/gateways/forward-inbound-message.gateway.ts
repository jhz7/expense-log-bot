export type InboundMessage = {
  userId: string;
  content: string;
};

export interface ForwardInboundMessageGateway {
  forward(message: InboundMessage): Promise<string | undefined>;
}
