import ArticleCard from "./ArticleCard";
import type { Article } from "@/lib/api";

interface ArticleListProps {
  articles: Article[];
}

export default function ArticleList({ articles }: ArticleListProps) {
  if (articles.length === 0) {
    return (
      <p className="text-gray-500 py-8 text-center">
        No articles found. Run the agent pipeline to fetch news.
      </p>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {articles.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
}
