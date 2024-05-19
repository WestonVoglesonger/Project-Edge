import { Component } from "@angular/core";
import { Route, Router } from "@angular/router";
import { AuthService } from "src/app/shared/auth.service";

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.css"],
})
export class LoginComponent {
  public static Route: Route = {
    path: "login",
    component: LoginComponent,
    title: "Login Page",
  };

  username: string = "";
  password: string = "";
  errorMessage: string = "";

  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  login(): void {
    this.authService.login(this.username, this.password).subscribe(
      () => this.router.navigate(["/"]),
      (error) => (this.errorMessage = "Invalid username or password"),
    );
  }
}
