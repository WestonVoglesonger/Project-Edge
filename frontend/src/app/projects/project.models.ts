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
    team_members: UserResponse[];
    project_leaders: UserResponse[];
  }