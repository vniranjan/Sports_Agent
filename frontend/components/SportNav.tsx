"use client";

import Link from "next/link";

interface Sport {
  id: number;
  name: string;
  slug: string;
}

interface SportNavProps {
  sports: Sport[];
  activeSlug?: string;
}

export default function SportNav({ sports, activeSlug }: SportNavProps) {
  return (
    <nav className="flex gap-4 border-b border-gray-200 pb-4 mb-6">
      <Link
        href="/"
        className={`px-4 py-2 rounded-md font-medium ${
          !activeSlug ? "bg-gray-900 text-white" : "text-gray-600 hover:bg-gray-100"
        }`}
      >
        All
      </Link>
      {sports.map((sport) => (
        <Link
          key={sport.id}
          href={`/${sport.slug}`}
          className={`px-4 py-2 rounded-md font-medium ${
            activeSlug === sport.slug ? "bg-gray-900 text-white" : "text-gray-600 hover:bg-gray-100"
          }`}
        >
          {sport.name}
        </Link>
      ))}
    </nav>
  );
}
