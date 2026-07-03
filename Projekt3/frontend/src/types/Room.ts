export interface Room {
  id: number;
  name: string;
  capacity: number;
  description: string;
}

export interface Booking {
  id: number;
  room_id: number;
  user_id: number;
  title: string;
  start_time: string;
  end_time: string;
}

export interface RoomCreate {
  name: string;
  capacity: number;
  description: string;
}

export interface RoomUpdate {
  name?: string;
  capacity?: number;
  description?: string;
}

export interface BookingCreate {
  room_id: number;
  title: string;
  start_time: string;
  end_time: string;
}
