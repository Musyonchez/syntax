import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-grid-gray-900/[0.02] bg-[size:60px_60px]"></div>
      <div className="absolute top-20 left-10 w-20 h-20 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
      <div className="absolute top-40 right-20 w-16 h-16 bg-purple-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
      <div className="absolute bottom-40 left-20 w-24 h-24 bg-indigo-200 rounded-full opacity-20 animate-pulse delay-2000"></div>
      
      <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="space-y-8">
          {/* 404 Number */}
          <div className="relative">
            <h1 className="text-9xl md:text-[12rem] font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent leading-none">
              404
            </h1>
            <div className="absolute inset-0 text-9xl md:text-[12rem] font-bold text-gray-200 -z-10 blur-sm">
              404
            </div>
          </div>
          
          {/* Error Message */}
          <div className="space-y-4">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
              Oops! Page Not Found
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              The page you're looking for seems to have vanished into the code void. 
              Don't worry, even the best developers encounter 404s!
            </p>
          </div>
          
          {/* Code Block */}
          <div className="bg-gray-900 rounded-2xl p-6 max-w-md mx-auto text-left overflow-hidden shadow-2xl">
            <div className="flex items-center mb-4">
              <div className="flex space-x-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
              <div className="ml-auto text-gray-400 text-sm">error.js</div>
            </div>
            <div className="text-green-400 text-sm font-mono">
              <div className="text-gray-500">// Houston, we have a problem</div>
              <div>
                <span className="text-blue-400">function</span>{' '}
                <span className="text-yellow-300">findPage</span>() {'{'}
              </div>
              <div className="ml-4">
                <span className="text-blue-400">return</span>{' '}
                <span className="text-red-400">null</span>; 
                <span className="text-gray-500"> // Page not found</span>
              </div>
              <div>{'}'}</div>
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
            <Link
              href="/"
              className="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <span className="flex items-center">
                <svg className="mr-2 w-5 h-5 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Home
              </span>
            </Link>
            
            <Link
              href="/practice"
              className="group flex items-center px-8 py-4 bg-white/80 backdrop-blur-sm hover:bg-white border border-gray-200 hover:border-gray-300 text-gray-700 hover:text-gray-900 rounded-xl text-lg font-medium transition-all duration-300 shadow-sm hover:shadow-md"
            >
              <svg className="mr-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
              </svg>
              Start Practicing
            </Link>
          </div>
          
          {/* Helpful Links */}
          <div className="pt-8">
            <p className="text-sm text-gray-500 mb-4">Or try one of these popular pages:</p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/snippets" className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors">
                Code Snippets
              </Link>
              <span className="text-gray-300">•</span>
              <Link href="/dashboard" className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors">
                Dashboard
              </Link>
              <span className="text-gray-300">•</span>
              <Link href="/help" className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors">
                Help Center
              </Link>
              <span className="text-gray-300">•</span>
              <Link href="/contact" className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors">
                Contact Us
              </Link>
            </div>
          </div>
          
          {/* Fun Message */}
          <div className="pt-6">
            <div className="inline-flex items-center px-4 py-2 bg-blue-50 rounded-full">
              <span className="text-blue-600 text-sm font-medium">
                💡 Pro tip: Use the navigation menu to explore our features
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}