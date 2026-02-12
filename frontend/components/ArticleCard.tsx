interface Article {
  id: number;
  headline: string;
  summary: string;
  source_url: string;
  source_name: string;
  published_at: string | null;
}

interface ArticleCardProps {
  article: Article;
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

export default function ArticleCard({ article }: ArticleCardProps) {
  return (
    <article className="border border-gray-200 rounded-lg p-5 hover:border-gray-300 transition-colors">
      <h2 className="text-lg font-semibold mb-2">{article.headline}</h2>
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
