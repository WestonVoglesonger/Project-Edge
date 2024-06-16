import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Router } from "@angular/router";
import { ProjectResponse } from "src/app/projects/project.models";

@Component({
  selector: "app-project-card",
  templateUrl: "./project-card.html",
  styleUrls: ["./project-card.css"],
})
export class ProjectCard {
  @Input() project!: ProjectResponse;
  @Output() viewDetails = new EventEmitter<void>();

  constructor(private router: Router) {}

  viewProjectDetails() {
    this.router.navigate(["/projects", this.project.id]);
  }
}
