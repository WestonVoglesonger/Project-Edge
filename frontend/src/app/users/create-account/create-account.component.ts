import { Component } from "@angular/core";
import { Route } from "@angular/router";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { UserService } from "../user.service"; // Adjust the import path as needed

@Component({
  selector: "app-create-account",
  templateUrl: "./create-account.component.html",
  styleUrls: ["./create-account.component.css"],
})
export class CreateAccountComponent {
  public static Route: Route = {
    path: "create-account",
    component: CreateAccountComponent,
    title: "Create Account Page",
  };

  createAccountForm: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
  ) {
    this.createAccountForm = this.fb.group({
      email: ["", [Validators.required, Validators.email]],
      password: ["", [Validators.required, Validators.minLength(6)]],
    });
  }

  onSubmit() {
    if (this.createAccountForm.valid) {
      const formData = this.createAccountForm.value;
      formData.email = formData.email.toLowerCase(); // Convert email to lowercase
      this.userService.createUser(formData).subscribe({
        next: (response: any) => {
          console.log("User created successfully", response);
          this.errorMessage = null; // Clear any previous error message
          // Handle successful response (e.g., redirect to a login page)
        },
        error: (error: any) => {
          console.error("Error creating user", error);
          this.errorMessage = error; // Set the specific error message
        },
      });
    }
  }
}
