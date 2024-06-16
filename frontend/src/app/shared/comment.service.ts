import { Injectable } from "@angular/core";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { CommentCreate, CommentUpdate } from "./comment.models";

@Injectable({
  providedIn: "root",
})
export class CommentService {
  private baseUrl = "/api/comments";

  constructor(private http: HttpClient) {}

  createComment(commentData: CommentCreate): Observable<Comment> {
    return this.http
      .post<Comment>(this.baseUrl, commentData)
      .pipe(catchError(this.handleError));
  }

  getCommentsByPost(postId: number): Observable<Comment[]> {
    return this.http
      .get<Comment[]>(`${this.baseUrl}?postId=${postId}`)
      .pipe(catchError(this.handleError));
  }

  getCommentsByDiscussion(discussionId: number): Observable<Comment[]> {
    return this.http
      .get<Comment[]>(`${this.baseUrl}?discussionId=${discussionId}`)
      .pipe(catchError(this.handleError));
  }

  updateComment(
    commentId: number,
    commentUpdate: CommentUpdate,
  ): Observable<Comment> {
    return this.http
      .put<Comment>(`${this.baseUrl}/${commentId}`, commentUpdate)
      .pipe(catchError(this.handleError));
  }

  deleteComment(commentId: number): Observable<Comment> {
    return this.http
      .delete<Comment>(`${this.baseUrl}/${commentId}`)
      .pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = "Unknown error!";
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(errorMessage);
  }
}
