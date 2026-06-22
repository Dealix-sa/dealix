import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  ClipboardCheck,
  FileCheck,
  Mail,
  MessageSquare,
  Phone,
  Plus,
  Send,
  ShieldCheck,
  Target,
  X,
} from "lucide-react";

const stageLabels: Record<string, string> = {
  target: "Target",
  researched: "Researched",
  contacted: "Contacted",
  replied: "Replied",
  discovery_booked: "Discovery Booked",
  proposal_sent: "Proposal Sent",
  won: "Won",
  delivery: "Delivery",
  retainer: "Retainer",
  lost: "Lost",
};

export default function CommandRoom() {
  const utils = trpc.useUtils();
  const drafts = trpc.commandRoom.draftList.useQuery();
  const stats = trpc.commandRoom.draftStats.useQuery();
  const pipeline = trpc.commandRoom.pipelineByStage.useQuery();
  const topOpportunities = trpc.commandRoom.topOpportunities.useQuery();
  const whatsappOverview = trpc.commandRoom.whatsappOverview.useQuery();
  const whatsappHealth = trpc.whatsapp.health.useQuery();
  const whatsappConversations = trpc.whatsapp.conversationList.useQuery();
  const whatsappMessageStats = trpc.whatsapp.messageStats.useQuery();
  const whatsappTemplates = trpc.whatsapp.templateList.useQuery();

  // WhatsApp UI state
  const [expandedConversation, setExpandedConversation] = useState<number | null>(null);
  const [newMessage, setNewMessage] = useState("");
  const [showNewMessageForm, setShowNewMessageForm] = useState<number | null>(null);

  // Fetch messages when conversation is expanded
  const conversationMessages = trpc.whatsapp.messageList.useQuery(
    { conversationId: expandedConversation ?? 0 },
    { enabled: expandedConversation !== null }
  );

  // WhatsApp mutations
  const sendText = trpc.whatsapp.sendText.useMutation({
    onSuccess: () => {
      utils.whatsapp.conversationList.invalidate();
      utils.whatsapp.messageList.invalidate();
      utils.whatsapp.messageStats.invalidate();
      utils.commandRoom.whatsappOverview.invalidate();
      setNewMessage("");
      setShowNewMessageForm(null);
    },
  });

  const approveMessage = trpc.whatsapp.approveMessage.useMutation({
    onSuccess: () => {
      utils.whatsapp.messageList.invalidate();
      utils.whatsapp.messageStats.invalidate();
    },
  });

  const rejectMessage = trpc.whatsapp.rejectMessage.useMutation({
    onSuccess: () => {
      utils.whatsapp.messageList.invalidate();
      utils.whatsapp.messageStats.invalidate();
    },
  });

  const approveDraft = trpc.commandRoom.approveDraft.useMutation({
    onSuccess: () => {
      utils.commandRoom.draftList.invalidate();
      utils.commandRoom.draftStats.invalidate();
    },
  });

  const rejectDraft = trpc.commandRoom.rejectDraft.useMutation({
    onSuccess: () => {
      utils.commandRoom.draftList.invalidate();
      utils.commandRoom.draftStats.invalidate();
    },
  });

  const typeIcon = (type: string) => {
    if (type === "email") return <Mail className="h-4 w-4" />;
    if (type === "whatsapp") return <MessageSquare className="h-4 w-4" />;
    if (type === "linkedin") return <FileCheck className="h-4 w-4" />;
    return <Send className="h-4 w-4" />;
  };

  const priorityColor = (priority: number) => {
    if (priority >= 8) return "bg-red-100 text-red-700";
    if (priority >= 6) return "bg-amber-100 text-amber-700";
    if (priority >= 4) return "bg-blue-100 text-blue-700";
    return "bg-slate-100 text-slate-700";
  };

  const messageStatusBadge = (status: string) => {
    const map: Record<string, string> = {
      pending: "bg-yellow-100 text-yellow-700",
      queued: "bg-blue-100 text-blue-700",
      sent: "bg-green-100 text-green-700",
      delivered: "bg-emerald-100 text-emerald-700",
      read: "bg-purple-100 text-purple-700",
      failed: "bg-red-100 text-red-700",
    };
    return map[status] || "bg-slate-100 text-slate-700";
  };

  const handleSendMessage = (conversationId: number, waId: string) => {
    if (!newMessage.trim()) return;
    sendText.mutate({
      conversationId,
      to: waId,
      body: newMessage,
    });
  };

  return (
    <div className="min-h-screen bg-[#F0F9F8] p-6" dir="rtl">
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#15807A]">
              <BarChart3 className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#0A1F1E]">
                Revenue Command Room
              </h1>
              <p className="text-sm text-[#4A6B69]">
                غرفة قيادة يومية للمؤسس: follow-ups، approvals، pipeline،
                وWhatsApp الرسمي.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <Badge
              variant="outline"
              className="border-[#15807A] text-[#15807A]"
            >
              <ClipboardCheck className="ml-1 h-3 w-3" />
              OUTBOUND_MODE: draft_only
            </Badge>
            <Badge variant="outline" className="border-slate-300 text-slate-600">
              <ShieldCheck className="ml-1 h-3 w-3" />
              Human approval required
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {[
            { label: "Drafts", value: stats.data?.total ?? 0 },
            { label: "Pending Approval", value: stats.data?.pending ?? 0 },
            { label: "Approved", value: stats.data?.approved ?? 0 },
            { label: "Sent", value: stats.data?.sent ?? 0 },
          ].map((item) => (
            <Card key={item.label} className="border-[#E8F4F3] bg-white">
              <CardContent className="p-4">
                <p className="text-xs text-[#4A6B69]">{item.label}</p>
                <p className="mt-1 text-2xl font-bold text-[#0A1F1E]">
                  {item.value}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-4 md:grid-cols-5">
          {[
            {
              label: "WA Conversations",
              value: whatsappOverview.data?.conversations ?? 0,
            },
            {
              label: "WA Open",
              value: whatsappOverview.data?.openConversations ?? 0,
            },
            {
              label: "WA Messages",
              value: whatsappMessageStats.data?.total ?? 0,
            },
            {
              label: "WA Pending",
              value: whatsappOverview.data?.pendingMessages ?? 0,
            },
            {
              label: "WA Templates",
              value: whatsappOverview.data?.templates ?? 0,
            },
          ].map((item) => (
            <Card key={item.label} className="border-[#E8F4F3] bg-white">
              <CardContent className="p-4">
                <p className="text-xs text-[#4A6B69]">{item.label}</p>
                <p className="mt-1 text-2xl font-bold text-[#0A1F1E]">
                  {item.value}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <Send className="h-4 w-4 text-[#15807A]" />
                  Approval Queue
                </CardTitle>
                <CardDescription>
                  كل draft في هذه القائمة يحتاج approve أو reject قبل أي إرسال
                  فعلي.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {drafts.data?.slice(0, 10).map((draft) => (
                  <div
                    key={draft.id}
                    className={`rounded-xl border p-4 ${
                      draft.approved
                        ? "border-green-200 bg-green-50"
                        : "border-[#E8F4F3] bg-[#F0F9F8]"
                    }`}
                  >
                    <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                      <div className="space-y-2">
                        <div className="flex flex-wrap items-center gap-2">
                          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white shadow-sm">
                            {typeIcon(draft.type)}
                          </div>
                          <span className="text-sm font-bold text-[#0A1F1E]">
                            Draft #{draft.id}
                          </span>
                          <span className="text-xs text-[#8CB3B0]">
                            Prospect ID: {draft.prospectId ?? "unlinked"}
                          </span>
                          <Badge
                            className={`${priorityColor(
                              draft.priority,
                            )} border-0 text-[10px]`}
                          >
                            P{draft.priority}
                          </Badge>
                        </div>

                        {draft.contentAr && (
                          <pre className="whitespace-pre-wrap rounded-lg border border-[#E8F4F3] bg-white p-3 font-sans text-xs text-[#0A1F1E]">
                            {draft.contentAr}
                          </pre>
                        )}

                        {draft.contentEn && (
                          <pre className="whitespace-pre-wrap rounded-lg border border-[#E8F4F3] bg-white p-3 font-sans text-xs text-[#4A6B69]">
                            {draft.contentEn}
                          </pre>
                        )}

                        <div className="flex flex-wrap gap-2 text-xs text-[#8CB3B0]">
                          <span className="rounded bg-[#E8F4F3] px-2 py-1">
                            [AI]
                          </span>
                          <span className="rounded bg-white px-2 py-1">
                            {draft.outboundMode || "draft_only"}
                          </span>
                          <span className="rounded bg-white px-2 py-1">
                            {draft.recommendedSendDate || "Today"}
                          </span>
                        </div>
                      </div>

                      <div className="flex flex-wrap gap-2">
                        {!draft.approved && (
                          <Button
                            size="sm"
                            variant="outline"
                            className="border-green-200 text-green-700 hover:bg-green-50"
                            onClick={() => approveDraft.mutate({ id: draft.id })}
                          >
                            <CheckCircle2 className="ml-1 h-3 w-3" />
                            موافقة
                          </Button>
                        )}
                        {!draft.approved && (
                          <Button
                            size="sm"
                            variant="outline"
                            className="border-red-200 text-red-700 hover:bg-red-50"
                            onClick={() => rejectDraft.mutate({ id: draft.id })}
                          >
                            Reject
                          </Button>
                        )}
                        {draft.approved && !draft.sent && (
                          <Badge className="border-0 bg-green-100 text-green-700">
                            Approved
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                ))}

                {(!drafts.data || drafts.data.length === 0) && (
                  <div className="rounded-xl border border-dashed border-[#D7E9E7] bg-[#F8FBFB] p-8 text-center text-sm text-[#8CB3B0]">
                    لا توجد drafts بانتظار المراجعة الآن.
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <MessageSquare className="h-4 w-4 text-[#15807A]" />
                  WhatsApp Inbox
                </CardTitle>
                <CardDescription>
                  محادثات القناة الرسمية — انقر على محادثة لعرض الرسائل وإرسال/الموافقة على رسائل.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {whatsappConversations.data?.slice(0, 8).map((conversation) => (
                  <div
                    key={conversation.id}
                    className="rounded-xl border border-[#E8F4F3] bg-[#F0F9F8] overflow-hidden"
                  >
                    {/* Conversation Header */}
                    <div
                      className="flex items-center justify-between p-4 cursor-pointer hover:bg-[#E8F4F3] transition-colors"
                      onClick={() =>
                        setExpandedConversation(
                          expandedConversation === conversation.id ? null : conversation.id
                        )
                      }
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#15807A] text-white">
                          <Phone className="h-4 w-4" />
                        </div>
                        <div>
                          <p className="text-sm font-bold text-[#0A1F1E]">
                            {conversation.name || conversation.waId}
                          </p>
                          <p className="text-xs text-[#4A6B69]">
                            {conversation.waId}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className="border-0 bg-[#15807A] text-[10px] text-white">
                          {conversation.status}
                        </Badge>
                        {expandedConversation === conversation.id ? (
                          <ChevronUp className="h-4 w-4 text-[#4A6B69]" />
                        ) : (
                          <ChevronDown className="h-4 w-4 text-[#4A6B69]" />
                        )}
                      </div>
                    </div>

                    {/* Last Message Preview */}
                    <div className="px-4 pb-2">
                      <p className="text-xs text-[#4A6B69] line-clamp-1">
                        {conversation.lastMessageBody || "لا توجد رسائل"}
                      </p>
                    </div>

                    {/* Expanded Messages View */}
                    {expandedConversation === conversation.id && (
                      <div className="border-t border-[#E8F4F3] bg-white">
                        {/* Messages List */}
                        <div className="max-h-64 overflow-y-auto p-3 space-y-2">
                          {conversationMessages.isLoading && (
                            <p className="text-xs text-[#8CB3B0] text-center py-2">جاري التحميل...</p>
                          )}
                          {conversationMessages.data?.length === 0 && (
                            <p className="text-xs text-[#8CB3B0] text-center py-2">لا توجد رسائل في هذه المحادثة</p>
                          )}
                          {conversationMessages.data?.map((msg) => (
                            <div
                              key={msg.id}
                              className={`rounded-lg p-2 text-xs ${
                                msg.direction === "inbound"
                                  ? "bg-[#F0F9F8] mr-4"
                                  : "bg-[#15807A]/10 ml-4"
                              }`}
                            >
                              <div className="flex items-center justify-between gap-2 mb-1">
                                <Badge className={`${messageStatusBadge(msg.status)} border-0 text-[8px]`}>
                                  {msg.direction === "inbound" ? "وارد" : "صادر"}
                                </Badge>
                                <Badge className={`${messageStatusBadge(msg.status)} border-0 text-[8px]`}>
                                  {msg.status}
                                </Badge>
                                {msg.aiGenerated && (
                                  <Badge className="bg-purple-100 text-purple-700 border-0 text-[8px]">AI</Badge>
                                )}
                              </div>
                              <p className="text-[#0A1F1E]">{msg.body || msg.templateName || "—"}</p>
                              <p className="text-[10px] text-[#8CB3B0] mt-1">
                                {msg.createdAt ? new Date(msg.createdAt).toLocaleString("ar-SA") : ""}
                              </p>

                              {/* Message Actions - for pending outbound messages */}
                              {msg.direction === "outbound" && msg.status === "pending" && !msg.approved && (
                                <div className="flex gap-1 mt-2">
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    className="h-6 text-[10px] border-green-200 text-green-700 hover:bg-green-50"
                                    onClick={() => approveMessage.mutate({ messageId: msg.id, to: msg.waMessageId || conversation.waId })}
                                  >
                                    <CheckCircle2 className="h-3 w-3 ml-1" />
                                    موافقة
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    className="h-6 text-[10px] border-red-200 text-red-700 hover:bg-red-50"
                                    onClick={() => rejectMessage.mutate({ messageId: msg.id })}
                                  >
                                    <X className="h-3 w-3 ml-1" />
                                    رفض
                                  </Button>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>

                        {/* Quick Reply / New Message Form */}
                        {showNewMessageForm === conversation.id ? (
                          <div className="border-t border-[#E8F4F3] p-3 space-y-2">
                            <Textarea
                              className="min-h-[80px] text-sm border-[#E8F4F3]"
                              placeholder="اكتب رسالتك هنا..."
                              value={newMessage}
                              onChange={(e) => setNewMessage(e.target.value)}
                            />
                            <div className="flex gap-2">
                              <Button
                                size="sm"
                                className="bg-[#15807A] hover:bg-[#0F5F5A]"
                                onClick={() => handleSendMessage(conversation.id, conversation.waId)}
                                disabled={sendText.isPending || !newMessage.trim()}
                              >
                                <Send className="h-3 w-3 ml-1" />
                                {sendText.isPending ? "جاري..." : "إرسال"}
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => {
                                  setShowNewMessageForm(null);
                                  setNewMessage("");
                                }}
                              >
                                إلغاء
                              </Button>
                            </div>
                          </div>
                        ) : (
                          <div className="border-t border-[#E8F4F3] p-2">
                            <Button
                              size="sm"
                              variant="outline"
                              className="w-full border-[#15807A]/30 text-[#15807A] hover:bg-[#15807A]/10"
                              onClick={() => setShowNewMessageForm(conversation.id)}
                            >
                              <Plus className="h-3 w-3 ml-1" />
                              رسالة جديدة
                            </Button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}

                {(!whatsappConversations.data ||
                  whatsappConversations.data.length === 0) && (
                  <div className="rounded-xl border border-dashed border-[#D7E9E7] bg-[#F8FBFB] p-8 text-center text-sm text-[#8CB3B0]">
                    لا توجد محادثات WhatsApp حتى الآن.
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="text-[#0A1F1E]">
                  Founder Daily Actions
                </CardTitle>
                <CardDescription>
                  الإجراءات المقترحة اليوم لتقليل التسرب وتحريك الصفقات.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-[#4A6B69]">
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  1. راجع drafts ذات الأولوية العالية أولًا.
                </div>
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  2. تابع محادثات WhatsApp المفتوحة التي لم تُغلق بعد.
                </div>
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  3. راقب مراحل pipeline ذات الاختناق الأكبر.
                </div>
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  4. انقل الصفقات القريبة من discovery إلى proposal بسرعة.
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <MessageSquare className="h-4 w-4 text-[#15807A]" />
                  WhatsApp Channel Health
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex items-center justify-between rounded bg-[#F0F9F8] p-2 text-xs">
                  <span>Configured</span>
                  <Badge
                    className={`${
                      whatsappHealth.data?.configured
                        ? "bg-green-100 text-green-700"
                        : "bg-red-100 text-red-700"
                    } border-0 text-[10px]`}
                  >
                    {whatsappHealth.data?.configured ? "yes" : "no"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between rounded bg-[#F0F9F8] p-2 text-xs">
                  <span>Mode</span>
                  <Badge className="border-0 bg-amber-100 text-[10px] text-amber-700">
                    {whatsappHealth.data?.mode ?? "dry_run"}
                  </Badge>
                </div>
                <div className="flex items-center justify-between rounded bg-[#F0F9F8] p-2 text-xs">
                  <span>Templates</span>
                  <Badge className="border-0 bg-[#15807A] text-[10px] text-white">
                    {whatsappTemplates.data?.length ?? 0}
                  </Badge>
                </div>
                <div className="flex items-center justify-between rounded bg-[#F0F9F8] p-2 text-xs">
                  <span>Pending messages</span>
                  <Badge className="border-0 bg-indigo-100 text-[10px] text-indigo-700">
                    {whatsappMessageStats.data?.pending ?? 0}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <Target className="h-4 w-4 text-[#15807A]" />
                  Pipeline Overview
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {pipeline.data &&
                  Object.entries(pipeline.data).map(([stage, count]) => (
                    <div
                      key={stage}
                      className="flex items-center justify-between rounded bg-[#F0F9F8] p-2 text-xs"
                    >
                      <span>{stageLabels[stage] || stage}</span>
                      <Badge className="border-0 bg-[#15807A] text-[10px] text-white">
                        {count}
                      </Badge>
                    </div>
                  ))}
              </CardContent>
            </Card>

            <Card className="border-[#0A1F1E] bg-[#0A1F1E] text-white">
              <CardContent className="p-5 text-center">
                <AlertTriangle className="mx-auto mb-2 h-6 w-6 text-amber-400" />
                <p className="text-sm font-semibold">Safety Defaults Active</p>
                <p className="mt-2 text-xs text-[#B7D2D0]">
                  No draft is sent without manual review. WhatsApp remains
                  controlled via draft_only and dry_run by default.
                </p>
              </CardContent>
            </Card>

            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="text-[#0A1F1E]">
                  Top Opportunities
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {topOpportunities.data?.slice(0, 5).map((opportunity) => (
                  <div key={opportunity.id} className="rounded-lg bg-[#F0F9F8] p-3">
                    <p className="text-sm font-bold text-[#0A1F1E]">
                      {opportunity.company}
                    </p>
                    <p className="text-xs text-[#4A6B69]">
                      {opportunity.value} SAR
                    </p>
                    <p className="text-xs text-[#8CB3B0]">
                      {opportunity.status}
                    </p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}