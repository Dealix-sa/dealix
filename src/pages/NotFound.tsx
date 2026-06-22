import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Link } from "react-router";
import { Home, ArrowRight, Search } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#F0F9F8] to-white flex items-center justify-center p-4">
      <Card className="w-full max-w-md text-center border-[#E8F4F3] shadow-lg">
        <CardHeader className="pb-2">
          <div className="mx-auto w-16 h-16 bg-[#E8F4F3] rounded-full flex items-center justify-center mb-4">
            <Search className="w-8 h-8 text-[#15807A]" />
          </div>
          <CardTitle className="text-6xl font-bold text-[#0A1F1E]">404</CardTitle>
          <CardDescription className="text-lg text-[#4A6B69] mt-2">
            الصفحة غير موجودة
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4 pt-4">
          <p className="text-[#8CB3B0]">
            الصفحة التي تبحث عنها غير موجودة أو تم نقلها.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button asChild className="bg-[#15807A] hover:bg-[#0F5F5A]">
              <Link to="/">
                <Home className="w-4 h-4 ml-2" />
                الصفحة الرئيسية
              </Link>
            </Button>
            <Button asChild variant="outline" className="border-[#15807A] text-[#15807A] hover:bg-[#E8F4F3]">
              <Link to="/command-room">
                Command Room
                <ArrowRight className="w-4 h-4 mr-2" />
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
