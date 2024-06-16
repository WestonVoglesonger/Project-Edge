import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Router } from "@angular/router";
import { CommentResponse } from "../../comment.models";

@Component({
  selector: "app-comment-card",
  templateUrl: "./comment-card.html",
  styleUrls: ["./comment-card.css"],
})
export class CommentCard {
  @Input() comment!: CommentResponse;
  @Output() viewOrEditComment = new EventEmitter<number>();

  constructor(private router: Router) {}

  viewOrEditCommentDetails() {
    this.router.navigate(["/comments", this.comment.id]);
  }
}
