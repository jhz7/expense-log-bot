export interface Subscriber {
  subscribe(
    subscription: string,
    onMessage: (data: string) => Promise<void>
  ): Promise<void>;
}
