export interface FitnessClass {
  id: number;
  name: string;
  description: string;
  instructor: string;
  datetime: string;
  capacity: number;
  free_spots: number;
  created_at: string;
}

export interface Signup {
  id: number;
  class_id: number;
  user_id: number;
  is_waitlisted: boolean;
  signed_up_at: string;
}

export interface ClassCreate {
  name: string;
  description: string;
  instructor: string;
  datetime: string;
  capacity: number;
}

export interface ClassUpdate {
  name?: string;
  description?: string;
  instructor?: string;
  datetime?: string;
  capacity?: number;
}

export interface SignupCreate {
  class_id: number;
}

export interface MyClassSignup {
  id: number;
  class_id: number;
  user_id: number;
  is_waitlisted: boolean;
  signed_up_at: string;
  fitness_class: FitnessClass;
}
