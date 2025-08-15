'use client';

import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { Suspense } from 'react';

function ErrorContent() {
  const searchParams = useSearchParams();
  const error = searchParams.get('error');
  const errorDescription = searchParams.get('error_description');

  const getErrorMessage = (errorCode: string | null) => {
    switch (errorCode) {
      case 'Configuration':
        return {
          title: 'Configuration Error',
          description: 'There is a problem with the server configuration.',
          details: 'This usually means environment variables are missing or incorrect.'
        };
      case 'AccessDenied':
        return {
          title: 'Access Denied',
          description: 'You denied access to your account.',
          details: 'Please try signing in again and allow access to continue.'
        };
      case 'Verification':
        return {
          title: 'Verification Error',
          description: 'The verification link is invalid or has expired.',
          details: 'Please request a new verification email.'
        };
      case 'Default':
      default:
        return {
          title: 'Authentication Error',
          description: 'An unexpected error occurred during authentication.',
          details: 'Please try again or contact support if the problem persists.'
        };
    }
  };

  const errorInfo = getErrorMessage(error);

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-gradient-to-br from-red-50 via-orange-50 to-yellow-50">
      <div className="max-w-md w-full mx-4">
        <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-lg border border-red-200/50 p-8 text-center">
          {/* Error Icon */}
          <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>

          {/* Error Details */}
          <h1 className="text-2xl font-bold text-gray-900 mb-3">
            {errorInfo.title}
          </h1>
          
          <p className="text-gray-600 mb-4">
            {errorInfo.description}
          </p>

          <p className="text-sm text-gray-500 mb-6">
            {errorInfo.details}
          </p>

          {/* Debug Information */}
          {(error || errorDescription) && (
            <div className="bg-gray-100 rounded-lg p-4 mb-6 text-left">
              <h3 className="text-sm font-semibold text-gray-700 mb-2">Debug Information:</h3>
              {error && (
                <div className="text-xs text-gray-600 mb-1">
                  <strong>Error Code:</strong> {error}
                </div>
              )}
              {errorDescription && (
                <div className="text-xs text-gray-600">
                  <strong>Description:</strong> {errorDescription}
                </div>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="space-y-3">
            <Link
              href="/login"
              className="block bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-semibold transition-all duration-200 shadow-md hover:shadow-lg"
            >
              Try Again
            </Link>
            
            <Link
              href="/"
              className="block text-gray-600 hover:text-gray-900 px-6 py-3 text-sm font-medium transition-colors"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function AuthErrorPage() {
  return (
    <Suspense fallback={
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
      </div>
    }>
      <ErrorContent />
    </Suspense>
  );
}