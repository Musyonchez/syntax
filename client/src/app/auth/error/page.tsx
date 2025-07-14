import { Metadata } from "next";
import Link from "next/link";
import { AlertCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const metadata: Metadata = {
  title: "Authentication Error",
  description: "An error occurred during authentication.",
};

export default async function AuthErrorPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  const params = await searchParams;
  const error = params.error;

  const getErrorMessage = (error?: string) => {
    switch (error) {
      case "AccessDenied":
        return {
          title: "Access Denied",
          description: "You denied access to your Google account. Please try again and grant the necessary permissions.",
        };
      case "Configuration":
        return {
          title: "Configuration Error",
          description: "There's an issue with the authentication configuration. Please contact support.",
        };
      case "Verification":
        return {
          title: "Verification Error",
          description: "Unable to verify your identity. Please try again.",
        };
      default:
        return {
          title: "Authentication Error",
          description: "An unexpected error occurred during authentication. Please try again.",
        };
    }
  };

  const errorInfo = getErrorMessage(error);

  return (
    <div className="container relative min-h-screen flex flex-col items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-destructive/10">
            <AlertCircle className="h-6 w-6 text-destructive" />
          </div>
          <CardTitle>{errorInfo.title}</CardTitle>
          <CardDescription>{errorInfo.description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <div className="rounded-md bg-muted p-3">
              <p className="text-sm text-muted-foreground">
                Error code: <code className="font-mono">{error}</code>
              </p>
            </div>
          )}
          <div className="flex flex-col space-y-2">
            <Button asChild>
              <Link href="/auth/signin">Try Again</Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/">Return Home</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}