import { Redis } from "ioredis";

const REDIS_PORT = process.env.REDIS_PORT;
const REDIS_PASSWORD = process.env.REDIS_PASSWORD;
const REDIS_HOST = process.env.REDIS_HOST;

if (!REDIS_PASSWORD || !REDIS_PORT || !REDIS_HOST) {
  throw new Error("Redis configuration could not be determine");
}

const redisConnection = () =>
  new Redis(Number(REDIS_PORT), REDIS_HOST, {
    password: REDIS_PASSWORD,
    maxRetriesPerRequest: 10,
  });

export { redisConnection };
