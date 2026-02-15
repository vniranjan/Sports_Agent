import type { Article } from "@/lib/api";

interface ArticleCardProps {
  article: Article;
  showSportTag?: boolean;
}

function formatDate(iso: string | null): string {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return "";
  }
}

export default function ArticleCard({ article, showSportTag }: ArticleCardProps) {
  return (
    <article className="border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors">
      <div className="flex items-start justify-between gap-2 mb-2">
        <h2 className="text-lg font-semibold">{article.headline}</h2>
        {showSportTag && article.sport && (
          <span className="shrink-0 px-2 py-0.5 text-xs font-medium rounded-full bg-gray-100 text-gray-700">
            {article.sport.name}
          </span>
        )}
      </div>
      <p className="text-gray-600 text-sm mb-4">{article.summary}</p>
      <footer className="flex items-center justify-between text-sm text-gray-500">
        <a
          href={article.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 hover:underline"
        >
          {article.source_name}
        </a>
        {article.published_at && (
          <time dateTime={article.published_at}>{formatDate(article.published_at)}</time>
        )}
      </footer>
    </article>
  );
}
