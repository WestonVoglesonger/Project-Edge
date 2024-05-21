import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from "rxjs";
import { tap } from "rxjs/operators";
import { UserResponse } from "../shared/users/user.models";

interface AuthResponse {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private apiUrl = "/api/auth";
  private token: string | null = null;
  private currentUser: UserResponse | null = null;

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<AuthResponse> {
    const headers = new HttpHeaders({
      "Content-Type": "application/x-www-form-urlencoded",
    });
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);

    return this.http
      .post<AuthResponse>(`${this.apiUrl}/token`, body.toString(), { headers })
      .pipe(
        tap((response) => {
          this.setToken(response.access_token);
          this.fetchCurrentUser().subscribe();
        }),
      );
  }

  private setToken(token: string): void {
    this.token = token;
    localStorage.setItem("access_token", token);
  }

  getToken(): string | null {
    return this.token || localStorage.getItem("access_token");
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem("access_token");
    this.currentUser = null;
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  fetchCurrentUser(): Observable<UserResponse> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${this.getToken()}`,
    });
    return this.http
      .get<UserResponse>(`${this.apiUrl}/users/me`, { headers })
      .pipe(
        tap((user) => {
          this.currentUser = user;
        }),
      );
  }

  getCurrentUser(): UserResponse | null {
    return this.currentUser;
  }
}
