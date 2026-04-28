import { useState, useEffect, useCallback } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import type { FAQItem, FAQListResponse } from "@/types/api";

const CATEGORIES = [
  "All",
  "Contracts",
  "Employment",
  "Intellectual Property",
  "Liability",
  "Privacy",
  "Business Law",
];

function FAQRow({ faq }: { faq: FAQItem }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border rounded-md overflow-hidden">
      <button
        className="w-full flex items-center justify-between gap-3 p-4 text-left hover:bg-muted/50 transition-colors"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
      >
        <div className="flex items-center gap-2 min-w-0">
          <Badge variant="outline" className="text-xs shrink-0">
            #{faq.id}
          </Badge>
          <span className="text-sm font-medium truncate">{faq.title}</span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <Badge variant="secondary" className="text-xs hidden sm:inline-flex">
            {faq.category}
          </Badge>
          {open ? (
            <ChevronDown className="h-4 w-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="h-4 w-4 text-muted-foreground" />
          )}
        </div>
      </button>
      {open && (
        <div className="px-4 pb-4 space-y-2 border-t bg-muted/20">
          <p className="text-sm font-medium pt-3 text-muted-foreground">{faq.question}</p>
          <p className="text-sm leading-relaxed">{faq.answer}</p>
        </div>
      )}
    </div>
  );
}

export function FAQsPanel() {
  const [data, setData] = useState<FAQListResponse | null>(null);
  const [category, setCategory] = useState("All");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (cat: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getFaqs(cat === "All" ? undefined : cat, 1, 200);
      setData(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load FAQs");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load(category);
  }, [category, load]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Select value={category} onValueChange={setCategory}>
          <SelectTrigger className="w-52">
            <SelectValue placeholder="Filter by category" />
          </SelectTrigger>
          <SelectContent>
            {CATEGORIES.map((c) => (
              <SelectItem key={c} value={c}>
                {c}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <p className="text-sm text-muted-foreground">
          {data ? `${data.total} FAQs` : ""}
        </p>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="pt-6 text-destructive text-sm">{error}</CardContent>
        </Card>
      )}

      {loading && !data && (
        <div className="space-y-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-12 w-full rounded-md" />
          ))}
        </div>
      )}

      {data && (
        <div className="space-y-1.5">
          {data.faqs.map((faq) => (
            <FAQRow key={faq.id} faq={faq} />
          ))}
        </div>
      )}
    </div>
  );
}
