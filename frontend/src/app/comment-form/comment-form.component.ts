import { Component, Input, OnInit } from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl,
} from "@angular/forms";
import { CommentService } from "src/app/shared/comment.service";
import {
  CommentCreate,
  CommentUpdate,
  CommentResponse,
} from "src/app/shared/comment.models";
import { Route } from "@angular/router";

@Component({
  selector: "app-comment-form",
  templateUrl: "./comment-form.component.html",
  styleUrls: ["./comment-form.component.css"],
})
export class CommentFormComponent implements OnInit {
  public static Route: Route = {
    path: "comments/:id",
    component: CommentFormComponent,
    title: "Comment Form Page",
  };
  @Input() discussion_id?: number;
  @Input() project_id?: number;
  @Input() comment_id?: number;

  commentForm: FormGroup;
  isEditMode: boolean = false;
  errorMessage: string = "";

  constructor(
    private fb: FormBuilder,
    private commentService: CommentService,
  ) {
    this.commentForm = this.fb.group({
      description: ["", [Validators.required, Validators.minLength(1)]],
    });
  }

  ngOnInit(): void {
    if (this.comment_id) {
      this.isEditMode = true;
      this.loadComment(this.comment_id);
    }
  }

  loadComment(id: number): void {
    this.commentService.getComment(id).subscribe(
      (comment) => {
        this.commentForm.patchValue({
          description: comment.description,
        });
      },
      (error) => {
        console.error("Error loading comment", error);
        this.handleError(error);
      },
    );
  }

  saveComment(): void {
    if (this.commentForm.valid) {
      if (this.isEditMode && this.comment_id) {
        const commentUpdate: CommentUpdate = {
          description: this.commentForm.value.description,
        };
        this.commentService
          .updateComment(this.comment_id, commentUpdate)
          .subscribe(
            (response) => {
              console.log("Comment updated successfully", response);
            },
            (error) => {
              console.error("Error updating comment", error);
              this.handleError(error);
            },
          );
      } else {
        const commentCreate: CommentCreate = {
          description: this.commentForm.value.description,
          user_id: 1, // Replace with the actual user ID
          discussion_id: this.discussion_id,
          project_id: this.project_id,
        };
        this.commentService.createComment(commentCreate).subscribe(
          (response) => {
            console.log("Comment created successfully", response);
          },
          (error) => {
            console.error("Error creating comment", error);
            this.handleError(error);
          },
        );
      }
    }
  }

  handleError(error: any): void {
    if (error.status === 422 && error.error && error.error.detail) {
      this.errorMessage =
        "Validation error: " +
        error.error.detail.map((err: any) => err.msg).join(", ");
    } else {
      this.errorMessage =
        "An unexpected error occurred. Please try again later.";
    }
  }

  get f(): { [key: string]: AbstractControl } {
    return this.commentForm.controls;
  }
}
