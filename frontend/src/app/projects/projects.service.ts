// project.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { JoinProjectRequestCreate, JoinProjectRequestResponse, Project } from './project.models';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private projectsApiUrl = '/api/projects';
  private requestsApiUrl = '/api/join_request';

  constructor(private http: HttpClient) {}

  createProject(project: Project): Observable<any> {
    return this.http.post(this.projectsApiUrl, project);
  }

  updateProject(id: number, project: Project): Observable<any> {
    return this.http.put(`${this.projectsApiUrl}/${id}`, project);
  }

  getProject(id: number): Observable<any> {
    return this.http.get(`${this.projectsApiUrl}/${id}`);
  }

  getAllProjects(): Observable<any[]> {
    return this.http.get<any[]>(this.projectsApiUrl);
  }

  getProjectsByUser(userId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.projectsApiUrl}?userId=${userId}`);
  }

  deleteProject(id: number): Observable<void> {
    return this.http.delete<void>(`${this.projectsApiUrl}/${id}`);
  }

  createJoinRequest(joinProjectRequest: JoinProjectRequestCreate): Observable<JoinProjectRequestResponse> {
    return this.http.post<JoinProjectRequestResponse>(this.requestsApiUrl, joinProjectRequest);
  }

  deleteJoinRequest(project_id: number, current_user_id: number): Observable<void> {
    return this.http.delete<void>(`${this.requestsApiUrl}/${current_user_id}/${project_id}`);
  }

  getJoinRequestsByProject(projectId: number): Observable<JoinProjectRequestResponse[]> {
    return this.http.get<JoinProjectRequestResponse[]>(`${this.requestsApiUrl}/${projectId}/all`);
  }

  getPendingJoinRequestsByProject(projectId: number): Observable<JoinProjectRequestResponse[]> {
    return this.http.get<JoinProjectRequestResponse[]>(`${this.requestsApiUrl}/${projectId}/pending`);
  }

  approveJoinRequest(requestId: number): Observable<void> {
    return this.http.put<void>(`${this.requestsApiUrl}/${requestId}/approve`, {});
  }

  rejectJoinRequest(requestId: number): Observable<void> {
    return this.http.put<void>(`${this.requestsApiUrl}/${requestId}/reject`, {});
  }
}
