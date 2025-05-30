import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-[#000814] text-gray-300 border-t border-[#A0FF70] py-10 px-6">
      <div className="max-w-6xl mx-auto grid grid-cols-2 sm:grid-cols-3 gap-8">
        {/* Brand */}
        <div>
          <h3 className="text-xl font-bold text-white">SyntaxMem</h3>
          <p className="text-sm mt-2">
            Practice smarter. Memorize syntax. Code with confidence.
          </p>
        </div>

        {/* Navigation */}
        <div>
          <h4 className="font-semibold text-white mb-2">Quick Links</h4>
          <ul className="space-y-2 text-sm">
            <li>
              <Link href="/" className="hover:text-white">
                Home
              </Link>
            </li>
            <li>
              <Link href="/add_snippet" className="hover:text-white">
                Add Snippet
              </Link>
            </li>
            <li>
              <Link href="/practice" className="hover:text-white">
                Practice
              </Link>
            </li>
            <li>
              <Link href="/leaderboard" className="hover:text-white">
                Leaderboard
              </Link>
            </li>
          </ul>
        </div>

        {/* Contact or Social */}
        <div>
          <h4 className="font-semibold text-white mb-2">Connect</h4>
          <ul className="space-y-2 text-sm">
            <li>
              <a
                href="mailto:contact@syntaxmem.app"
                className="hover:text-white"
              >
                Email Us
              </a>
            </li>
            <li>
              <a
                href="https://github.com/your-repo"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-white"
              >
                GitHub
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div className="text-center mt-10 text-xs text-gray-500">
        © {new Date().getFullYear()} SyntaxMem. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;
