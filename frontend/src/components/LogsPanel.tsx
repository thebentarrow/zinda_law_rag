import { useState, useEffect, useCallback } from "react";
import { RefreshCw, ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { api } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import type { LogListResponse } from "@/types/api";

const PAGE_SIZE = 10;

export function LogsPanel() {
  const [data, setData] = useState<LogListResponse | null>(null);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (p: number) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getLogs(p, PAGE_SIZE);
      setData(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load logs");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load(page);
  }, [page, load]);

  const totalPages = data ? Math.ceil(data.total / PAGE_SIZE) : 1;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          {data ? `${data.total} queries logged` : ""}
        </p>
        <Button variant="outline" size="sm" onClick={() => load(page)} disabled={loading}>
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="pt-6 text-destructive text-sm">{error}</CardContent>
        </Card>
      )}

      {loading && !data && (
        <div className="space-y-3">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-3 w-1/4" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-3 w-full" />
                <Skeleton className="h-3 w-5/6 mt-1" />
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {data && data.logs.length === 0 && (
        <Card>
          <CardContent className="pt-6 text-center text-muted-foreground text-sm">
            No queries logged yet. Ask a question to see it appear here.
          </CardContent>
        </Card>
      )}

      {data &&
        data.logs.map((log, idx) => (
          <Card key={log.id}>
            <CardHeader className="pb-2">
              <div className="flex items-start justify-between gap-2">
                <CardTitle className="text-sm font-medium leading-snug">
                  {log.user_question}
                </CardTitle>
                <span className="text-xs text-muted-foreground shrink-0">
                  {formatDate(log.created_at)}
                </span>
              </div>
              <CardDescription className="flex gap-1.5 flex-wrap">
                <Badge variant="outline" className="text-xs">
                  {log.chat_model}
                </Badge>
                {log.retrieved_faq_titles.map((title) => (
                  <Badge key={title} variant="secondary" className="text-xs">
                    {title}
                  </Badge>
                ))}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed text-muted-foreground line-clamp-4">
                {log.ai_response}
              </p>
            </CardContent>
            {idx < data.logs.length - 1 && <Separator />}
          </Card>
        ))}

      {data && totalPages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1 || loading}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <span className="text-sm text-muted-foreground">
            {page} / {totalPages}
          </span>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages || loading}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
}
