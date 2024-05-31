import {
  HttpClient,
  HttpHeaders,
  HttpErrorResponse,
  HttpParams,
} from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { ProfileForm, UserResponse } from "./user.models";

@Injectable({
  providedIn: "root",
})
export class UserService {
  private apiUrl = "/api/user";

  constructor(private http: HttpClient) {}

  createUser(user: ProfileForm): Observable<UserResponse> {
    const headers = new HttpHeaders({ "Content-Type": "application/json" });
    return this.http
      .post<UserResponse>(this.apiUrl, user, { headers })
      .pipe(catchError(this.handleError));
  }

  getUserProfile(userId: number): Observable<ProfileForm> {
    const headers = new HttpHeaders({ "Content-Type": "application/json" });
    return this.http
      .get<ProfileForm>(`${this.apiUrl}/${userId}`, { headers })
      .pipe(catchError(this.handleError));
  }

  updateUserProfile(
    userId: number,
    formData: FormData,
  ): Observable<UserResponse> {
    return this.http
      .put<UserResponse>(`${this.apiUrl}/${userId}`, formData)
      .pipe(catchError(this.handleError));
  }

  searchUsers(name: string): Observable<UserResponse[]> {
    const headers = new HttpHeaders({ "Content-Type": "application/json" });
    const params = new HttpParams().set("name", name);
    return this.http
      .get<UserResponse[]>(`${this.apiUrl}/search`, { params, headers })
      .pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = "An unknown error occurred!";
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      if (error.status === 400 && error.error.detail) {
        errorMessage = error.error.detail;
      } else {
        errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
      }
    }
    console.error(errorMessage);
    return throwError(errorMessage);
  }
}
