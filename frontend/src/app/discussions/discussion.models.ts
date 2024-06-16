export interface Discussion {
  title: string;
  description: string;
  author_id: number;
}

export interface DiscussionResponse {
  id: number;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
  author_id: number;
}
