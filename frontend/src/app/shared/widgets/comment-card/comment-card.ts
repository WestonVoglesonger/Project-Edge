import {
  Component,
  Input,
  OnInit,
  Output,
  EventEmitter,
  OnDestroy,
} from "@angular/core";
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
import { Subscription } from "rxjs";

@Component({
  selector: "app-comment-card",
  templateUrl: "./comment-card.html",
  styleUrls: ["./comment-card.css"],
})
export class CommentCard implements OnInit, OnDestroy {
  @Input() comment!: CommentResponse;
  @Input() currentUser!: UserResponse;
  @Input() isExpanded: boolean = false;
  @Output() commentDeleted = new EventEmitter<number>();
  @Output() commentUpdated = new EventEmitter<CommentResponse>();

  editCommentForm: FormGroup;
  isEditing: boolean = false;
  isTruncated: boolean = false;

  private subscriptions: Subscription[] = [];

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
    const userSub = this.authService.fetchCurrentUser().subscribe((user) => {
      this.currentUser = user;
      this.isTruncated = this.comment.description.length > 250;
    });
    this.subscriptions.push(userSub);
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach((sub) => sub.unsubscribe());
  }

  get cf(): { [key: string]: AbstractControl } {
    return this.editCommentForm.controls;
  }

  get isAuthor(): boolean {
    return this.comment.author.id === this.currentUser?.id;
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
            this.comment.updated_at = response.updated_at; // Update the updated_at field
            this.isEditing = false;
            this.isTruncated = this.comment.description.length > 250;
            this.commentUpdated.emit(this.comment); // Emit the updated comment
          },
          (error) => {
            console.error("Error updating comment", error);
          },
        );
    }
  }

  deleteComment(): void {
    if (confirm("Are you sure you want to delete this comment?")) {
      this.commentService.deleteComment(this.comment.id).subscribe(
        (response) => {
          console.log("Comment deleted successfully", response);
          this.commentDeleted.emit(this.comment.id);
        },
        (error) => {
          console.error("Error deleting comment", error);
        },
      );
    }
  }

  toggleExpand(): void {
    this.isExpanded = !this.isExpanded;
  }

  navigateToForm(): void {
    console.log("Navigating to form:", this.comment.id);
    this.router.navigate(["/comments", this.comment.id]);
  }

  get mostRecentTime(): Date {
    return new Date(this.comment.updated_at) > new Date(this.comment.created_at)
      ? new Date(this.comment.updated_at)
      : new Date(this.comment.created_at);
  }
}
