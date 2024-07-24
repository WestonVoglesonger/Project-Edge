import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { JoinProjectRequestCreate, Project } from './project.models';

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

  createJoinRequest(joinProjectRequest: JoinProjectRequestCreate): Observable<any> {
    return this.http.post(this.requestsApiUrl, joinProjectRequest);
  }

  deleteJoinRequest(project_id: number, current_user_id: number): Observable<void> {
    return this.http.delete<void>(`${this.requestsApiUrl}/${current_user_id}/${project_id}`);
  }
}