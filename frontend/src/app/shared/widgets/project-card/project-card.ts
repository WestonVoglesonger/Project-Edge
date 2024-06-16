import { Component, EventEmitter, Input, Output } from "@angular/core";
import { ProjectResponse } from "src/app/projects/project.models";

@Component({
  selector: "app-project-card",
  templateUrl: "./project-card.html",
  styleUrls: ["./project-card.css"],
})
export class ProjectCard {
  @Input() project!: ProjectResponse;
  @Output() viewDetails = new EventEmitter<void>();

  viewProjectDetails() {
    this.viewDetails.emit();
  }
}
