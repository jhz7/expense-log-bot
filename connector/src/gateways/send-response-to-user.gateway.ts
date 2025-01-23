export type OutboundMessage = {
  chatId: number;
  content: string;
};

export interface SendResponseToUserGateway {
  send(message: OutboundMessage): Promise<void>;
}
