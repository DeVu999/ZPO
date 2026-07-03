import { api } from '../api/api';
import type { Room, RoomCreate, RoomUpdate, Booking, BookingCreate } from '../types/Room';

export const roomService = {
  getAll: () => api.get<Room[]>('/rooms'),

  getById: (id: number) => api.get<Room>(`/rooms/${id}`),

  create: (data: RoomCreate) => api.post<Room>('/rooms', data),

  update: (id: number, data: RoomUpdate) => api.patch<Room>(`/rooms/${id}`, data),

  delete: (id: number) => api.delete<void>(`/rooms/${id}`),

  getAllBookings: () => api.get<Booking[]>('/bookings'),

  createBooking: (data: BookingCreate) => api.post<Booking>('/bookings', data),

  deleteBooking: (id: number) => api.delete<void>(`/bookings/${id}`),

  getAvailableRooms: (start: string, end: string) => {
    const params = new URLSearchParams({ start_time: start, end_time: end });
    return api.get<Room[]>(`/rooms/available?${params}`);
  },
};
