import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Route, Router } from '@angular/router';
import { ProjectService } from './projects.service';
import { ProjectResponse } from './project.models';
import { AuthService } from '../shared/auth.service';
import { UserResponse } from '../shared/users/user.models';

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
  currentUser!: UserResponse;

  constructor(
    private projectService: ProjectService,
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe(
      (user: UserResponse) => {
        this.currentUser = user;
      },
      (error: any) => {
        console.error("Error fetching current user", error);
      },
    );
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

  createProject(): void {
    this.router.navigate(['/projects/new']);
  }

  filterProjects(): void {
    this.filteredProjects = this.projects.filter(project =>
      project.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
      project.description.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
  }

  handleProjectDeleted(projectId: number): void {
    this.projects = this.projects.filter(project => project.id !== projectId);
    this.filteredProjects = this.filteredProjects.filter(project => project.id !== projectId);
    this.cdr.markForCheck(); // Manually trigger change detection
  }
}
