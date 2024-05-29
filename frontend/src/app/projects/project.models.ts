import { UserResponse } from "../shared/users/user.models";

export interface ProjectCreate {
    name: string;
    description: string;
    current_users?: UserResponse[];
    owners?: UserResponse[];
  }
  
export interface ProjectUpdate {
    name?: string;
    description?: string;
    current_users?: UserResponse[];
    owners?: UserResponse[];
  }

export interface ProjectResponse {
    id: number;
    name: string;
    description: string;
    current_users: UserResponse[];
    owners: UserResponse[];
  }