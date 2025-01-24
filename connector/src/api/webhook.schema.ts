import { z } from "zod";

export const WebHookSchema = z.object({
  message: z
    .object({
      message_id: z.number(),
      from: z.object({
        id: z.number(),
        first_name: z.string(),
        last_name: z.string(),
        is_bot: z.boolean(),
      }),
      chat: z.object({
        id: z.number(),
      }),
      date: z.number(),
      text: z.string().max(200),
    })
    .optional(),
});
