import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Router } from "@angular/router";
import { ProjectResponse } from "src/app/projects/project.models";
import { ProjectService } from "src/app/projects/projects.service";

@Component({
  selector: "app-project-card",
  templateUrl: "./project-card.html",
  styleUrls: ["./project-card.css"],
})
export class ProjectCard {
  @Input() project!: ProjectResponse;
  @Output() viewDetails = new EventEmitter<void>();

  constructor(
    private router: Router,
    private projectService: ProjectService,
  ) {}

  viewProjectDetails() {
    this.router.navigate(["/projects", this.project.id]);
  }

  deleteProject(): void {
    if (confirm("Are you sure you want to delete this project?")) {
      this.projectService.deleteProject(this.project.id).subscribe(
        (response) => {
          console.log("Project deleted successfully", response);
        },
        (error) => {
          console.error("Error deleting project", error);
        },
      );
    }
  }
}
