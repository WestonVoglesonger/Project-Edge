import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Project } from './project.models';

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private apiUrl = '/api/projects';

  constructor(private http: HttpClient) {}

  createProject(project: Project): Observable<any> {
    return this.http.post(this.apiUrl, project);
  }

  updateProject(id: number, project: Project): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, project);
  }

  getProject(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/${id}`);
  }

  getAllProjects(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  deleteProject(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}