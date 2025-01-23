import { Request, Response, NextFunction } from "express";
import { z } from "zod";

const TELEGRAM_SECRET_TOKEN = process.env.TELEGRAM_SECRET_TOKEN;

export const WebHookSchema = z.object({
  message: z
    .object({
      from: z.object({
        is_bot: z.boolean(),
      }),
    })
    .optional(),
});

export const authorizeTelegram = (
  request: Request,
  response: Response,
  next: NextFunction
): void => {
  const secret = request.headers["x-telegram-bot-api-secret-token"];
  const isTheConfiguredTelegramSecret =
    !!TELEGRAM_SECRET_TOKEN && TELEGRAM_SECRET_TOKEN === secret;

  if (!isTheConfiguredTelegramSecret) {
    console.warn("Unauthorized webhook request: Invalid secret token");
    response.status(403).json({ error: "Forbidden" });
    return;
  }

  const parsedRequest = WebHookSchema.safeParse(request.body);

  if (!parsedRequest.success) {
    console.error(parsedRequest.error);
    return;
  }

  const isABot = !!parsedRequest.data.message?.from.is_bot;

  if (isABot) {
    console.warn("Unauthorized webhook request: Bot request");
    response.status(403).json({ error: "Forbidden" });
    return;
  }

  next();
};
