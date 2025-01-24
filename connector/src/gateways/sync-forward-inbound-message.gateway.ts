export type InboundMessage = {
  userId: string;
  content: string;
};

export interface SyncForwardInboundMessageGateway {
  forward(message: InboundMessage): Promise<string | undefined>;
}
