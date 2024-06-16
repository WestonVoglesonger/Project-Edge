import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { CommentCreate, CommentUpdate } from "./comment.models";

@Injectable({
  providedIn: "root",
})
export class CommentService {
  private apiUrl = "/api/comments";

  constructor(private http: HttpClient) {}

  createComment(comment: CommentCreate): Observable<any> {
    return this.http.post(this.apiUrl, comment);
  }

  updateComment(comment_id: number, comment: CommentUpdate): Observable<any> {
    return this.http.put(`${this.apiUrl}/${comment_id}`, comment);
  }

  getComment(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/${id}`);
  }

  getCommentsByDiscussion(discussionId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?discussionId=${discussionId}`);
  }

  getCommentsByProject(projectId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}?projectId=${projectId}`);
  }

  deleteComment(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
