export interface SourceItem {
  id: number;
  type: "faq" | "chunk";
  title: string;
  question: string;
  category: string;
}

export interface QueryResponse {
  answer: string;
  sources: SourceItem[];
  log_id: number;
  blocked: boolean;
}

export interface FAQItem {
  id: number;
  title: string;
  question: string;
  answer: string;
  category: string;
  created_at: string;
}

export interface FAQListResponse {
  total: number;
  faqs: FAQItem[];
}

export interface LogEntry {
  id: number;
  user_question: string;
  retrieved_faq_ids: number[];
  retrieved_faq_titles: string[];
  ai_response: string;
  chat_model: string;
  embedding_model: string;
  created_at: string;
}

export interface LogListResponse {
  total: number;
  page: number;
  page_size: number;
  logs: LogEntry[];
}

export interface UploadResult {
  upload_type: "faqs" | "document";
  inserted: number;
  skipped: number;
  indexed: number;
  errors: string[];
}

export interface HealthResponse {
  status: string;
  chat_model: string;
  embedding_model: string;
  retrieval_top_k: number;
  environment: string;
}
