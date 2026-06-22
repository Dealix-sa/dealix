import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LogIn, Shield } from "lucide-react";

function getOAuthUrl() {
  const kimiAuthUrl = import.meta.env.VITE_KIMI_AUTH_URL;
  const appID = import.meta.env.VITE_APP_ID;
  const redirectUri = `${window.location.origin}/api/oauth/callback`;
  const state = btoa(redirectUri);

  const url = new URL(`${kimiAuthUrl}/api/oauth/authorize`);
  url.searchParams.set("client_id", appID);
  url.searchParams.set("redirect_uri", redirectUri);
  url.searchParams.set("response_type", "code");
  url.searchParams.set("scope", "profile");
  url.searchParams.set("state", state);

  return url.toString();
}

export default function Login() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0A1F1E] to-[#15807A] flex items-center justify-center p-4">
      <Card className="w-full max-w-sm border-0 shadow-2xl">
        <CardHeader className="text-center pb-2">
          <div className="mx-auto w-14 h-14 bg-[#15807A] rounded-xl flex items-center justify-center mb-4">
            <Shield className="w-7 h-7 text-white" />
          </div>
          <CardTitle className="text-2xl font-bold text-[#0A1F1E]">
            مرحباً بك في Dealix
          </CardTitle>
          <CardDescription className="text-[#4A6B69]">
            AI Operating Systems for Saudi B2B
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-4">
          <Button
            className="w-full bg-[#15807A] hover:bg-[#0F5F5A] text-white h-12 text-base"
            size="lg"
            onClick={() => {
              window.location.href = getOAuthUrl();
            }}
          >
            <LogIn className="w-5 h-5 ml-2" />
            تسجيل الدخول
          </Button>
          <p className="text-xs text-center text-[#8CB3B0]">
            بالتسجيل، أنت توافق على سياسة الخصوصية وشروط الاستخدام
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
