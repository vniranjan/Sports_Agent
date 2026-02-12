import { getArticles, getSports } from "@/lib/api";
import SportNav from "@/components/SportNav";
import ArticleList from "@/components/ArticleList";

export const dynamic = "force-dynamic";

interface Props {
  params: Promise<{ sport: string }>;
}

export default async function SportPage({ params }: Props) {
  const { sport: sportSlug } = await params;
  let sports = [];
  let articles: Awaited<ReturnType<typeof getArticles>> = [];
  try {
    [sports, articles] = await Promise.all([
      getSports(),
      getArticles({ sport: sportSlug }),
    ]);
  } catch {
    // API may be unreachable
  }

  const sportName = sports.find((s) => s.slug === sportSlug)?.name || sportSlug;

  return (
    <div>
      <header className="mb-8">
        <h1 className="text-3xl font-bold">{sportName} News</h1>
      </header>
      <SportNav sports={sports} activeSlug={sportSlug} />
      <ArticleList articles={articles} />
    </div>
  );
}
