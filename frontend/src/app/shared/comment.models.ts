export interface CommentResponse {
  id: number;
  description: string;
  user_id: number;
  project_id?: number; // Optional because a comment could be on a project or discussion
  discussion_id?: number; // Optional because a comment could be on a project or discussion
  createdAt: Date;
  updatedAt: Date;
}

export interface CommentCreate {
  description: string;
  user_id: number;
  project_id?: number; // Optional because a comment could be on a project or discussion
  discussion_id?: number; // Optional because a comment could be on a project or discussion
}

export interface CommentUpdate {
  description: string;
}
