import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { Router, ActivatedRoute, Route } from "@angular/router";
import { AuthService } from "../shared/auth.service";
import { UserService } from "../shared/users/user.service";

@Component({
  selector: "app-auth",
  templateUrl: "./auth.component.html",
  styleUrls: ["./auth.component.css"],
})
export class AuthComponent implements OnInit {
  public static Route: Route = {
    path: "",
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
    private route: ActivatedRoute,
  ) {
    this.loginForm = this.fb.group({
      email: ["", [Validators.required, Validators.email]],
      password: ["", [Validators.required, Validators.minLength(6)]],
    });

    this.createAccountForm = this.fb.group({
      email: ["", [Validators.required, Validators.email]],
      password: ["", [Validators.required, Validators.minLength(6)]],
    });
  }

  ngOnInit(): void {
    this.route.url.subscribe(() => {
      this.resetComponent();
    });
  }

  private resetComponent(): void {
    this.isLoginMode = true;
    this.errorMessage = null;
    this.loginForm.reset();
    this.createAccountForm.reset();
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
      const { email, password } = this.loginForm.value;
      this.authService.login(email, password).subscribe(
        () => this.router.navigate(["/home"]),
        (error) => (this.errorMessage = "Invalid email or password"),
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
        error: (error: string | null) => {
          this.errorMessage = error; // Set the specific error message
        },
      });
    }
  }
}
