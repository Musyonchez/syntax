import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/store";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import {
  addFavorite,
  setAddFavoriteStatus,
  fetchSnippets,
} from "@/store/snippet_store/actions";
import SnippetCard from "@/components/snippets/SnippetCard";
import SnippetFilters from "@/components/snippets/SnippetFilters";
import RandomButtons from "@/components/snippets/RandomButtons";
import { Snippet } from "@/types";
import toast from "react-hot-toast";

const PracticePage: React.FC = () => {
  const dispatch = useDispatch();
  const snippets = useSelector(
    (state: RootState) => state.snippet.snippets || []
  );
  const status = useSelector(
    (state: RootState) => state.snippet.addFavoriteStatus
  );
  const [search, setSearch] = useState<string>("");
  const [filter, setFilter] = useState<
    "newest" | "oldest" | "frequently" | "favorites"
  >("newest");
  const [filteredSnippets, setFilteredSnippets] = useState<Snippet[]>([]);

  useEffect(() => {
    dispatch(fetchSnippets());
  }, [dispatch]);

  useEffect(() => {
    if (status === "loading") {
      toast.loading("Adding to favorites...", { id: "favorite-toast" });
    } else if (status === "success") {
      toast.success("Added to favorites!", { id: "favorite-toast" });
      dispatch(setAddFavoriteStatus("idle"));
    } else if (status === "error") {
      toast.error("Failed to add to favorites.", { id: "favorite-toast" });
      dispatch(setAddFavoriteStatus("idle"));
    }
  }, [status, dispatch]);

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

  const handleAddFavorites = (id: string) => {
    if (!id || status === "loading") {
      return;
    }
    dispatch(addFavorite(Number(id), "group"));
    dispatch(setAddFavoriteStatus("idle"));
  };

  return (
    <div className="bg-[#000d2a] min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <div className="flex flex-wrap items-center justify-between px-4">
          <SnippetFilters
            search={search}
            setSearch={setSearch}
            filter={filter}
            setFilter={setFilter}
          />
          <RandomButtons onOpenRandom={openRandom} />
        </div>

        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 p-4">
          {filteredSnippets.map((snippet) => (
            <SnippetCard
              key={snippet.id}
              snippet={snippet}
              onToggleFavorite={handleAddFavorites}
            />
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default PracticePage;
