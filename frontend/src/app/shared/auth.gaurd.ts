import { Injectable } from "@angular/core";
import { CanActivate, Router } from "@angular/router";
import { AuthService } from "./auth.service";
import { Observable, map, catchError, of } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router,
  ) {}

  canActivate(): Observable<boolean> | boolean {
    if (this.authService.isLoggedIn()) {
      return this.authService.verifyToken().pipe(
        map(() => true),
        catchError(() => {
          // Attempt to refresh the token
          return this.authService.refreshToken().pipe(
            map(() => true),
            catchError(() => {
              this.authService.logout();
              this.router.navigate([""]);
              return of(false);
            }),
          );
        }),
      );
    } else {
      this.router.navigate([""]);
      return false;
    }
  }
}
