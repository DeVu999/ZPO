export interface Movie {
  id: number;
  title: string;
  description: string;
  genre: string;
  created_at: string;
  average_rating: number | null;
  rating_count: number;
}

export interface MovieCreate {
  title: string;
  description: string;
  genre: string;
}

export interface MovieUpdate {
  title?: string;
  description?: string;
  genre?: string;
}

export interface Rating {
  id: number;
  movie_id: number;
  user_id: number;
  score: number;
  created_at: string;
}

export interface TopMovie {
  id: number;
  title: string;
  description: string;
  genre: string;
  avg: number;
  count: number;
}
