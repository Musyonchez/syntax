export interface Snippet {
    id: string;
    title: string;
    content: string;
    language: string;
    userId: string;
    createdAt: string;
    favorite?: boolean;
    solveCount?: number;
  }
  