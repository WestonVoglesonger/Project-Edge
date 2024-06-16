export interface CommentResponse {
  id: number;
  description: string;
  userId: number;
  postId?: number; // Optional because a comment could be on a project or discussion
  discussionId?: number; // Optional because a comment could be on a project or discussion
  createdAt: Date;
  updatedAt: Date;
}

export interface CommentCreate {
  description: string;
  userId: number;
  postId?: number; // Optional because a comment could be on a project or discussion
  discussionId?: number; // Optional because a comment could be on a project or discussion
}

export interface CommentUpdate {
  id: number;
  description: string;
}
