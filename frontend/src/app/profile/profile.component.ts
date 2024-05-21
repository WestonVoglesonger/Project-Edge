import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { UserService } from "../shared/users/user.service";
import { Route } from "@angular/router";
import { AuthService } from "../shared/auth.service";

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

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private authService: AuthService,
  ) {
    this.profileForm = this.fb.group({
      first_name: ["", Validators.required],
      last_name: ["", Validators.required],
      email: [
        { value: "", disabled: true },
        [Validators.required, Validators.email],
      ],
      bio: [""],
      profile_picture: [""],
      accepted_community_agreement: [false, Validators.requiredTrue],
    });
  }

  ngOnInit(): void {
    const currentUser = this.authService.getCurrentUser();
    if (currentUser) {
      this.userId = currentUser.id;
      this.userService.getUserProfile(this.userId!).subscribe((profile) => {
        this.profileForm.patchValue(profile);
      });
    } else {
      this.authService.fetchCurrentUser().subscribe((user) => {
        this.userId = user.id;
        this.userService.getUserProfile(this.userId!).subscribe((profile) => {
          this.profileForm.patchValue(profile);
        });
      });
    }
  }

  onSubmit(): void {
    if (this.profileForm.valid && this.userId !== undefined) {
      this.userService
        .updateUserProfile(this.userId, this.profileForm.getRawValue())
        .subscribe({
          next: () => alert("Profile updated successfully!"),
          error: (error) => alert("An error occurred: " + error),
        });
    }
  }
}
