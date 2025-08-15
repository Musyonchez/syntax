import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section className="relative h-[calc(100vh-4rem)] flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        
        {/* Floating Elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-purple-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute bottom-40 left-20 w-24 h-24 bg-indigo-200 rounded-full opacity-20 animate-pulse delay-2000"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center z-10">
          <div className="space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center px-4 py-2 bg-white/80 backdrop-blur-sm rounded-full border border-gray-200 shadow-sm">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              <span className="text-sm font-medium text-gray-700">Join 10,000+ developers improving daily</span>
            </div>
            
            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">
              Master Coding Through
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block mt-2">
                Interactive Practice
              </span>
            </h1>
            
            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
              Transform your programming skills with our AI-powered masked code completion exercises. 
              Build muscle memory, learn patterns, and code with confidence.
            </p>
            
            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link
                href="/practice"
                className="group relative bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
              >
                <span className="relative flex items-center">
                  Start Practicing Free
                  <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </Link>
              
              <Link
                href="#how-it-works"
                className="group flex items-center px-8 py-4 bg-white/80 backdrop-blur-sm hover:bg-white border border-gray-200 hover:border-gray-300 text-gray-700 hover:text-gray-900 rounded-xl text-lg font-medium transition-all duration-300 shadow-sm hover:shadow-md"
              >
                <svg className="mr-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                See How It Works
              </Link>
            </div>
            
            {/* Social Proof */}
            <div className="pt-8 flex flex-col sm:flex-row items-center justify-center gap-8 text-sm text-gray-500">
              <div className="flex items-center">
                <div className="flex -space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full border-2 border-white"></div>
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full border-2 border-white"></div>
                  <div className="w-8 h-8 bg-gradient-to-r from-green-400 to-green-600 rounded-full border-2 border-white"></div>
                  <div className="w-8 h-8 bg-gradient-to-r from-yellow-400 to-orange-600 rounded-full border-2 border-white"></div>
                </div>
                <span className="ml-3 font-medium">Loved by developers worldwide</span>
              </div>
              
              <div className="flex items-center">
                <div className="flex text-yellow-400">
                  {[...Array(5)].map((_, i) => (
                    <svg key={i} className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <span className="ml-2 font-medium">4.9/5 from 1,200+ reviews</span>
              </div>
            </div>
          </div>
        </div>
        
        {/* Bottom Wave */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg className="w-full h-20 fill-white" viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25"></path>
            <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5"></path>
            <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z"></path>
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative bg-white py-24 overflow-hidden">
        {/* Background Decoration */}
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-96 h-96 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full opacity-20 blur-3xl"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <div className="inline-block px-4 py-2 bg-blue-50 rounded-full mb-6">
              <span className="text-blue-600 font-semibold text-sm">POWERFUL FEATURES</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Why Developers Choose 
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block">
                SyntaxMem
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built by developers, for developers. Our platform combines cutting-edge technology 
              with proven learning methodologies to accelerate your coding journey.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="group relative bg-white p-8 rounded-2xl border border-gray-100 hover:border-blue-200 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">Interactive Practice</h3>
                <p className="text-gray-600 text-center leading-relaxed">
                  Master coding patterns through hands-on practice. Fill in the blanks, build muscle memory, 
                  and learn by doing with real-world code examples.
                </p>
                <div className="mt-6 flex justify-center">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ⚡ Instant Feedback
                  </span>
                </div>
              </div>
            </div>
            
            <div className="group relative bg-white p-8 rounded-2xl border border-gray-100 hover:border-green-200 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
              <div className="absolute inset-0 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative">
                <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">Smart Analytics</h3>
                <p className="text-gray-600 text-center leading-relaxed">
                  Track your progress with detailed insights. Identify strengths, pinpoint weaknesses, 
                  and get personalized recommendations to accelerate your learning.
                </p>
                <div className="mt-6 flex justify-center">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    📊 Data-Driven
                  </span>
                </div>
              </div>
            </div>
            
            <div className="group relative bg-white p-8 rounded-2xl border border-gray-100 hover:border-purple-200 hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
              <div className="absolute inset-0 bg-gradient-to-br from-purple-50 to-violet-50 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              <div className="relative">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C20.832 18.477 19.246 18 17.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">Multi-Language</h3>
                <p className="text-gray-600 text-center leading-relaxed">
                  Practice across JavaScript, Python, TypeScript, React, and more. Expand your 
                  skill set with curated content for every major programming language.
                </p>
                <div className="mt-6 flex justify-center">
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    🚀 Always Growing
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Stats Section */}
          <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900 mb-2">10K+</div>
              <div className="text-gray-600">Active Developers</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900 mb-2">500K+</div>
              <div className="text-gray-600">Exercises Completed</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900 mb-2">15+</div>
              <div className="text-gray-600">Programming Languages</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-gray-900 mb-2">98%</div>
              <div className="text-gray-600">Success Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="relative bg-gradient-to-b from-gray-50 to-white py-24 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-grid-gray-900/[0.04] bg-[size:20px_20px]"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <div className="inline-block px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 rounded-full mb-6">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent font-semibold text-sm">HOW IT WORKS</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Master Coding in
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block">
                Three Simple Steps
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our proven methodology helps thousands of developers improve their coding skills 
              through structured, interactive practice sessions.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
              {/* Step 1 */}
              <div className="relative text-center group">
                <div className="relative mb-8">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-3xl flex items-center justify-center mx-auto shadow-xl group-hover:shadow-2xl transition-all duration-300 transform group-hover:scale-110">
                    <span className="text-2xl font-bold">1</span>
                  </div>
                  <div className="absolute -inset-4 bg-gradient-to-r from-blue-400 to-blue-600 rounded-full opacity-20 blur-lg group-hover:opacity-30 transition-opacity duration-300"></div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Choose Your Challenge</h3>
                <p className="text-gray-600 leading-relaxed mb-6">
                  Browse our curated library of code snippets across 15+ programming languages. 
                  Pick challenges that match your skill level and learning goals.
                </p>
                <div className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                  <div className="text-sm text-gray-500 mb-2">Popular Languages</div>
                  <div className="flex flex-wrap gap-2 justify-center">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">JavaScript</span>
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">Python</span>
                    <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-medium">TypeScript</span>
                  </div>
                </div>
              </div>
              
              {/* Step 2 */}
              <div className="relative text-center group">
                <div className="relative mb-8">
                  <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-3xl flex items-center justify-center mx-auto shadow-xl group-hover:shadow-2xl transition-all duration-300 transform group-hover:scale-110">
                    <span className="text-2xl font-bold">2</span>
                  </div>
                  <div className="absolute -inset-4 bg-gradient-to-r from-purple-400 to-purple-600 rounded-full opacity-20 blur-lg group-hover:opacity-30 transition-opacity duration-300"></div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Fill in the Blanks</h3>
                <p className="text-gray-600 leading-relaxed mb-6">
                  Complete the masked code by typing the missing keywords, variables, and logic. 
                  Our intelligent system provides instant feedback and hints.
                </p>
                <div className="bg-gray-900 p-4 rounded-xl text-left overflow-hidden">
                  <div className="text-green-400 text-xs mb-2">// JavaScript Example</div>
                  <div className="text-white text-sm font-mono">
                    <div>const [count, setCount] = <span className="bg-blue-500 text-white px-1 rounded">____</span>(0);</div>
                    <div className="text-gray-400">// Type: useState</div>
                  </div>
                </div>
              </div>
              
              {/* Step 3 */}
              <div className="relative text-center group">
                <div className="relative mb-8">
                  <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 text-white rounded-3xl flex items-center justify-center mx-auto shadow-xl group-hover:shadow-2xl transition-all duration-300 transform group-hover:scale-110">
                    <span className="text-2xl font-bold">3</span>
                  </div>
                  <div className="absolute -inset-4 bg-gradient-to-r from-green-400 to-green-600 rounded-full opacity-20 blur-lg group-hover:opacity-30 transition-opacity duration-300"></div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Track & Improve</h3>
                <p className="text-gray-600 leading-relaxed mb-6">
                  Review detailed analytics, identify knowledge gaps, and get personalized 
                  recommendations to accelerate your learning journey.
                </p>
                <div className="bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                  <div className="text-sm text-gray-500 mb-3">Your Progress</div>
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>Accuracy</span>
                      <span className="font-medium">94%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{width: '94%'}}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          
          {/* CTA in this section */}
          <div className="text-center mt-16">
            <Link
              href="/practice"
              className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              Start Your First Session
              <svg className="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="relative bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 py-24 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:60px_60px]"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500 rounded-full opacity-10 blur-3xl"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500 rounded-full opacity-10 blur-3xl"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="inline-block px-4 py-2 bg-white/10 backdrop-blur-sm rounded-full mb-6">
              <span className="text-white font-semibold text-sm">🚀 START YOUR JOURNEY</span>
            </div>
            
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
              Ready to Transform Your
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent block">
                Coding Skills?
              </span>
            </h2>
            
            <p className="text-xl text-gray-300 mb-12 max-w-3xl mx-auto leading-relaxed">
              Join over 10,000 developers who have already accelerated their programming journey with SyntaxMem. 
              Start practicing today and see immediate improvements in your coding confidence.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-12">
              <Link
                href="/practice"
                className="group relative bg-white hover:bg-gray-50 text-gray-900 px-8 py-4 rounded-xl text-lg font-bold transition-all duration-300 shadow-2xl hover:shadow-white/20 transform hover:-translate-y-1"
              >
                <span className="flex items-center">
                  Start Practicing Free
                  <svg className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
              </Link>
              
              <Link
                href="/snippets"
                className="group flex items-center px-8 py-4 bg-white/10 backdrop-blur-sm hover:bg-white/20 border border-white/20 hover:border-white/30 text-white rounded-xl text-lg font-medium transition-all duration-300"
              >
                <svg className="mr-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                Browse Code Snippets
              </Link>
            </div>
            
            {/* Trust Indicators */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              <div className="text-center p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
                <div className="text-3xl font-bold text-white mb-2">10,000+</div>
                <div className="text-gray-300">Developers Trust Us</div>
              </div>
              
              <div className="text-center p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
                <div className="text-3xl font-bold text-white mb-2">500K+</div>
                <div className="text-gray-300">Exercises Completed</div>
              </div>
              
              <div className="text-center p-6 bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10">
                <div className="text-3xl font-bold text-white mb-2">4.9/5</div>
                <div className="text-gray-300">Average Rating</div>
              </div>
            </div>
            
            {/* Security Badge */}
            <div className="mt-12 flex justify-center">
              <div className="inline-flex items-center px-4 py-2 bg-green-500/20 rounded-full border border-green-400/30">
                <svg className="w-4 h-4 text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-green-400 text-sm font-medium">100% Free • No Credit Card Required</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
