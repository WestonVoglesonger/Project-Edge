import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, of } from "rxjs";
import { Router } from "@angular/router";
import { tap, catchError, map } from "rxjs/operators";

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private tokenKey = "authToken";
  private refreshTokenKey = "refreshToken";
  private refreshTokenTimeout: any;
  public token: string | null = null;
  public tokenRefresh: string | null = null;

  constructor(
    private http: HttpClient,
    private router: Router,
  ) {
    this.token = this.getTokenFromLocalStorage();
    this.tokenRefresh = this.getRefreshTokenFromLocalStorage();
    this.scheduleTokenRefresh();
  }

  fetchCurrentUser(): Observable<any> {
    return this.http.get("/api/auth/users/me", {
      headers: new HttpHeaders({
        Authorization: `Bearer ${this.token}`,
      }),
    });
  }

  verifyToken(): Observable<any> {
    return this.http.get("/api/auth/verify", {
      headers: new HttpHeaders({
        Authorization: `Bearer ${this.token}`,
      }),
    });
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

  private storeTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.tokenKey, accessToken);
    localStorage.setItem(this.refreshTokenKey, refreshToken);
    this.token = accessToken;
    this.tokenRefresh = refreshToken;
  }

  private clearTokens(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.refreshTokenKey);
    this.token = null;
    this.tokenRefresh = null;
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

  login(credentials: { email: string; password: string }): Observable<any> {
    const formData = new FormData();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    return this.http.post("/api/auth/token", formData).pipe(
      tap((response: any) => {
        this.storeTokens(response.access_token, response.refresh_token);
        this.scheduleTokenRefresh();
      }),
    );
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
        this.scheduleTokenRefresh();
      }),
      catchError(() => {
        this.logout();
        return of(null);
      }),
    );
  }

  logout() {
    this.clearTokens();
    this.clearTokenRefreshTimeout();
    this.router.navigate([""]);
  }

  private clearTokenRefreshTimeout() {
    if (this.refreshTokenTimeout) {
      clearTimeout(this.refreshTokenTimeout);
    }
  }
}
