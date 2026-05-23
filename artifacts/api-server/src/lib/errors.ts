export class HttpError extends Error {
  public readonly status: number;
  public readonly code: string;
  public readonly details?: unknown;

  constructor(
    status: number,
    code: string,
    message: string,
    details?: unknown,
  ) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

export const badRequest = (msg = "Bad request", details?: unknown) =>
  new HttpError(400, "bad_request", msg, details);

export const unauthorized = (msg = "Unauthorized") =>
  new HttpError(401, "unauthorized", msg);

export const forbidden = (msg = "Forbidden") =>
  new HttpError(403, "forbidden", msg);

export const notFound = (msg = "Not found") =>
  new HttpError(404, "not_found", msg);

export const conflict = (msg = "Conflict") =>
  new HttpError(409, "conflict", msg);

export const tooManyRequests = (msg = "Too many requests") =>
  new HttpError(429, "rate_limited", msg);

export const internal = (msg = "Internal server error", details?: unknown) =>
  new HttpError(500, "internal_error", msg, details);
