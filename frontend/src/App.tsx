import { Scale } from "lucide-react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { QueryPanel } from "@/components/QueryPanel";
import { LogsPanel } from "@/components/LogsPanel";
import { FAQsPanel } from "@/components/FAQsPanel";
import { UploadPanel } from "@/components/UploadPanel";
import { Toaster } from "@/components/Toaster";

export default function App() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="container max-w-4xl mx-auto px-4 h-14 flex items-center gap-3">
          <Scale className="h-5 w-5 text-primary" />
          <div>
            <h1 className="text-base font-semibold leading-none">Zinda Law</h1>
            <p className="text-xs text-muted-foreground">Legal FAQ Assistant</p>
          </div>
        </div>
      </header>

      <main className="container max-w-4xl mx-auto px-4 py-8">
        <Tabs defaultValue="ask">
          <TabsList className="mb-6">
            <TabsTrigger value="ask">Ask a Question</TabsTrigger>
            <TabsTrigger value="faqs">Browse Data</TabsTrigger>
            <TabsTrigger value="upload">Upload Data</TabsTrigger>
            <TabsTrigger value="logs">Query Logs</TabsTrigger>
          </TabsList>

          <TabsContent value="ask">
            <QueryPanel />
          </TabsContent>

          <TabsContent value="faqs">
            <FAQsPanel />
          </TabsContent>

          <TabsContent value="upload">
            <UploadPanel />
          </TabsContent>

          <TabsContent value="logs">
            <LogsPanel />
          </TabsContent>
        </Tabs>
      </main>

      <Toaster />
    </div>
  );
}
