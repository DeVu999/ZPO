export interface Employee {
  id: number;
  name: string;
  position: string;
  department: string;
  created_at: string;
}

export interface EmployeeCreate {
  name: string;
  position: string;
  department: string;
}

export interface EmployeeUpdate {
  name?: string;
  position?: string;
  department?: string;
}

export interface Shift {
  id: number;
  employee_id: number;
  user_id: number;
  shift_date: string;
  start_time: string;
  end_time: string;
  task: string;
}

export interface ShiftCreate {
  employee_id: number;
  shift_date: string;
  start_time: string;
  end_time: string;
  task: string;
}

export interface WeeklyScheduleItem {
  id: number;
  date: string;
  start: string;
  end: string;
  task: string;
}

export interface EmployeeRanking {
  id: number;
  name: string;
  position: string;
  hours: number;
}
