import { Injectable, NgZone } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";
import { Router } from "@angular/router";
import { tap, catchError } from "rxjs/operators";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private tokenKey = "authToken";
  private refreshTokenKey = "refreshToken";
  private refreshTokenTimeout: any;
  private logoutTimeout: any;
  private inactivityTimeout: any;
  private inactivityDuration = 5 * 60 * 1000; // 5 minutes of inactivity for testing
  public token: string | null = null;
  public tokenRefresh: string | null = null;

  constructor(
    private http: HttpClient,
    private router: Router,
    private ngZone: NgZone,
  ) {
    this.token = this.getTokenFromLocalStorage();
    this.tokenRefresh = this.getRefreshTokenFromLocalStorage();
  }

  fetchCurrentUser(): Observable<any> {
    return this.http.get("/api/auth/users/me", {
      headers: new HttpHeaders({
        Authorization: `Bearer ${this.token}`,
      }),
    });
  }

  verifyToken(): Observable<any> {
    return this.http
      .get("/api/auth/verify", {
        headers: new HttpHeaders({
          Authorization: `Bearer ${this.token}`,
        }),
      })
      .pipe(
        tap(() => {
          // Token is valid
        }),
        catchError(() => {
          // Token is invalid or expired
          return of(null);
        }),
      );
  }

  isLoggedIn(): boolean {
    return this.token !== null;
  }

  private getTokenFromLocalStorage(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  private getRefreshTokenFromLocalStorage(): string | null {
    return localStorage.getItem(this.refreshTokenKey);
  }

  private clearTokens(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshTokenKey);
    this.token = null;
    this.tokenRefresh = null;
    this.clearTokenRefreshTimeout();
    this.clearLogoutTimeout();
    this.clearInactivityTimeout();
  }

  private getTokenExpiryTime(token: string | null): number {
    if (!token) return 0;
    const jwtPayload = JSON.parse(atob(token.split(".")[1]));
    return jwtPayload.exp * 1000; // Convert to milliseconds
  }

  private scheduleTokenRefresh() {
    const tokenExpiryTime = this.getTokenExpiryTime(this.token);
    const timeout = tokenExpiryTime - Date.now() - 60000; // Refresh 1 minute before expiry
    if (timeout > 0) {
      this.refreshTokenTimeout = setTimeout(() => {
        this.refreshToken().subscribe();
      }, timeout);
    }
  }

  private scheduleLogout() {
    const tokenExpiryTime = this.getTokenExpiryTime(this.token);
    const timeout = tokenExpiryTime - Date.now();
    if (timeout > 0) {
      this.logoutTimeout = setTimeout(() => {
        this.logout();
      }, timeout);
    }
  }

  private resetInactivityTimer() {
    this.clearInactivityTimeout();
    this.inactivityTimeout = setTimeout(() => {
      this.logout();
    }, this.inactivityDuration);
  }

  private setupActivityListeners() {
    ["click", "mousemove", "keydown", "scroll", "touchstart"].forEach(
      (event) => {
        document.addEventListener(event, () => this.resetInactivityTimer());
      },
    );
  }

  login(credentials: { email: string; password: string }): Observable<any> {
    const formData = new FormData();
    formData.append("username", credentials.email.toLowerCase()); // Convert email to lowercase
    formData.append("password", credentials.password);

    return this.http.post("/api/auth/token", formData).pipe(
      tap((response: any) => {
        if (response.access_token && response.refresh_token) {
          this.storeTokens(response.access_token, response.refresh_token);
        } else {
          console.error("Tokens are missing in the response:", response);
        }
      }),
    );
  }

  private storeTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.tokenKey, accessToken);
    localStorage.setItem(this.refreshTokenKey, refreshToken);
    this.token = accessToken;
    this.tokenRefresh = refreshToken;
    this.scheduleTokenRefresh();
    this.scheduleLogout();
  }

  refreshToken(): Observable<any> {
    const refreshToken = this.getRefreshTokenFromLocalStorage();
    if (!refreshToken) {
      this.logout();
      return of(null);
    }

    const formData = new FormData();
    formData.append("refresh_token", refreshToken);

    return this.http.post("/api/auth/refresh-token", formData).pipe(
      tap((response: any) => {
        this.storeTokens(response.access_token, response.refresh_token);
      }),
      catchError(() => {
        this.logout();
        return of(null);
      }),
    );
  }

  logout() {
    this.clearTokens();
    this.router.navigate([""]);
  }

  private clearTokenRefreshTimeout() {
    if (this.refreshTokenTimeout) {
      clearTimeout(this.refreshTokenTimeout);
    }
  }

  private clearLogoutTimeout() {
    if (this.logoutTimeout) {
      clearTimeout(this.logoutTimeout);
    }
  }

  private clearInactivityTimeout() {
    if (this.inactivityTimeout) {
      clearTimeout(this.inactivityTimeout);
    }
  }

  initializeAuthState(): Observable<any> {
    if (this.isLoggedIn()) {
      return this.verifyToken().pipe(
        tap(() => {
          // Token is valid, setting user as logged in
          this.setUserAsAuthenticated();
        }),
        catchError(() => {
          return this.refreshToken().pipe(
            tap(() => {
              // Token refreshed, setting user as logged in
              this.setUserAsAuthenticated();
            }),
            catchError(() => {
              this.logout();
              return of(null);
            }),
          );
        }),
      );
    }
    return of(null);
  }

  private setUserAsAuthenticated(): void {
    // Assuming fetchCurrentUser sets some user state in the application
    this.fetchCurrentUser().subscribe(() => {
      // Navigate to home after user is set
      this.router.navigate(["/home"]);
    });
  }
}
