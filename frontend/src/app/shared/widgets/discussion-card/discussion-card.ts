import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Router } from "@angular/router";
import { DiscussionResponse } from "src/app/discussions/discussion.models";
import { DiscussionService } from "src/app/discussions/discussions.service";
import { UserResponse } from "../../users/user.models";

@Component({
  selector: "app-discussion-card",
  templateUrl: "./discussion-card.html",
  styleUrls: ["./discussion-card.css"],
})
export class DiscussionCard {
  @Input() discussion!: DiscussionResponse;
  @Output() viewDetails = new EventEmitter<void>();
  @Input() currentUser!: UserResponse;
  @Output() discussionDeleted = new EventEmitter<number>();

  constructor(
    private router: Router,
    private discussionService: DiscussionService,
  ) {}

  viewDiscussionDetails() {
    this.router.navigate(["/discussions", this.discussion.id]);
  }

  deleteDiscussion(): void {
    if (confirm("Are you sure you want to delete this discussion?")) {
      this.discussionService.deleteDiscussion(this.discussion.id).subscribe(
        (response) => {
          console.log("Discussion deleted successfully", response);
          this.discussionDeleted.emit(this.discussion.id);
        },
        (error) => {
          console.error("Error deleting discussion", error);
        },
      );
    }
  }

  get isAuthor(): boolean {
    return this.discussion.author_id === this.currentUser?.id;
  }

  get mostRecentTime(): Date {
    return new Date(this.discussion.updated_at) >
      new Date(this.discussion.created_at)
      ? new Date(this.discussion.updated_at)
      : new Date(this.discussion.created_at);
  }
}
