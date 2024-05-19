import { Component } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { Route, Router } from "@angular/router";
import { AuthService } from "../shared/auth.service";
import { UserService } from "../users/user.service";

@Component({
  selector: "app-auth",
  templateUrl: "./auth.component.html",
  styleUrls: ["./auth.component.css"],
})
export class AuthComponent {
  public static Route: Route = {
    path: "auth",
    component: AuthComponent,
    title: "Authorization Page",
  };

  loginForm: FormGroup;
  createAccountForm: FormGroup;
  isLoginMode = true;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private userService: UserService,
    private router: Router,
  ) {
    this.loginForm = this.fb.group({
      email: ["", [Validators.required]],
      password: ["", [Validators.required, Validators.minLength(6)]],
    });

    this.createAccountForm = this.fb.group({
      email: ["", [Validators.required, Validators.email]],
      password: ["", [Validators.required, Validators.minLength(6)]],
    });
  }

  onSwitchMode() {
    this.isLoginMode = !this.isLoginMode;
    this.errorMessage = null;
  }

  onSubmit() {
    if (this.isLoginMode) {
      this.login();
    } else {
      this.createAccount();
    }
  }

  login() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      this.authService.login(username, password).subscribe(
        () => this.router.navigate(["/"]),
        (error) => (this.errorMessage = "Invalid username or password"),
      );
    }
  }

  createAccount() {
    if (this.createAccountForm.valid) {
      const formData = this.createAccountForm.value;
      formData.email = formData.email.toLowerCase(); // Convert email to lowercase
      this.userService.createUser(formData).subscribe({
        next: () => {
          this.errorMessage = null; // Clear any previous error message
          this.isLoginMode = true; // Switch to login mode after successful registration
        },
        error: (error) => {
          this.errorMessage = error; // Set the specific error message
        },
      });
    }
  }
}
