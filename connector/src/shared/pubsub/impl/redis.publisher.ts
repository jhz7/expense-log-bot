import { Redis } from "ioredis";
import { Publisher } from "../publisher.js";
import { redisConnection } from "shared/redis/index.js";

export class RedisPublisher implements Publisher {
  private readonly redis: Redis;

  constructor() {
    this.redis = redisConnection();
  }

  publish = async (topic: string, data: unknown): Promise<void> => {
    try {
      const dataAsText = JSON.stringify(data);

      console.log(
        `${this.constructor.name}: About to publish a message: subs=${topic} data=${dataAsText}`
      );

      await this.redis.publish(topic, dataAsText);
    } catch (error) {
      console.error(`${this.constructor.name}`, topic, error);

      throw error;
    }
  };
}
