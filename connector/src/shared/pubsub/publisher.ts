export interface Publisher {
  publish(topic: string, data: unknown): Promise<void>;
}
