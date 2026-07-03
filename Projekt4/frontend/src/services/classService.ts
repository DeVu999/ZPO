import { api } from '../api/api';
import type { FitnessClass, ClassCreate, ClassUpdate, SignupCreate, MyClassSignup } from '../types/Fitness';

export const classService = {
  getAll: () => api.get<FitnessClass[]>('/fitness'),

  getById: (id: number) => api.get<FitnessClass>(`/fitness/${id}`),

  getAvailable: () => api.get<FitnessClass[]>('/fitness/available'),

  create: (data: ClassCreate) => api.post<FitnessClass>('/fitness', data),

  update: (id: number, data: ClassUpdate) => api.patch<FitnessClass>(`/fitness/${id}`, data),

  delete: (id: number) => api.delete<void>(`/fitness/${id}`),

  signup: (data: SignupCreate) => api.post<void>('/fitness/signup', data),

  cancelSignup: (classId: number) => api.delete<void>(`/fitness/signup/${classId}`),

  getMyClasses: () => api.get<MyClassSignup[]>('/fitness/mine'),

  getWaitlist: (classId: number) => api.get<MyClassSignup>(`/fitness/${classId}/waitlist`),
};
