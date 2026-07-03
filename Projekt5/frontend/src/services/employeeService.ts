import { api } from '../api/api';
import type { Employee, EmployeeCreate, EmployeeUpdate, Shift, ShiftCreate, WeeklyScheduleItem, EmployeeRanking } from '../types/Employee';

export const employeeService = {
  getAll: () => api.get<Employee[]>('/employees'),

  getById: (id: number) => api.get<Employee>(`/employees/${id}`),

  create: (data: EmployeeCreate) => api.post<Employee>('/employees', data),

  update: (id: number, data: EmployeeUpdate) => api.patch<Employee>(`/employees/${id}`, data),

  delete: (id: number) => api.delete<void>(`/employees/${id}`),

  getShifts: (employeeId: number) => api.get<Shift[]>(`/employees/${employeeId}/shifts`),

  createShift: (data: ShiftCreate) => api.post<Shift>('/employees/shifts', data),

  updateShift: (id: number, data: Partial<ShiftCreate>) => api.patch<Shift>(`/employees/shifts/${id}`, data),

  deleteShift: (id: number) => api.delete<void>(`/employees/shifts/${id}`),

  getWeeklySchedule: (employeeId: number, weekStart: string) =>
    api.get<WeeklyScheduleItem[]>(`/employees/${employeeId}/weekly-schedule?week_start=${weekStart}`),

  getTotalHours: (employeeId: number, startDate: string, endDate: string) =>
    api.get<number>(`/employees/${employeeId}/total-hours?start_date=${startDate}&end_date=${endDate}`),

  getRanking: (startDate: string, endDate: string, limit = 10) =>
    api.get<EmployeeRanking[]>(`/employees/ranking?start_date=${startDate}&end_date=${endDate}&limit=${limit}`),
};
