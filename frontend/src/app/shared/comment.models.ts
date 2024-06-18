import { UserResponse } from "./users/user.models";

export interface CommentResponse {
  id: number;
  description: string;
  author: UserResponse;
  project_id: number | null; // Optional because a comment could be on a project or discussion
  discussion_id: number | null; // Optional because a comment could be on a project or discussion
  created_at: Date;
  updated_at: Date;
}

export interface CommentCreate {
  description: string;
  author_id: number;
  project_id: number | null; // Optional because a comment could be on a project or discussion
  discussion_id: number | null; // Optional because a comment could be on a project or discussion
  parent_id: number | null; // Optional because a comment could be a reply to a project or discussion
}

export interface CommentUpdate {
  description: string;
}
