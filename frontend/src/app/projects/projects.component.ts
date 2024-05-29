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
  filteredProjects: ProjectResponse[] = [];
  searchQuery: string = '';

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
        this.filteredProjects = projects;
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

  filterProjects(): void {
    this.filteredProjects = this.projects.filter(project =>
      project.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
      project.description.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
  }  
}
