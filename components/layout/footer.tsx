import Link from 'next/link';
import Image from 'next/image';

export function Footer() {
  return (
    <footer className="relative bg-gradient-to-br from-gray-50 to-blue-50/30 border-t border-gray-200/50">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-gray-900/[0.02] bg-[size:40px_40px]"></div>
      
      <div className="relative max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-5 lg:gap-12 space-y-12 lg:space-y-0 text-center lg:text-left">
          {/* Company Info */}
          <div className="lg:col-span-2">
            <div className="flex items-center justify-center lg:justify-start mb-6">
              <Image
                src="/logo.png"
                alt="SyntaxMem"
                width={120}
                height={32}
                className="h-8"
              />
            </div>
            <p className="text-gray-600 mb-6 max-w-md leading-relaxed mx-auto lg:mx-0">
              Transform your programming skills with interactive masked code completion exercises. 
              Join thousands of developers improving their coding abilities daily.
            </p>
            
            {/* Social Proof */}
            <div className="flex items-center justify-center lg:justify-start space-x-6 mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">10K+</div>
                <div className="text-xs text-gray-500">Developers</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">500K+</div>
                <div className="text-xs text-gray-500">Exercises</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">4.9/5</div>
                <div className="text-xs text-gray-500">Rating</div>
              </div>
            </div>
            
            {/* Newsletter */}
            <div className="mb-6">
              <h4 className="text-sm font-semibold text-gray-900 mb-3">Stay Updated</h4>
              <div className="flex max-w-md mx-auto lg:mx-0">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm"
                />
                <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-2 rounded-r-lg text-sm font-medium transition-all duration-200">
                  Subscribe
                </button>
              </div>
            </div>
          </div>
          
          {/* Links Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-8 lg:contents">
            {/* Product Links */}
            <div>
              <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-6">Product</h4>
              <ul className="space-y-4">
                <li>
                  <Link href="/practice" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Practice Sessions
                  </Link>
                </li>
                <li>
                  <Link href="/snippets" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Code Snippets
                  </Link>
                </li>
                <li>
                  <Link href="/dashboard" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Dashboard
                  </Link>
                </li>
                <li>
                  <Link href="/analytics" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Analytics
                  </Link>
                </li>
              </ul>
            </div>
            
            {/* Resources */}
            <div>
              <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-6">Resources</h4>
              <ul className="space-y-4">
                <li>
                  <Link href="/docs" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Documentation
                  </Link>
                </li>
                <li>
                  <Link href="/tutorials" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Tutorials
                  </Link>
                </li>
                <li>
                  <Link href="/blog" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Blog
                  </Link>
                </li>
                <li>
                  <Link href="/changelog" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Changelog
                  </Link>
                </li>
              </ul>
            </div>
            
            {/* Support */}
            <div className="md:col-span-1">
              <h4 className="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-6">Support</h4>
              <ul className="space-y-4">
                <li>
                  <Link href="/help" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link href="/contact" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Contact Us
                  </Link>
                </li>
                <li>
                  <Link href="/status" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    System Status
                  </Link>
                </li>
                <li>
                  <Link href="/feedback" className="text-gray-600 hover:text-blue-600 transition-colors duration-200 text-sm">
                    Feedback
                  </Link>
                </li>
              </ul>
            </div>
            
            {/* Empty 4th grid item for mobile layout */}
            <div className="md:hidden"></div>
          </div>
        </div>
        
        {/* Bottom Section */}
        <div className="mt-12 pt-8 border-t border-gray-200/50">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-6">
              <p className="text-gray-500 text-sm">
                © 2024 SyntaxMem. All rights reserved.
              </p>
              <div className="hidden md:flex items-center space-x-4 text-xs text-gray-400">
                <Link href="/privacy" className="hover:text-gray-600 transition-colors">
                  Privacy Policy
                </Link>
                <span>•</span>
                <Link href="/terms" className="hover:text-gray-600 transition-colors">
                  Terms of Service
                </Link>
                <span>•</span>
                <Link href="/cookies" className="hover:text-gray-600 transition-colors">
                  Cookie Policy
                </Link>
              </div>
            </div>
            
            {/* Social Links */}
            <div className="flex items-center space-x-4">
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors duration-200">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z" />
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors duration-200">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0C5.374 0 0 5.373 0 12 0 17.302 3.438 21.8 8.207 23.387c.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-600 transition-colors duration-200">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
                </svg>
              </a>
            </div>
          </div>
          
          {/* Additional Info */}
          <div className="mt-6 text-center">
            <p className="text-xs text-gray-400">
              Built with ❤️ and the principle of Simple, Uniform, Consistent. 
              <span className="mx-2">•</span>
              Made for developers, by developers.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}