import { Context } from "../../deps.ts";
import { HTTPException, MiddlewareHandler } from "../../deps.ts";

export const apiKeyAuth = (options: {
  key: string;
}): MiddlewareHandler => {
  if (!options) {
    throw new Error(`apikey auth middleware requires options "key".`);
  }
  return async function apiKeyAuth(ctx: Context<Environment>, next) {
    const isValidRequest: boolean = ctx.req.header("X-API-KEY") === options.key;
    if (!isValidRequest) {
      throw new HTTPException(401, { message: "Unauthorized" });
    }
    await next();
    return;
  };
};
