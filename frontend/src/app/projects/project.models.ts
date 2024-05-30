import { UserResponse } from "../shared/users/user.models";

export interface ProjectCreate {
    name: string;
    description: string;
    team_members?: UserResponse[];
    project_leaders?: UserResponse[];
  }
  
export interface ProjectUpdate {
    name?: string;
    description?: string;
    team_members?: UserResponse[];
    project_leaders?: UserResponse[];
  }

export interface ProjectResponse {
    id: number;
    name: string;
    description: string;
    team_members: UserResponse[];
    project_leaders: UserResponse[];
  }