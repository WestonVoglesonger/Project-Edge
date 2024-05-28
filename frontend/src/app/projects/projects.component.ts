import { Component } from '@angular/core';
import { Route } from '@angular/router';

@Component({
  selector: 'app-projects',
  templateUrl: './projects.component.html',
  styleUrls: ['./projects.component.css']
})
export class ProjectsComponent {
  public static Route: Route = {
    path: "projects",
    component: ProjectsComponent,
    title: "Projects Page",
  };
}
