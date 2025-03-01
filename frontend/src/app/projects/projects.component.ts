import { Component, OnInit, ChangeDetectorRef } from "@angular/core";
import { Route, Router } from "@angular/router";
import { ProjectService } from "./projects.service";
import { ProjectResponse } from "./project.models";
import { AuthService } from "../shared/auth.service";
import { UserResponse } from "../shared/users/user.models";

@Component({
  selector: "app-projects",
  templateUrl: "./projects.component.html",
  styleUrls: ["./projects.component.css"],
})
export class ProjectsComponent implements OnInit {
  public static Route: Route = {
    path: "projects",
    component: ProjectsComponent,
    title: "Projects Page",
  };

  projects: ProjectResponse[] = [];
  filteredProjects: ProjectResponse[] = [];
  searchQuery: string = "";
  currentUser!: UserResponse;
  isLoading: boolean = true;

  constructor(
    private projectService: ProjectService,
    private router: Router,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe(
      (user: UserResponse) => {
        this.currentUser = user;
      },
      (error: any) => {
        console.error("Error fetching current user", error);
      }
    );
    this.loadProjects();
  }

  loadProjects(): void {
    this.isLoading = true;
    this.projectService.getAllProjects().subscribe(
      (projects: ProjectResponse[]) => {
        this.projects = projects.sort(
          (a, b) =>
            new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
        );
        this.filteredProjects = this.projects;
        this.isLoading = false;
        this.cdr.markForCheck(); // Ensure view is updated
      },
      (error) => {
        console.error("Error loading projects", error);
        this.isLoading = false;
        this.cdr.markForCheck(); // Ensure view is updated even on error
      }
    );
  }

  createProject(): void {
    this.router.navigate(["/projects/new"]);
  }

  filterProjects(): void {
    if (!this.searchQuery) {
      this.filteredProjects = [...this.projects];
      return;
    }

    const searchTermLower = this.searchQuery.toLowerCase();
    this.filteredProjects = this.projects.filter(
      (project) =>
        project.name.toLowerCase().includes(searchTermLower) ||
        project.description.toLowerCase().includes(searchTermLower) ||
        project.team_members.some(
          (member) =>
            member.first_name?.toLowerCase().includes(searchTermLower) ||
            member.last_name?.toLowerCase().includes(searchTermLower) ||
            member.email.toLowerCase().includes(searchTermLower)
        )
    );
  }

  clearSearch(): void {
    this.searchQuery = "";
    this.filterProjects();
  }

  handleProjectDeleted(projectId: number): void {
    this.projects = this.projects.filter((project) => project.id !== projectId);
    this.filteredProjects = this.filteredProjects.filter(
      (project) => project.id !== projectId
    );
    this.cdr.markForCheck(); // Manually trigger change detection
  }
}
