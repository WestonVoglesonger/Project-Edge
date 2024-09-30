import { UserResponse } from "../shared/users/user.models";

export interface Project {
    name: string;
    description: string;
    team_members?: UserResponse[];
    project_leaders?: UserResponse[];
  }

export interface ProjectResponse {
    id: number;
    name: string;
    description: string;
    created_at: string;
    updated_at: string;
    team_members: UserResponse[];
    project_leaders: UserResponse[];
  }

export interface JoinProjectRequestCreate {
    user_id: number;
    project_id: number;
  }

export interface JoinProjectRequestResponse {
    id: number;
    user_id: number;
    project_id: number;
    created_at: string;
    status: number;
  }