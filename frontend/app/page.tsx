import { getArticles, getSports } from "@/lib/api";
import SportNav from "@/components/SportNav";
import ArticleList from "@/components/ArticleList";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  let sports: Awaited<ReturnType<typeof getSports>> = [];
  let articles: Awaited<ReturnType<typeof getArticles>> = [];
  try {
    [sports, articles] = await Promise.all([
      getSports(),
      getArticles(),
    ]);
  } catch {
    // API may be unreachable
  }

  return (
    <div>
      <header className="mb-8">
        <h1 className="text-3xl font-bold">Sports News</h1>
        <p className="text-gray-600 mt-1">Cricket and Soccer headlines with AI summaries</p>
      </header>
      <SportNav sports={sports} />
      <ArticleList articles={articles} showSportTag />
    </div>
  );
}
