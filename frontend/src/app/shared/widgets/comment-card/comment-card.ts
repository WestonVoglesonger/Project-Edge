import { Component, Input, OnInit } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl,
} from "@angular/forms";
import { CommentResponse, CommentUpdate } from "../../comment.models";
import { CommentService } from "../../comment.service";
import { AuthService } from "../../auth.service";
import { Router } from "@angular/router";
import { UserResponse } from "../../users/user.models";

@Component({
  selector: "app-comment-card",
  templateUrl: "./comment-card.html",
  styleUrls: ["./comment-card.css"],
})
export class CommentCard implements OnInit {
  @Input() comment!: CommentResponse;
  @Input() currentUser!: UserResponse;
  @Input() isExpanded: boolean = false;

  editCommentForm: FormGroup;
  isEditing: boolean = false;
  isTruncated: boolean = false;

  constructor(
    private fb: FormBuilder,
    private commentService: CommentService,
    private authService: AuthService,
    private router: Router,
  ) {
    this.editCommentForm = this.fb.group({
      description: ["", [Validators.required, Validators.maxLength(1000)]],
    });
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe((user) => {
      this.currentUser = user;
      this.isTruncated = this.comment.description.length > 250;
    });
  }

  get cf(): { [key: string]: AbstractControl } {
    return this.editCommentForm.controls;
  }

  get isAuthor(): boolean {
    return this.comment.user_id === this.currentUser?.id;
  }

  get truncatedComment(): string {
    return this.isExpanded || this.comment.description.length <= 250
      ? this.comment.description
      : this.comment.description.slice(0, 250) + "...";
  }

  enableEditMode(): void {
    this.isEditing = true;
    this.editCommentForm.patchValue({
      description: this.comment.description,
    });
  }

  saveComment(): void {
    if (this.editCommentForm.valid) {
      const commentUpdate: CommentUpdate = {
        description: this.editCommentForm.value.description,
      };
      this.commentService
        .updateComment(this.comment.id, commentUpdate)
        .subscribe(
          (response) => {
            this.comment.description = response.description;
            this.isEditing = false;
            this.isTruncated = this.comment.description.length > 250;
          },
          (error) => {
            console.error("Error updating comment", error);
          },
        );
    }
  }

  toggleExpand(): void {
    this.isExpanded = !this.isExpanded;
  }

  navigateToForm(): void {
    this.router.navigate(["/comments", this.comment.id]);
  }
}
