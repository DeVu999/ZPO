import { api } from '../api/api';
import type { User } from '../types/User';

export const userService = {
  getAll: () => api.get<User[]>('/users'),

  getById: (id: number) => api.get<User>(`/users/${id}`),

  updateRole: (id: number, role: 'admin' | 'user') =>
    api.patch<User>(`/users/${id}/role`, { role }),

  toggleActive: (id: number) =>
    api.patch<User>(`/users/${id}/toggle-active`),

  delete: (id: number) => api.delete<void>(`/users/${id}`),
};
