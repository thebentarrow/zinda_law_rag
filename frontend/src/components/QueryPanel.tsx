import { useState } from "react";
import { Send, BookOpen, ShieldAlert, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { api } from "@/lib/api";
import type { QueryResponse } from "@/types/api";

const CATEGORY_COLORS: Record<string, string> = {
  Contracts: "bg-blue-100 text-blue-800 border-blue-200",
  Employment: "bg-green-100 text-green-800 border-green-200",
  "Intellectual Property": "bg-purple-100 text-purple-800 border-purple-200",
  Liability: "bg-orange-100 text-orange-800 border-orange-200",
  Privacy: "bg-rose-100 text-rose-800 border-rose-200",
  "Business Law": "bg-teal-100 text-teal-800 border-teal-200",
  PDF: "bg-red-100 text-red-800 border-red-200",
  MARKDOWN: "bg-purple-100 text-purple-800 border-purple-200",
  TEXT: "bg-gray-100 text-gray-800 border-gray-200",
};

export function QueryPanel() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!question.trim() || loading) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await api.query(question.trim());
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-3">
        <Textarea
          placeholder="Ask a legal question… e.g. 'What is needed for a contract to be legally binding?'"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={4}
          className="resize-none text-base"
          disabled={loading}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) handleSubmit(e as unknown as React.FormEvent);
          }}
        />
        <div className="flex items-center justify-between">
          <p className="text-xs text-muted-foreground">Press Ctrl+Enter to submit</p>
          <Button type="submit" disabled={loading || question.trim().length < 5}>
            <Send className="h-4 w-4" />
            {loading ? "Thinking…" : "Ask"}
          </Button>
        </div>
      </form>

      {loading && (
        <Card>
          <CardHeader>
            <Skeleton className="h-5 w-32" />
          </CardHeader>
          <CardContent className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </CardContent>
        </Card>
      )}

      {error && (
        <Card className="border-destructive">
          <CardContent className="pt-6 text-destructive text-sm">{error}</CardContent>
        </Card>
      )}

      {result && result.blocked && (
        <Card className="border-amber-300 bg-amber-50">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base text-amber-800">
              <ShieldAlert className="h-4 w-4" />
              Question out of scope
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-amber-900">{result.answer}</p>
          </CardContent>
        </Card>
      )}

      {result && !result.blocked && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">AI Answer</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{result.answer}</p>
            </CardContent>
          </Card>

          {result.sources.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <BookOpen className="h-4 w-4" />
                  Retrieved Sources
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {result.sources.map((src, idx) => (
                  <div key={`${src.type}-${src.id}`}>
                    {idx > 0 && <Separator className="mb-4" />}
                    <div className="space-y-1.5">
                      <div className="flex items-start gap-2 flex-wrap">
                        {src.type === "chunk" ? (
                          <FileText className="h-3.5 w-3.5 text-muted-foreground shrink-0 mt-0.5" />
                        ) : (
                          <Badge variant="outline" className="text-xs shrink-0">#{src.id}</Badge>
                        )}
                        <Badge
                          variant="outline"
                          className={`text-xs shrink-0 ${CATEGORY_COLORS[src.category] ?? ""}`}
                        >
                          {src.category}
                        </Badge>
                        <span className="text-sm font-medium">{src.title}</span>
                      </div>
                      <p className="text-xs text-muted-foreground pl-1">{src.question}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
