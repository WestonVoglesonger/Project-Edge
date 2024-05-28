import { Component, OnInit, OnDestroy } from "@angular/core";
import { Router } from "@angular/router";
import { Subscription, interval } from "rxjs";
import { AuthService } from "./shared/auth.service";

@Component({
  selector: "app-root",
  template: `<router-outlet> </router-outlet>`,
})
export class AppComponent implements OnInit, OnDestroy {
  private authCheckSubscription!: Subscription;

  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.authService.initializeAuthState().subscribe({
      next: () => {
        this.startAuthCheck();
      },
      error: () => {
        this.authService.logout();
        this.router.navigate([""]);
      },
    });
  }

  ngOnDestroy(): void {
    if (this.authCheckSubscription) {
      this.authCheckSubscription.unsubscribe();
    }
  }

  startAuthCheck(): void {
    this.authCheckSubscription = interval(60000).subscribe(() => {
      this.authService.verifyToken().subscribe(
        () => {
          console.log("Token is valid and user is logged in");
        },
        () => {
          this.authService.refreshToken().subscribe(
            () => {
              console.log("Token refreshed");
            },
            () => {
              console.log("Token refresh failed, logging out");
              this.authService.logout();
              this.router.navigate([""]);
            },
          );
        },
      );
    });
  }
}
