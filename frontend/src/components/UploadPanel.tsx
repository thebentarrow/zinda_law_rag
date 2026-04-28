import { useState, useRef, useCallback } from "react";
import { Upload, FileText, X, AlertCircle, CheckCircle2, FileJson, File } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import { toast } from "@/hooks/use-toast";
import type { UploadResult } from "@/types/api";

type Mode = "append" | "replace";

const FAQ_EXTENSIONS = [".csv", ".json"];
const DOC_EXTENSIONS = [".pdf", ".docx", ".md", ".txt"];
const ALL_EXTENSIONS = [...FAQ_EXTENSIONS, ...DOC_EXTENSIONS];

function fileCategory(filename: string): "faq" | "document" | null {
  const lower = filename.toLowerCase();
  if (FAQ_EXTENSIONS.some((e) => lower.endsWith(e))) return "faq";
  if (DOC_EXTENSIONS.some((e) => lower.endsWith(e))) return "document";
  return null;
}

function FileIcon({ name }: { name: string }) {
  const lower = name.toLowerCase();
  if (lower.endsWith(".json")) return <FileJson className="h-5 w-5 text-muted-foreground shrink-0" />;
  if (lower.endsWith(".pdf")) return <File className="h-5 w-5 text-red-500 shrink-0" />;
  return <FileText className="h-5 w-5 text-muted-foreground shrink-0" />;
}

export function UploadPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState<Mode>("append");
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<UploadResult | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((f: File) => {
    if (!fileCategory(f.name)) {
      toast({
        title: "Unsupported file type",
        description: `Accepted formats: ${ALL_EXTENSIONS.join(", ")}`,
        variant: "destructive",
      });
      return;
    }
    setFile(f);
    setResult(null);
  }, []);

  function onDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }

  async function handleUpload() {
    if (!file) return;
    if (mode === "replace") {
      const confirmed = window.confirm(
        "Replace mode will delete ALL existing FAQs and document chunks before importing. Continue?"
      );
      if (!confirmed) return;
    }
    setUploading(true);
    try {
      const res = await api.uploadContent(file, mode);
      setResult(res);
      const label = res.upload_type === "faqs" ? "FAQ records" : "document chunks";
      toast({
        title: "Upload complete",
        description: `${res.inserted} ${label} inserted, ${res.indexed} indexed.`,
      });
      setFile(null);
    } catch (err) {
      toast({
        title: "Upload failed",
        description: err instanceof Error ? err.message : "Unknown error",
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  }

  const category = file ? fileCategory(file.name) : null;

  return (
    <div className="space-y-6 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>Upload Legal Content</CardTitle>
          <CardDescription>
            Upload structured FAQ data or any legal document. The system will parse, chunk, and
            index the content automatically.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Supported formats */}
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="text-muted-foreground font-medium self-center">Accepted:</span>
            {[
              { ext: ".csv / .json", label: "FAQ pairs", color: "bg-blue-100 text-blue-800 border-blue-200" },
              { ext: ".pdf", label: "PDF", color: "bg-red-100 text-red-800 border-red-200" },
              { ext: ".docx", label: "Word document", color: "bg-blue-100 text-blue-800 border-blue-200" },
              { ext: ".md", label: "Markdown", color: "bg-purple-100 text-purple-800 border-purple-200" },
              { ext: ".txt", label: "Plain text", color: "bg-gray-100 text-gray-800 border-gray-200" },
            ].map(({ ext, label, color }) => (
              <Badge key={ext} variant="outline" className={`${color} gap-1`}>
                <code>{ext}</code>
                <span className="opacity-70">— {label}</span>
              </Badge>
            ))}
          </div>

          <Separator />

          {/* Drop zone */}
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              dragging
                ? "border-primary bg-primary/5"
                : "border-muted-foreground/30 hover:border-primary/50"
            }`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
          >
            <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
            <p className="text-sm font-medium">Drop file here or click to browse</p>
            <p className="text-xs text-muted-foreground mt-1">
              CSV · JSON · PDF · DOCX · MD · TXT · max 20 MB
            </p>
            <input
              ref={inputRef}
              type="file"
              accept={ALL_EXTENSIONS.join(",")}
              className="hidden"
              onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); e.target.value = ""; }}
            />
          </div>

          {/* Selected file */}
          {file && (
            <div className="flex items-center gap-3 p-3 border rounded-md bg-muted/30">
              <FileIcon name={file.name} />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / 1024).toFixed(1)} KB ·{" "}
                  <span className="font-medium">
                    {category === "faq" ? "Will be imported as FAQ pairs" : "Will be chunked and indexed as a document"}
                  </span>
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 shrink-0"
                onClick={() => setFile(null)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          )}

          {/* Mode */}
          <div>
            <p className="text-sm font-medium mb-1.5">Import mode</p>
            <Select value={mode} onValueChange={(v) => setMode(v as Mode)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="append">Append — add to existing knowledge base</SelectItem>
                <SelectItem value="replace">Replace — delete everything and reimport</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button className="w-full" disabled={!file || uploading} onClick={handleUpload}>
            <Upload className="h-4 w-4" />
            {uploading ? "Uploading & indexing…" : "Upload"}
          </Button>
        </CardContent>
      </Card>

      {/* Result */}
      {result && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <CheckCircle2 className="h-5 w-5 text-green-600" />
              {result.upload_type === "faqs" ? "FAQ Upload Complete" : "Document Ingestion Complete"}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex gap-3 flex-wrap">
              <Badge variant="default">
                {result.inserted} {result.upload_type === "faqs" ? "FAQs" : "chunks"} inserted
              </Badge>
              <Badge variant="secondary">{result.indexed} indexed</Badge>
              {result.skipped > 0 && (
                <Badge variant="outline">{result.skipped} skipped</Badge>
              )}
            </div>
            {result.errors.length > 0 && (
              <div className="space-y-1">
                <p className="text-sm font-medium flex items-center gap-1 text-destructive">
                  <AlertCircle className="h-4 w-4" />
                  Warnings / Errors
                </p>
                <ul className="text-xs text-muted-foreground space-y-0.5 max-h-40 overflow-y-auto">
                  {result.errors.map((e, i) => (
                    <li key={i} className="font-mono bg-muted px-2 py-0.5 rounded">{e}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* FAQ format reference — only shown when a FAQ file is selected or nothing is selected */}
      {category !== "document" && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">FAQ File Format Reference</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-xs">
            <div>
              <p className="font-medium mb-1">CSV</p>
              <pre className="bg-muted rounded p-3 overflow-x-auto leading-relaxed">
{`title,question,answer,category
"What is a contract?","What makes a contract valid?","A valid contract requires offer, acceptance, and consideration.","Contracts"`}
              </pre>
            </div>
            <div>
              <p className="font-medium mb-1">JSON</p>
              <pre className="bg-muted rounded p-3 overflow-x-auto leading-relaxed">
{`[
  {
    "title": "What is a contract?",
    "question": "What makes a contract valid?",
    "answer": "A valid contract requires offer, acceptance, and consideration.",
    "category": "Contracts"
  }
]`}
              </pre>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
