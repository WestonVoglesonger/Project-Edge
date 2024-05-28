import { Component, OnInit } from '@angular/core';
import { Route, Router } from '@angular/router';

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

  projects = [
    // Example projects data
    {
      title: 'Project 1',
      description: 'Description for project 1',
      categories: ['Web Development'],
      tags: ['Angular', 'TypeScript']
    },
    {
      title: 'Project 2',
      description: 'Description for project 2',
      categories: ['Machine Learning'],
      tags: ['Python', 'TensorFlow']
    }
    // Add more project data as needed
  ];

  constructor(private router: Router) {
  }

  ngOnInit(): void {}

  viewProjectDetails(project: any): void {
    // Implement the logic to view project details
    console.log('Viewing project details for:', project);
  }

  createProject(): void {
    this.router.navigate(['projects/creation'])
  }
}









