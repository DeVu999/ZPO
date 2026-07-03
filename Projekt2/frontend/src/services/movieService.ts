import { api } from '../api/api';
import type { Movie, MovieCreate, MovieUpdate, Rating, TopMovie } from '../types/Movie';

export const movieService = {
  getAll: () => api.get<Movie[]>('/movies'),

  getById: (id: number) => api.get<Movie>(`/movies/${id}`),

  create: (data: MovieCreate) => api.post<Movie>('/movies', data),

  update: (id: number, data: MovieUpdate) => api.patch<Movie>(`/movies/${id}`, data),

  delete: (id: number) => api.delete<void>(`/movies/${id}`),

  rate: (movieId: number, score: number) =>
    api.post<Rating>(`/movies/${movieId}/rate`, { score }),

  getTop: (genre?: string, limit = 10) => {
    const params = new URLSearchParams();
    if (genre) params.set('genre', genre);
    params.set('limit', String(limit));
    return api.get<TopMovie[]>(`/movies/top?${params}`);
  },
};
