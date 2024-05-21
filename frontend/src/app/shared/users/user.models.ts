export interface ProfileForm {
  email: string;
  password: string;
  accepted_community_agreement: boolean;
}

export interface UserResponse {
  id?: number;
  first_name?: string;
  last_name?: string;
  email: string;
  accepted_community_agreement: boolean;
  bio?: string;
  profile_picture?: string;
  areas_of_interest?: number[];
}
