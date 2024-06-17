import { Component, EventEmitter, Input, Output, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DiscussionResponse } from "src/app/discussions/discussion.models";
import { DiscussionService } from "src/app/discussions/discussions.service";
import { UserResponse } from "../../users/user.models";

@Component({
  selector: "app-discussion-card",
  templateUrl: "./discussion-card.html",
  styleUrls: ["./discussion-card.css"],
})
export class DiscussionCard implements OnInit {
  @Input() discussion!: DiscussionResponse;
  @Input() currentUser!: UserResponse;
  @Output() viewDetails = new EventEmitter<void>();
  @Output() discussionDeleted = new EventEmitter<number>();

  isExpanded: boolean = false;
  isTruncated: boolean = false;

  constructor(
    private router: Router,
    private discussionService: DiscussionService,
  ) {}

  ngOnInit(): void {
    this.isTruncated = this.discussion.description.length > 250;
  }

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

  toggleExpand(): void {
    this.isExpanded = !this.isExpanded;
  }

  get isAuthor(): boolean {
    return this.discussion.author.id === this.currentUser?.id;
  }

  get mostRecentTime(): Date {
    return new Date(this.discussion.updated_at) >
      new Date(this.discussion.created_at)
      ? new Date(this.discussion.updated_at)
      : new Date(this.discussion.created_at);
  }

  get truncatedDescription(): string {
    return this.isExpanded || this.discussion.description.length <= 250
      ? this.discussion.description
      : this.discussion.description.slice(0, 250) + "...";
  }
}
