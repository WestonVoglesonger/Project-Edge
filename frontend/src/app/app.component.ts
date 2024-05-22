import { Component, OnInit, OnDestroy } from "@angular/core";
import { Router } from "@angular/router";
import { Subscription, interval } from "rxjs";
import { AuthService } from "./shared/auth.service";

@Component({
  selector: "app-root",
  template: ` <router-outlet> </router-outlet> `,
})
export class AppComponent implements OnInit, OnDestroy {
  private authCheckSubscription!: Subscription;

  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.authService.verifyToken().subscribe({
        next: () => {
          this.startAuthCheck();
        },
        error: () => {
          this.authService.logout();
          this.router.navigate([""]);
        },
      });
    } else {
      this.router.navigate([""]);
    }
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
          // Token is valid
        },
        () => {
          // Token is invalid or expired, log the user out
          this.authService.logout();
          this.router.navigate([""]);
        },
      );
    });
  }
}
