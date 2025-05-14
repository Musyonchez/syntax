import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchSnippets } from "../store/snippet_store/actions";
import { RootState } from "../store";
import Link from "next/link";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

// Define snippet type
interface Snippet {
  id: string;
  title: string;
  content: string;
  language: string;
  userId: string;
  createdAt: string;
  favorite?: boolean;
  solveCount?: number;
}

const PracticePage: React.FC = () => {
  const dispatch = useDispatch();
  const snippets = useSelector(
    (state: RootState) => state.snippet.snippets || []
  );
  console.log(snippets)
  const [search, setSearch] = useState<string>("");
  const [filter, setFilter] = useState<
    "newest" | "oldest" | "frequently" | "favorites"
  >("newest");
  const [filteredSnippets, setFilteredSnippets] = useState<Snippet[]>([]);

  useEffect(() => {
    dispatch(fetchSnippets());
  }, [dispatch]);

  useEffect(() => {
    let filtered = [...snippets];

    if (filter === "newest") {
      filtered.sort(
        (a, b) =>
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
      );
    } else if (filter === "oldest") {
      filtered.sort(
        (a, b) =>
          new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      );
    } else if (filter === "favorites") {
      filtered = filtered.filter((s) => s.favorite);
    } else if (filter === "frequently") {
      filtered.sort((a, b) => (b.solveCount || 0) - (a.solveCount || 0));
    }

    if (search.trim()) {
      filtered = filtered.filter((s) =>
        s.title.toLowerCase().includes(search.toLowerCase())
      );
    }

    setFilteredSnippets(filtered);
  }, [search, filter, snippets]);

  const openRandom = (type: "all" | "favorites" | "frequent") => {
    let pool = [...snippets];

    if (type === "favorites") {
      pool = pool.filter((s) => s.favorite);
    } else if (type === "frequent") {
      pool = pool.filter((s) => (s.solveCount || 0) > 5);
    }

    if (pool.length === 0) {
      return;
    }

    const randomSnippet = pool[Math.floor(Math.random() * pool.length)];
    window.open(`/solve/${randomSnippet.id}`, "_blank");
  };

  return (
    <div className=" bg-[#000d2a] min-h-screen flex flex-col">
      <Navbar />
      <main className=" flex-grow">
        <div className="flex flex-wrap gap-2 items-center mb-6 p-4">
          <input
            type="text"
            placeholder="Search snippets..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border px-3 py-2 rounded w-full sm:w-auto"
          />
          <button
            onClick={() => {}}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Search
          </button>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as typeof filter)}
            className="border px-2 py-2 rounded bg-gray-900 text-white"
          >
            <option value="newest">Newest</option>
            <option value="oldest">Oldest</option>
            <option value="favorites">Favorites</option>
            <option value="favorites">Frequent</option>
          </select>

          <div className="ml-auto flex gap-2">
            <button
              onClick={() => openRandom("all")}
              className="bg-gray-700 text-white px-3 py-1 rounded"
            >
              🎲 Random
            </button>
            <button
              onClick={() => openRandom("favorites")}
              className="bg-yellow-600 text-white px-3 py-1 rounded"
            >
              ⭐ Favorites
            </button>
            <button
              onClick={() => openRandom("frequent")}
              className="bg-purple-600 text-white px-3 py-1 rounded"
            >
              🔁 Frequent
            </button>
          </div>
        </div>

        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 p-4">
          {filteredSnippets.map((snippet) => (
            <div
              key={snippet.id}
              className="border p-4 rounded shadow hover:shadow-lg transition cursor-pointer"
              onClick={() => window.open(`/solve/${snippet.id}`, "_blank")}
            >
              <h3 className="font-semibold text-lg mb-2 truncate">
                {snippet.title}
              </h3>
              <pre className="bg-gray-100 p-2 rounded overflow-x-auto text-sm text-black">
                {snippet.content?.split("\n").slice(0, 10).join("\n") || ""}
              </pre>
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default PracticePage;
