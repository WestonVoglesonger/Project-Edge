// src/app/projects/projects.component.ts
import { Component, OnInit } from '@angular/core';
import { Route, Router } from '@angular/router';
import { ProjectService } from './projects.service';
import { ProjectResponse } from './project.models';

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent implements OnInit {
  public static Route: Route = {
    path: "projects",
    component: ProjectsComponent,
    title: "Projects Page",
  };

  projects: ProjectResponse[] = [];

  constructor(
    private projectService: ProjectService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.projectService.getAllProjects().subscribe(
      (projects: ProjectResponse[]) => {
        this.projects = projects;
      },
      error => {
        console.error('Error loading projects', error);
      }
    );
  }

  viewProjectDetails(project: ProjectResponse): void {
    this.router.navigate(['/projects', project.id]);
  }

  createProject(): void {
    this.router.navigate(['/projects/new']);
  }
}
