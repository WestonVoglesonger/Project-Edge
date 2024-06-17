import {
  Component,
  Input,
  OnInit,
  OnDestroy,
  ChangeDetectorRef,
} from "@angular/core";
import {
  FormBuilder,
  FormGroup,
  Validators,
  AbstractControl,
} from "@angular/forms";
import { Router, ActivatedRoute, Route } from "@angular/router";
import {
  CommentCreate,
  CommentResponse,
  CommentUpdate,
} from "../shared/comment.models";
import { AuthService } from "../shared/auth.service";
import { CommentService } from "../shared/comment.service";
import { UserResponse } from "../shared/users/user.models";
import { Subscription } from "rxjs";

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

  replyForm: FormGroup;
  isEditMode: boolean = false;
  errorMessage: string = "";
  currentUser!: UserResponse;
  comment!: CommentResponse;
  replies: CommentResponse[] = [];

  constructor(
    private fb: FormBuilder,
    private commentService: CommentService,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private cdr: ChangeDetectorRef,
  ) {
    this.replyForm = this.fb.group({
      description: [
        "",
        [
          Validators.required,
          Validators.minLength(1),
          Validators.maxLength(1000),
        ],
      ],
    });
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe(
      (user: UserResponse) => {
        this.currentUser = user;
        this.route.paramMap.subscribe(
          (params) => {
            const id = params.get("id");
            if (id) {
              this.comment_id = +id;
              this.isEditMode = true;
              this.loadComment(this.comment_id);
            }
          },
          (error: any) => {
            console.error("Error fetching route parameters", error);
          },
        );
      },
      (error: any) => {
        console.error("Error fetching current user", error);
      },
    );
  }

  loadComment(id: number): void {
    this.commentService.getComment(id).subscribe(
      (comment) => {
        this.comment = comment;
        this.loadReplies(id);
      },
      (error: any) => {
        console.error("Error loading comment", error);
        this.handleError(error);
      },
    );
  }

  loadReplies(parent_id: number): void {
    this.commentService.getCommentsByParent(parent_id).subscribe(
      (replies: CommentResponse[]) => {
        this.replies = replies;
      },
      (error) => {
        console.error("Error loading comments", error);
      },
    );
  }

  saveReply(): void {
    if (this.replyForm.valid) {
      const replyCreate: CommentCreate = {
        description: this.replyForm.value.description,
        project_id: this.project_id || null,
        discussion_id: this.discussion_id || null,
        parent_id: this.comment_id || null,
        user_id: this.currentUser.id!,
      };
      this.commentService.createComment(replyCreate).subscribe(
        (response: CommentResponse) => {
          console.log("Reply created successfully", response);
          this.replies.push(response);
          this.replyForm.reset();
        },
        (error: any) => {
          console.error("Error creating reply", error);
          this.handleError(error);
        },
      );
    }
  }

  cancelChanges(): void {
    if (this.isEditMode && this.comment) {
      this.replyForm.patchValue({
        description: this.comment.description,
      });
      this.isEditMode = false;
    } else {
      this.replyForm.reset();
      this.router.navigate(["/discussions"]);
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

  get rf(): { [key: string]: AbstractControl } {
    return this.replyForm.controls;
  }
}
