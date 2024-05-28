import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";
import { UserService } from "../shared/users/user.service";
import { Route } from "@angular/router";
import { AuthService } from "../shared/auth.service";
import { UserResponse } from "../shared/users/user.models";

@Component({
  selector: "app-profile",
  templateUrl: "./profile.component.html",
  styleUrls: ["./profile.component.css"],
})
export class ProfileComponent implements OnInit {
  public static Route: Route = {
    path: "profile",
    component: ProfileComponent,
    title: "Profile Page",
  };
  profileForm: FormGroup;
  userId: number | undefined;
  isEditMode: boolean = false;
  selectedFile: File | null = null;
  profilePictureUrl: string | undefined;

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private authService: AuthService,
  ) {
    this.profileForm = this.fb.group({
      first_name: [{ value: "", disabled: true }],
      last_name: [{ value: "", disabled: true }],
      email: [{ value: "", disabled: true }],
      bio: [{ value: "", disabled: true }],
      accepted_community_agreement: [{ value: true }],
    });
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe((user: UserResponse) => {
      console.log("User:", user);
      this.userId = user.id;
      this.profileForm.patchValue({
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        email: user.email || "",
        bio: user.bio || "",
        accepted_community_agreement: user.accepted_community_agreement,
      });
      if (user.profile_picture) {
        this.profilePictureUrl = user.profile_picture; // Directly use the URL from the API
      }
    });
  }

  onEdit() {
    this.isEditMode = !this.isEditMode;
    if (this.isEditMode) {
      this.profileForm.enable();
      this.profileForm.get("email")?.disable();
    } else {
      this.profileForm.disable();
    }
  }

  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
      this.profilePictureUrl = URL.createObjectURL(this.selectedFile!);
    }
  }

  onSubmit() {
    if (this.userId) {
      const profileData = this.profileForm.getRawValue();
      const formData = new FormData();

      // Append profile data to FormData
      for (const key in profileData) {
        if (profileData.hasOwnProperty(key) && profileData[key] !== null) {
          formData.append(key, profileData[key]);
        }
      }

      // Append the selected file to FormData
      if (this.selectedFile) {
        formData.append("profile_picture", this.selectedFile);
      }

      // Log the FormData key-value pairs to the console
      formData.forEach((value, key) => {
        console.log(`${key}: ${value}`);
      });

      this.userService.updateUserProfile(this.userId, formData).subscribe({
        next: () => {
          this.isEditMode = false;
          this.profileForm.disable();
        },
        error: (err) => {
          console.error("Error updating profile:", err);
        },
      });
    }
  }
}
