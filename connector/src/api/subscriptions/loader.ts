import { HttpSendResponseToUserGateway } from "gateways/impl/http-send-response-to-user.gateway.js";
import { RedisSubscriber } from "shared/pubsub/impl/redis.subscriber.js";
import { OutboundMessageSubscriber } from "./outbound-message.subscriber.js";

const baseSubscriber = new RedisSubscriber();
const outboundMessageSender = new HttpSendResponseToUserGateway();

const subscriber = new OutboundMessageSubscriber(
  baseSubscriber,
  outboundMessageSender
);

setImmediate(() => subscriber.run());
