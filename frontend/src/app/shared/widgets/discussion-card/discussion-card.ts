import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Router } from "@angular/router";
import { DiscussionResponse } from "src/app/discussions/discussion.models";

@Component({
  selector: "app-discussion-card",
  templateUrl: "./discussion-card.html",
  styleUrls: ["./discussion-card.css"],
})
export class DiscussionCard {
  @Input() discussion!: DiscussionResponse;
  @Output() viewDetails = new EventEmitter<void>();

  constructor(private router: Router) {}

  viewDiscussionDetails() {
    this.router.navigate(["/discussions", this.discussion.id]);
  }
}
