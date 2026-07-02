export interface Item {
  id: number;
  name: string;
  description: string;
  created_at: string;
  owner_id: number;
}

export interface ItemCreate {
  name: string;
  description: string;
}

export interface ItemUpdate {
  name?: string;
  description?: string;
}
