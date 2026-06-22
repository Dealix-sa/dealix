import { z } from "zod";
import { count, desc, eq } from "drizzle-orm";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import {
  whatsappConversations,
  whatsappMessages,
  whatsappTemplates,
} from "@db/schema";

const templateStatusSchema = z.enum(["draft", "pending", "approved", "rejected"]);
const templateCategorySchema = z.enum(["MARKETING", "UTILITY", "AUTHENTICATION"]);
const conversationStatusSchema = z.enum(["open", "resolved", "archived"]);
const messageStatusSchema = z.enum([
  "pending",
  "queued",
  "sent",
  "delivered",
  "read",
  "failed",
]);

type WhatsAppApiResponse = {
  error?: { message?: string };
  data?: Array<Record<string, unknown>>;
  messages?: Array<{ id?: string }>;
};

const WHATSAPP_ACCESS_TOKEN = process.env.WHATSAPP_ACCESS_TOKEN || "";
const WHATSAPP_PHONE_NUMBER_ID = process.env.WHATSAPP_PHONE_NUMBER_ID || "";
const WHATSAPP_WEBHOOK_VERIFY_TOKEN =
  process.env.WHATSAPP_WEBHOOK_VERIFY_TOKEN || "";
const WHATSAPP_API_VERSION = "v18.0";
const WHATSAPP_API_BASE = `https://graph.facebook.com/${WHATSAPP_API_VERSION}`;

function waHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${WHATSAPP_ACCESS_TOKEN}`,
  };
}

function toWaPhone(phone: string): string {
  let digits = phone.replace(/\D/g, "");
  if (digits.startsWith("0")) {
    digits = `966${digits.slice(1)}`;
  }
  if (!digits.startsWith("966")) {
    digits = `966${digits}`;
  }
  return digits;
}

async function waApiFetch(path: string, init: RequestInit = {}) {
  if (!WHATSAPP_ACCESS_TOKEN || !WHATSAPP_PHONE_NUMBER_ID) {
    return {
      ok: false as const,
      error: "WhatsApp Cloud API credentials are not configured",
    };
  }

  const agentMode = process.env.WHATSAPP_AGENT_MODE || "dry_run";
  if (agentMode === "dry_run") {
    return {
      ok: true as const,
      dryRun: true,
      data: {} as WhatsAppApiResponse,
    };
  }

  try {
    const response = await fetch(`${WHATSAPP_API_BASE}${path}`, {
      ...init,
      headers: waHeaders(),
    });
    const json = (await response.json()) as WhatsAppApiResponse;

    if (!response.ok) {
      return {
        ok: false as const,
        error: json.error?.message || `HTTP ${response.status}`,
        code: response.status,
      };
    }

    return { ok: true as const, data: json };
  } catch (error) {
    return { ok: false as const, error: String(error) };
  }
}

async function insertMessageDraft(params: {
  conversationId: number;
  body?: string;
  templateName?: string;
  templateVariables?: string[];
  type: "text" | "template";
  approved: boolean;
  approvedBy?: number;
}) {
  const db = getDb();
  const result = await db.insert(whatsappMessages).values({
    conversationId: params.conversationId,
    direction: "outbound",
    type: params.type,
    body: params.body,
    templateName: params.templateName,
    templateVariables: params.templateVariables ?? null,
    status: params.approved ? "queued" : "pending",
    aiGenerated: true,
    approved: params.approved,
    approvedBy: params.approvedBy,
  });

  return Number(result[0].insertId);
}

async function sendApprovedText(params: {
  messageId: number;
  to: string;
  body: string;
}) {
  const db = getDb();
  const response = await waApiFetch(`/${WHATSAPP_PHONE_NUMBER_ID}/messages`, {
    method: "POST",
    body: JSON.stringify({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to: params.to,
      type: "text",
      text: { body: params.body, preview_url: false },
    }),
  });

  if (!response.ok) {
    await db
      .update(whatsappMessages)
      .set({
        status: "failed",
        errorCode: String(response.code || "ERR"),
        errorMessage: response.error,
      })
      .where(eq(whatsappMessages.id, params.messageId));

    return { ok: false as const, error: response.error };
  }

  await db
    .update(whatsappMessages)
    .set({
      status: "sent",
      sentAt: new Date(),
      waMessageId: response.data.messages?.[0]?.id || null,
    })
    .where(eq(whatsappMessages.id, params.messageId));

  return { ok: true as const };
}

async function sendApprovedTemplate(params: {
  messageId: number;
  to: string;
  templateName: string;
  language: string;
  variables: string[];
}) {
  const db = getDb();
  const response = await waApiFetch(`/${WHATSAPP_PHONE_NUMBER_ID}/messages`, {
    method: "POST",
    body: JSON.stringify({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to: params.to,
      type: "template",
      template: {
        name: params.templateName,
        language: { code: params.language },
        ...(params.variables.length > 0
          ? {
              components: [
                {
                  type: "body",
                  parameters: params.variables.map((value) => ({
                    type: "text",
                    text: value,
                  })),
                },
              ],
            }
          : {}),
      },
    }),
  });

  if (!response.ok) {
    await db
      .update(whatsappMessages)
      .set({
        status: "failed",
        errorCode: String(response.code || "ERR"),
        errorMessage: response.error,
      })
      .where(eq(whatsappMessages.id, params.messageId));

    return { ok: false as const, error: response.error };
  }

  await db
    .update(whatsappMessages)
    .set({
      status: "sent",
      sentAt: new Date(),
      waMessageId: response.data.messages?.[0]?.id || null,
    })
    .where(eq(whatsappMessages.id, params.messageId));

  return { ok: true as const };
}

export const whatsappRouter = createRouter({
  templateList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(whatsappTemplates)
      .orderBy(desc(whatsappTemplates.createdAt))
      .limit(100);
  }),

  templateByStatus: publicQuery
    .input(z.object({ status: templateStatusSchema.default("approved") }))
    .query(async ({ input }) => {
      const db = getDb();
      return db
        .select()
        .from(whatsappTemplates)
        .where(eq(whatsappTemplates.status, input.status))
        .orderBy(desc(whatsappTemplates.createdAt))
        .limit(100);
    }),

  templateSync: publicQuery.mutation(async () => {
    const response = await waApiFetch(
      `/${WHATSAPP_PHONE_NUMBER_ID}/message_templates?limit=100`,
    );

    if (!response.ok) {
      return { ok: false, error: response.error };
    }

    const templates = response.data.data || [];
    const db = getDb();

    for (const template of templates) {
      const name = String(template.name || "");
      if (!name) {
        continue;
      }

      await db.insert(whatsappTemplates).values({
        name,
        language: String(template.language || "ar"),
        category: templateCategorySchema.parse(
          String(template.category || "MARKETING"),
        ),
        status:
          String(template.status || "").toUpperCase() === "APPROVED"
            ? "approved"
            : String(template.status || "").toUpperCase() === "REJECTED"
              ? "rejected"
              : "pending",
        content: JSON.stringify(template),
      });
    }

    return { ok: true, count: templates.length, dryRun: response.dryRun ?? false };
  }),

  templateCreate: publicQuery
    .input(
      z.object({
        name: z.string().min(2),
        content: z.string().min(3),
        language: z.string().default("ar"),
        category: templateCategorySchema.default("MARKETING"),
        header: z.string().optional(),
        footer: z.string().optional(),
      }),
    )
    .mutation(async ({ input, ctx }) => {
      const db = getDb();
      const result = await db.insert(whatsappTemplates).values({
        name: input.name,
        content: input.content,
        language: input.language,
        category: input.category,
        header: input.header,
        footer: input.footer,
        approvedBy: ctx.user?.id,
      });

      return { success: true, id: Number(result[0].insertId) };
    }),

  templateSubmit: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      await db
        .update(whatsappTemplates)
        .set({ status: "pending" })
        .where(eq(whatsappTemplates.id, input.id));
      return { success: true, submitted: true };
    }),

  conversationList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(whatsappConversations)
      .orderBy(desc(whatsappConversations.lastMessageAt))
      .limit(100);
  }),

  conversationByStatus: publicQuery
    .input(z.object({ status: conversationStatusSchema.default("open") }))
    .query(async ({ input }) => {
      const db = getDb();
      return db
        .select()
        .from(whatsappConversations)
        .where(eq(whatsappConversations.status, input.status))
        .orderBy(desc(whatsappConversations.lastMessageAt))
        .limit(100);
    }),

  conversationStats: publicQuery.query(async () => {
    const db = getDb();
    const [total, open, resolved] = await Promise.all([
      db.select({ count: count() }).from(whatsappConversations),
      db
        .select({ count: count() })
        .from(whatsappConversations)
        .where(eq(whatsappConversations.status, "open")),
      db
        .select({ count: count() })
        .from(whatsappConversations)
        .where(eq(whatsappConversations.status, "resolved")),
    ]);

    return {
      total: total[0]?.count ?? 0,
      open: open[0]?.count ?? 0,
      resolved: resolved[0]?.count ?? 0,
    };
  }),

  messageList: publicQuery
    .input(z.object({ conversationId: z.number() }))
    .query(async ({ input }) => {
      const db = getDb();
      return db
        .select()
        .from(whatsappMessages)
        .where(eq(whatsappMessages.conversationId, input.conversationId))
        .orderBy(desc(whatsappMessages.createdAt))
        .limit(200);
    }),

  messageStats: publicQuery.query(async () => {
    const db = getDb();
    const [total, inbound, outbound, sent, pending, failed] = await Promise.all([
      db.select({ count: count() }).from(whatsappMessages),
      db
        .select({ count: count() })
        .from(whatsappMessages)
        .where(eq(whatsappMessages.direction, "inbound")),
      db
        .select({ count: count() })
        .from(whatsappMessages)
        .where(eq(whatsappMessages.direction, "outbound")),
      db
        .select({ count: count() })
        .from(whatsappMessages)
        .where(eq(whatsappMessages.status, "sent")),
      db
        .select({ count: count() })
        .from(whatsappMessages)
        .where(eq(whatsappMessages.status, "pending")),
      db
        .select({ count: count() })
        .from(whatsappMessages)
        .where(eq(whatsappMessages.status, "failed")),
    ]);

    return {
      total: total[0]?.count ?? 0,
      inbound: inbound[0]?.count ?? 0,
      outbound: outbound[0]?.count ?? 0,
      sent: sent[0]?.count ?? 0,
      pending: pending[0]?.count ?? 0,
      failed: failed[0]?.count ?? 0,
    };
  }),

  sendText: publicQuery
    .input(
      z.object({
        conversationId: z.number(),
        to: z.string().min(8),
        body: z.string().min(1),
      }),
    )
    .mutation(async ({ input }) => {
      const messageId = await insertMessageDraft({
        conversationId: input.conversationId,
        body: input.body,
        type: "text",
        approved: false,
      });

      return {
        ok: true,
        pending: true,
        messageId,
        to: toWaPhone(input.to),
      };
    }),

  sendTemplate: publicQuery
    .input(
      z.object({
        conversationId: z.number(),
        to: z.string().min(8),
        templateName: z.string().min(2),
        language: z.string().default("ar"),
        variables: z.array(z.string()).default([]),
      }),
    )
    .mutation(async ({ input }) => {
      const messageId = await insertMessageDraft({
        conversationId: input.conversationId,
        templateName: input.templateName,
        templateVariables: input.variables,
        type: "template",
        approved: false,
      });

      return {
        ok: true,
        pending: true,
        messageId,
        to: toWaPhone(input.to),
      };
    }),

  approveMessage: publicQuery
    .input(
      z.object({
        messageId: z.number(),
        to: z.string().min(8),
        language: z.string().default("ar"),
      }),
    )
    .mutation(async ({ input, ctx }) => {
      const db = getDb();
      const rows = await db
        .select()
        .from(whatsappMessages)
        .where(eq(whatsappMessages.id, input.messageId));

      if (!rows.length) {
        return { ok: false, error: "Message not found" };
      }

      const message = rows[0];
      await db
        .update(whatsappMessages)
        .set({
          approved: true,
          approvedBy: ctx.user?.id,
          status: "queued",
        })
        .where(eq(whatsappMessages.id, input.messageId));

      if (message.type === "text" && message.body) {
        return sendApprovedText({
          messageId: input.messageId,
          to: toWaPhone(input.to),
          body: message.body,
        });
      }

      if (message.type === "template" && message.templateName) {
        return sendApprovedTemplate({
          messageId: input.messageId,
          to: toWaPhone(input.to),
          templateName: message.templateName,
          language: input.language,
          variables: Array.isArray(message.templateVariables)
            ? message.templateVariables.map((value) => String(value))
            : [],
        });
      }

      return { ok: true, approved: true };
    }),

  rejectMessage: publicQuery
    .input(z.object({ messageId: z.number() }))
    .mutation(async ({ input, ctx }) => {
      const db = getDb();
      await db
        .update(whatsappMessages)
        .set({
          approved: false,
          approvedBy: ctx.user?.id,
          status: "failed",
          errorCode: "REJECTED",
          errorMessage: "Message rejected by reviewer",
        })
        .where(eq(whatsappMessages.id, input.messageId));

      return { ok: true, rejected: true };
    }),

  health: publicQuery.query(() => {
    const mode = process.env.WHATSAPP_AGENT_MODE || "dry_run";
    return {
      configured: Boolean(WHATSAPP_ACCESS_TOKEN && WHATSAPP_PHONE_NUMBER_ID),
      mode,
      verifyTokenConfigured: Boolean(WHATSAPP_WEBHOOK_VERIFY_TOKEN),
      status:
        WHATSAPP_ACCESS_TOKEN && WHATSAPP_PHONE_NUMBER_ID
          ? "Ready"
          : "Not Configured",
    };
  }),

  verifyWebhook: publicQuery
    .input(
      z.object({
        mode: z.string(),
        verifyToken: z.string(),
        challenge: z.string(),
      }),
    )
    .query(({ input }) => {
      const verified =
        input.mode === "subscribe" &&
        input.verifyToken === WHATSAPP_WEBHOOK_VERIFY_TOKEN;

      return {
        ok: verified,
        challenge: verified ? input.challenge : null,
      };
    }),

  receiveWebhook: publicQuery
    .input(z.object({ body: z.any() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const changes = input.body?.entry?.[0]?.changes?.[0]?.value;
      const messages = changes?.messages as
        | Array<Record<string, unknown>>
        | undefined;
      const statuses = changes?.statuses as
        | Array<Record<string, unknown>>
        | undefined;

      if (Array.isArray(messages)) {
        for (const incoming of messages) {
          const waId = String(incoming.from || "");
          const body =
            String(
              (incoming.text as { body?: string } | undefined)?.body ||
                (incoming.button as { text?: string } | undefined)?.text ||
                "",
            ) || "";

          const existingConversation = await db
            .select()
            .from(whatsappConversations)
            .where(eq(whatsappConversations.waId, waId));

          let conversationId = existingConversation[0]?.id;
          if (!conversationId) {
            const created = await db.insert(whatsappConversations).values({
              waId,
              name: waId,
              lastMessageAt: new Date(),
              lastMessageDirection: "inbound",
              lastMessageBody: body,
              status: "open",
            });
            conversationId = Number(created[0].insertId);
          } else {
            await db
              .update(whatsappConversations)
              .set({
                lastMessageAt: new Date(),
                lastMessageDirection: "inbound",
                lastMessageBody: body,
              })
              .where(eq(whatsappConversations.id, conversationId));
          }

          await db.insert(whatsappMessages).values({
            conversationId,
            waMessageId: String(incoming.id || ""),
            direction: "inbound",
            type: "text",
            body,
            status: "delivered",
            sentAt: new Date(),
          });
        }
      }

      if (Array.isArray(statuses)) {
        for (const statusEntry of statuses) {
          const waMessageId = String(statusEntry.id || "");
          const status = String(statusEntry.status || "");
          const nextStatus = messageStatusSchema.safeParse(status);

          if (!waMessageId || !nextStatus.success) {
            continue;
          }

          await db
            .update(whatsappMessages)
            .set({
              status: nextStatus.data,
              ...(nextStatus.data === "delivered"
                ? { deliveredAt: new Date() }
                : {}),
              ...(nextStatus.data === "read" ? { readAt: new Date() } : {}),
            })
            .where(eq(whatsappMessages.waMessageId, waMessageId));
        }
      }

      return {
        ok: true,
        receivedMessages: Array.isArray(messages) ? messages.length : 0,
        receivedStatuses: Array.isArray(statuses) ? statuses.length : 0,
      };
    }),
});