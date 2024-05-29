import { Component, OnInit } from '@angular/core';
import { Route, Router } from '@angular/router';
import { ProjectService } from './projects.service';

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
  projects: any[] = [];

  constructor(private router: Router, private projectService: ProjectService) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.projectService.getAllProjects().subscribe(
      projects => {
        this.projects = projects;
      },
      error => {
        console.error('Error fetching projects', error);
      }
    );
  }

  viewProjectDetails(project: any): void {
    // Implement the logic to view project details
    console.log('Viewing project details for:', project);
  }

  createProject(): void {
    this.router.navigate(['projects/new']);
  }

  editProject(project: any): void {
    this.router.navigate([`projects/${project.id}`]);
  }
}