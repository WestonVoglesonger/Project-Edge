import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from "rxjs";
import { tap } from "rxjs/operators";

interface AuthResponse {
  access_token: string;
  token_type: string;
}

@Injectable({
  providedIn: "root",
})
export class AuthService {
  private apiUrl = "/api/auth/token";
  private token: string | null = null;

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<AuthResponse> {
    const headers = new HttpHeaders({
      "Content-Type": "application/x-www-form-urlencoded",
    });
    const body = new URLSearchParams();
    body.set("username", username);
    body.set("password", password);

    return this.http
      .post<AuthResponse>(this.apiUrl, body.toString(), { headers })
      .pipe(tap((response) => this.setToken(response.access_token)));
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
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
