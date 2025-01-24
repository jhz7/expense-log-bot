export type InboundMessage = {
  messageId: string;
  userId: string;
  content: string;
};

export interface SyncForwardInboundMessageGateway {
  forward(message: InboundMessage): Promise<string | undefined>;
}
