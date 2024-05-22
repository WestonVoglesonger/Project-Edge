export interface ProfileForm {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  bio?: string;
  profile_picture?: File;
  accepted_community_agreement: boolean;
}

export interface UserResponse {
  id?: number;
  first_name?: string;
  last_name?: string;
  email: string;
  accepted_community_agreement: boolean;
  bio?: string;
  profile_picture?: File;
}
