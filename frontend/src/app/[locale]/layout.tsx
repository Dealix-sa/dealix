import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { notFound } from "next/navigation";
import { ThemeProvider } from "next-themes";
import { routing } from "@/i18n/routing";
import { AuthProvider } from "@/lib/hooks/useAuth";
import { Toaster } from "sonner";

interface LocaleLayoutProps {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function LocaleLayout({
  children,
  params,
}: LocaleLayoutProps) {
  const { locale } = await params;

  if (!routing.locales.includes(locale as "ar" | "en")) {
    notFound();
  }

  const messages = await getMessages();
  const isRTL = locale === "ar";

  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Dealix",
    "url": "https://dealix.sa",
    "logo": "https://dealix.sa/logo.png",
    "description": locale === "ar" ? "نظام تشغيل الإيرادات الأول المدعوم بوكلاء الذكاء الاصطناعي في السعودية" : "The First AI-Powered Revenue Operating System in Saudi Arabia",
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+966-50-000-0000",
      "contactType": "customer service",
      "availableLanguage": ["Arabic", "English"]
    }
  };

  return (
    <html
      lang={locale}
      dir={isRTL ? "rtl" : "ltr"}
      suppressHydrationWarning
    >
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
      </head>
      <body className="font-arabic antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange={false}
        >
          <NextIntlClientProvider messages={messages}>
            <AuthProvider>
              {children}
              <Toaster
                position={isRTL ? "bottom-left" : "bottom-right"}
                toastOptions={{
                  style: {
                    fontFamily: "'Noto Sans Arabic', sans-serif",
                  },
                }}
              />
            </AuthProvider>
          </NextIntlClientProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
