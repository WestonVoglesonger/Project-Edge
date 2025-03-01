import { ChangeDetectorRef, Component, OnInit } from "@angular/core";
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
  isLoading: boolean = true;

  constructor(
    private discussionService: DiscussionService,
    private router: Router,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
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
    this.isLoading = true;
    this.discussionService.getAllDiscussions().subscribe(
      (discussions: DiscussionResponse[]) => {
        this.discussions = discussions.sort(
          (a, b) =>
            new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
        );
        this.filteredDiscussions = this.discussions;
        this.isLoading = false;
        this.cdr.markForCheck(); // Ensure view is updated
      },
      (error) => {
        console.error("Error loading discussions", error);
        this.isLoading = false;
        this.cdr.markForCheck(); // Ensure view is updated even on error
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
    if (!this.searchQuery) {
      this.filteredDiscussions = [...this.discussions];
      return;
    }

    const searchTermLower = this.searchQuery.toLowerCase();
    this.filteredDiscussions = this.discussions.filter(
      (discussion) =>
        discussion.title.toLowerCase().includes(searchTermLower) ||
        discussion.description.toLowerCase().includes(searchTermLower),
    );
  }

  clearSearch() {
    this.searchQuery = "";
    this.filterDiscussions();
  }

  handleDiscussionDeleted(discussionId: number): void {
    this.discussions = this.discussions.filter(
      (discussion) => discussion.id !== discussionId,
    );
    this.filteredDiscussions = this.filteredDiscussions.filter(
      (discussion) => discussion.id !== discussionId,
    );
    this.cdr.markForCheck(); // Manually trigger change detection
  }
}
