import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Router } from "@angular/router";
import { ProjectResponse } from "src/app/projects/project.models";
import { ProjectService } from "src/app/projects/projects.service";
import { UserResponse } from "../../users/user.models";

@Component({
  selector: "app-project-card",
  templateUrl: "./project-card.html",
  styleUrls: ["./project-card.css"],
})
export class ProjectCard {
  @Input() project!: ProjectResponse;
  @Input() currentUser!: UserResponse;
  @Output() viewDetails = new EventEmitter<void>();
  @Output() projectDeleted = new EventEmitter<number>();

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
          this.projectDeleted.emit(this.project.id);
        },
        (error) => {
          console.error("Error deleting project", error);
        },
      );
    }
  }

  isLeader(): boolean {
    return this.project.project_leaders.some(
      (leader) => leader.id === this.currentUser.id,
    );
  }

  get mostRecentTime(): Date {
    return new Date(this.project.updated_at) > new Date(this.project.created_at)
      ? new Date(this.project.updated_at)
      : new Date(this.project.created_at);
  }
}
