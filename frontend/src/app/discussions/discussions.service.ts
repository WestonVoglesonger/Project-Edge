import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Discussion, DiscussionResponse } from "./discussion.models";

@Injectable({
  providedIn: "root",
})
export class DiscussionService {
  private apiUrl = "/api/discussions";

  constructor(private http: HttpClient) {}

  createDiscussion(discussion: Discussion): Observable<DiscussionResponse> {
    return this.http.post<DiscussionResponse>(this.apiUrl, discussion);
  }

  updateDiscussion(
    id: number,
    discussion: Discussion,
  ): Observable<DiscussionResponse> {
    return this.http.put<DiscussionResponse>(
      `${this.apiUrl}/${id}`,
      discussion,
    );
  }

  getDiscussion(id: number): Observable<DiscussionResponse> {
    return this.http.get<DiscussionResponse>(`${this.apiUrl}/${id}`);
  }

  getAllDiscussions(): Observable<DiscussionResponse[]> {
    return this.http.get<DiscussionResponse[]>(this.apiUrl);
  }

  deleteDiscussion(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
