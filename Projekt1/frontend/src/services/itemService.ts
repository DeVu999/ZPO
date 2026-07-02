import { api } from '../api/api';
import type { Item, ItemCreate, ItemUpdate } from '../types/Item';

export const itemService = {
  getAll: () => api.get<Item[]>('/items'),

  getById: (id: number) => api.get<Item>(`/items/${id}`),

  create: (data: ItemCreate) => api.post<Item>('/items', data),

  update: (id: number, data: ItemUpdate) => api.patch<Item>(`/items/${id}`, data),

  delete: (id: number) => api.delete<void>(`/items/${id}`),
};
