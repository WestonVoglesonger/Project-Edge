import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
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
    this.authService.fetchCurrentUser().subscribe((user: UserResponse) => {
      this.userId = user.id;
      this.profileForm.patchValue(user);
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

  onSubmit() {
    if (this.profileForm.valid && this.userId) {
      this.userService
        .updateUserProfile(this.userId, this.profileForm.value)
        .subscribe(() => {
          this.isEditMode = false;
          this.profileForm.disable();
        });
    }
  }
}
