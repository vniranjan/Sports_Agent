import Link from "next/link";
import { getSports } from "@/lib/api";
import SportNav from "@/components/SportNav";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  let sports;
  try {
    sports = await getSports();
  } catch (e) {
    sports = [];
  }
  return (
    <div>
      <header className="mb-8">
        <h1 className="text-3xl font-bold">Sports News</h1>
        <p className="text-gray-600 mt-1">Cricket and Soccer headlines with AI summaries</p>
      </header>
      <SportNav sports={sports} />
      <div className="space-y-4">
        <p className="text-gray-600">
          Select a sport above or browse{" "}
          <Link href="/cricket" className="text-blue-600 hover:underline">
            Cricket
          </Link>{" "}
          and{" "}
          <Link href="/soccer" className="text-blue-600 hover:underline">
            Soccer
          </Link>{" "}
          articles.
        </p>
      </div>
    </div>
  );
}
