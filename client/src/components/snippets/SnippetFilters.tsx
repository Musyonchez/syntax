interface SnippetFiltersProps {
    search: string;
    setSearch: (value: string) => void;
    filter: string;
    setFilter: (value: "newest" | "oldest" | "frequently" | "favorites") => void;
  }
  
  const SnippetFilters: React.FC<SnippetFiltersProps> = ({
    search,
    setSearch,
    filter,
    setFilter,
  }) => {
    return (
      <div className="flex flex-wrap gap-2 items-center mb-6 p-4">
        <input
          type="text"
          placeholder="Search snippets..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border px-3 py-2 rounded w-full sm:w-auto"
        />
        <select
          value={filter}
          onChange={(e) =>
            setFilter(e.target.value as "newest" | "oldest" | "frequently" | "favorites")
          }
          className="border px-2 py-2 rounded bg-gray-900 text-white"
        >
          <option value="newest">Newest</option>
          <option value="oldest">Oldest</option>
          <option value="favorites">Favorites</option>
          <option value="frequently">Frequent</option>
        </select>
      </div>
    );
  };
  
  export default SnippetFilters;
  