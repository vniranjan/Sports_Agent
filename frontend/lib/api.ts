const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Sport {
  id: number;
  name: string;
  slug: string;
  created_at?: string;
}

export interface Article {
  id: number;
  headline: string;
  summary: string;
  source_url: string;
  source_name: string;
  published_at: string | null;
  sport: Sport;
}

export async function getSports(): Promise<Sport[]> {
  const res = await fetch(`${API_URL}/api/sports`);
  if (!res.ok) throw new Error("Failed to fetch sports");
  return res.json();
}

export async function getArticles(params?: {
  sport?: string;
  from?: string;
  to?: string;
}): Promise<Article[]> {
  const searchParams = new URLSearchParams();
  if (params?.sport) searchParams.set("sport", params.sport);
  if (params?.from) searchParams.set("from", params.from);
  if (params?.to) searchParams.set("to", params.to);
  const qs = searchParams.toString();
  const url = `${API_URL}/api/articles${qs ? `?${qs}` : ""}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch articles");
  return res.json();
}

export async function getArticle(id: number): Promise<Article> {
  const res = await fetch(`${API_URL}/api/articles/${id}`);
  if (!res.ok) throw new Error("Failed to fetch article");
  return res.json();
}
