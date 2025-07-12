import React from "react";

type SnippetFormProps = {
  title: string;
  setTitle: (val: string) => void;
  content: string;
  setContent: (val: string) => void;
  language: string;
  setLanguage: (val: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
  isSubmitting: boolean;
};

const placeholders: Record<string, string> = {
  python: `# Simple addition\ndef add(a, b):\n    return a + b`,
  javascript: `// Simple addition\nfunction add(a, b) {\n  return a + b;\n}`,
};

const SnippetForm: React.FC<SnippetFormProps> = ({
  title,
  setTitle,
  content,
  setContent,
  language,
  setLanguage,
  handleSubmit,
  isSubmitting,
}) => {
  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="snippetTitle" className="block mb-1 font-medium">Snippet Name:</label>
        <input
          id="snippetTitle"
          type="text"
          placeholder="e.g. Add Two Numbers"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="block w-full border border-gray-300 rounded-md p-3 font-mono text-white bg-gray-900"
          required
        />
        <p className="text-sm text-gray-400 mt-1">
          Give your snippet a short title like “Addition Function.”
        </p>
      </div>

      <div>
        <label htmlFor="language" className="block mb-1 font-medium">Choose Language:</label>
        <select
          id="language"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full border border-gray-300 rounded-md p-2 text-white bg-gray-900"
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
        </select>
        <p className="text-sm text-gray-400 mt-1">
          Currently supporting Python and JavaScript.
        </p>
      </div>

      <div>
        <label htmlFor="code" className="block mb-1 font-medium">
          Paste Your Code: <span className=" text-red-500">NOTE: It is advisable the code be already formatted</span>
        </label>
        <textarea
          id="code"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          rows={10}
          className="w-full border border-gray-300 rounded-md p-3 font-mono text-white bg-gray-900"
          placeholder={placeholders[language]}
          required
        />
        <p className="text-sm text-gray-400 mt-1">
          We’ll mask parts of this to help you practice recalling syntax.
        </p>
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700"
        disabled={isSubmitting}
      >
        {isSubmitting ? "Saving..." : "Save Snippet"}
      </button>
    </form>
  );
};

export default SnippetForm;
