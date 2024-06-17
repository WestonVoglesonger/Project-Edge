import { Component, OnInit } from "@angular/core";
import { Route, Router } from "@angular/router";
import { DiscussionResponse } from "./discussion.models";
import { DiscussionService } from "./discussions.service";
import { UserResponse } from "../shared/users/user.models";
import { AuthService } from "../shared/auth.service";

@Component({
  selector: "app-discussions",
  templateUrl: "./discussions.component.html",
  styleUrls: ["./discussions.component.css"],
})
export class DiscussionsComponent implements OnInit {
  public static Route: Route = {
    path: "discussions",
    component: DiscussionsComponent,
    title: "Discussions Page",
  };

  discussions: DiscussionResponse[] = [];
  filteredDiscussions: DiscussionResponse[] = [];
  searchQuery: string = "";
  currentUser!: UserResponse;

  constructor(
    private discussionService: DiscussionService,
    private router: Router,
    private authService: AuthService,
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
    this.loadDiscussions();
  }

  loadDiscussions(): void {
    this.discussionService.getAllDiscussions().subscribe(
      (discussions: DiscussionResponse[]) => {
        this.discussions = discussions;
        this.filteredDiscussions = discussions;
      },
      (error) => {
        console.error("Error loading discussions", error);
      },
    );
  }

  viewDiscussionDetails(discussion: DiscussionResponse): void {
    this.router.navigate(["/discussions", discussion.id]);
  }

  createDiscussion(): void {
    this.router.navigate(["/discussions/new"]);
  }

  filterDiscussions(): void {
    this.filteredDiscussions = this.discussions.filter(
      (discussion) =>
        discussion.title
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase()) ||
        discussion.description
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase()),
    );
  }
}
