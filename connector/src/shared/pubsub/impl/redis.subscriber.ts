import { Redis } from "ioredis";
import { redisConnection } from "shared/redis/index.js";
import { Subscriber } from "../subscriber.js";

export class RedisSubscriber implements Subscriber {
  private readonly redis: Redis;

  constructor() {
    this.redis = redisConnection();
  }

  subscribe = async (
    subscription: string,
    onMessage: (data: string) => Promise<void>
  ): Promise<void> => {
    try {
      await this.redis.subscribe(subscription, (err, count) => {
        if (err) {
          console.error(`${this.constructor.name}`, subscription, err);
        } else {
          console.log(
            `${this.constructor.name}: Subscribed to ${count} Redis channels. subs=${subscription}`
          );
        }
      });

      this.redis.on("message", async (channel, message) => {
        if (channel === subscription) {
          console.log(
            `${this.constructor.name}: About to process a message: subs=${subscription} data=${message}`
          );

          await onMessage(message);
        }
      });
    } catch (error) {
      console.error(`${this.constructor.name}`, subscription, error);

      throw error;
    }
  };
}
