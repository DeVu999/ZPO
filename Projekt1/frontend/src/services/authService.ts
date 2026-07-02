import { api } from '../api/api';
import type { User } from '../types/User';

export const authService = {
  getMe: () => api.get<{ user: User }>('/auth/me'),
};
