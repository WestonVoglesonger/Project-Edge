import {
  Component,
  OnInit,
  ViewChild,
  ElementRef,
  AfterViewInit,
  ChangeDetectorRef,
} from "@angular/core";
import {
  FormGroup,
  FormBuilder,
  Validators,
  AbstractControl,
} from "@angular/forms";
import { ActivatedRoute, Route, Router } from "@angular/router";
import { MatAutocompleteTrigger } from "@angular/material/autocomplete";
import { DiscussionService } from "../discussions.service";
import { UserResponse } from "src/app/shared/users/user.models";
import { UserService } from "src/app/shared/users/user.service";
import { AuthService } from "src/app/shared/auth.service";
import { Discussion } from "../discussion.models";
import { CommentService } from "src/app/shared/comment.service";
import { CommentResponse, CommentCreate } from "src/app/shared/comment.models";

@Component({
  selector: "app-discussion-form",
  templateUrl: "./discussion-form.component.html",
  styleUrls: ["./discussion-form.component.css"],
})
export class DiscussionFormComponent implements OnInit, AfterViewInit {
  public static Route: Route = {
    path: "discussions/:id",
    component: DiscussionFormComponent,
    title: "Discussion Form Page",
  };

  discussionForm: FormGroup;
  commentForm: FormGroup;
  isNewDiscussion: boolean = true;
  currentUser!: UserResponse;
  isAuthor: boolean = false;
  comments: CommentResponse[] = [];
  discussion_id!: number;

  @ViewChild("currentUsersInput") currentUsersInput!: ElementRef;
  @ViewChild("ownersInput") ownersInput!: ElementRef;
  @ViewChild("currentUsersInput", { read: MatAutocompleteTrigger })
  currentUsersInputTrigger!: MatAutocompleteTrigger;
  @ViewChild("ownersInput", { read: MatAutocompleteTrigger })
  ownersInputTrigger!: MatAutocompleteTrigger;

  private originalDiscussionData: any;

  constructor(
    private fb: FormBuilder,
    private discussionService: DiscussionService,
    private userService: UserService,
    private authService: AuthService,
    private commentService: CommentService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {
    this.discussionForm = this.fb.group({
      title: [
        "",
        [
          Validators.required,
          Validators.minLength(3),
          Validators.maxLength(50),
        ],
      ],
      description: ["", [Validators.required, Validators.minLength(10)]],
    });

    this.commentForm = this.fb.group({
      description: ["", [Validators.required, Validators.minLength(1)]],
    });
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe(
      (user) => {
        this.currentUser = user;
        this.route.paramMap.subscribe((params) => {
          const id = params.get("id");
          if (id && id !== "new") {
            this.isNewDiscussion = false;
            this.discussion_id = +id;
            this.loadDiscussion(this.discussion_id);
            this.loadComments(this.discussion_id);
          }
        });
      },
      (error) => {
        console.error("Error fetching current user", error);
      },
    );
  }

  ngAfterViewInit(): void {
    // Ensure input elements are available after view initialization
    if (this.currentUsersInput) {
      console.log("currentUsersInput is available");
    }
    if (this.ownersInput) {
      console.log("ownersInput is available");
    }
  }

  loadDiscussion(id: number): void {
    this.discussionService.getDiscussion(id).subscribe(
      (discussion) => {
        this.discussionForm.patchValue({
          title: discussion.title,
          description: discussion.description,
        });
        this.originalDiscussionData = {
          ...discussion,
        };

        this.isAuthor = discussion.author.id === this.currentUser?.id;
        if (!this.isAuthor) {
          this.discussionForm.disable();
        }
      },
      (error) => {
        console.error("Error loading discussion", error);
      },
    );
  }

  loadComments(discussionId: number): void {
    this.commentService.getCommentsByDiscussion(discussionId).subscribe(
      (comments: CommentResponse[]) => {
        this.comments = comments;
      },
      (error) => {
        console.error("Error loading comments", error);
      },
    );
  }

  saveDiscussion(): void {
    if (this.discussionForm.valid) {
      const discussionData: Discussion = {
        ...this.discussionForm.value,
        author_id: this.currentUser?.id,
      };

      if (this.isNewDiscussion) {
        this.discussionService.createDiscussion(discussionData).subscribe(
          (response) => {
            console.log("Discussion created successfully", response);
            this.router.navigate(["/discussions"]);
          },
          (error) => {
            console.error("Error creating discussion", error);
          },
        );
      } else {
        this.discussionService
          .updateDiscussion(this.discussion_id, discussionData)
          .subscribe(
            (response) => {
              console.log("Discussion updated successfully", response);
              this.router.navigate(["/discussions"]);
            },
            (error) => {
              console.error("Error updating discussion", error);
            },
          );
      }
    }
  }

  deleteDiscussion(): void {
    if (confirm("Are you sure you want to delete this project?")) {
      this.discussionService.deleteDiscussion(this.discussion_id).subscribe(
        (response) => {
          console.log("Project deleted successfully", response);
          this.router.navigate(["/projects"]);
        },
        (error) => {
          console.error("Error deleting project", error);
        },
      );
    }
  }
  saveComment(): void {
    if (this.commentForm.valid) {
      const commentCreate: CommentCreate = {
        description: this.commentForm.value.description,
        project_id: null,
        discussion_id: this.discussion_id,
        parent_id: null,
        author_id: this.currentUser?.id!,
      };

      this.commentService.createComment(commentCreate).subscribe(
        (response) => {
          console.log("Comment created successfully", response);
          this.comments.push(response);
          this.commentForm.reset();
        },
        (error) => {
          console.error("Error creating comment", error);
        },
      );
    }
  }

  handleCommentDeleted(commentId: number): void {
    this.comments = this.comments.filter((comment) => comment.id !== commentId);
  }

  deleteComment(commentId: number): void {
    this.commentService.deleteComment(commentId).subscribe(
      (response) => {
        console.log("Comment deleted successfully", response);
        this.comments = this.comments.filter(
          (comment) => comment.id !== commentId,
        );
      },
      (error) => {
        console.error("Error deleting comment", error);
      },
    );
  }

  cancelChanges(): void {
    if (this.isNewDiscussion) {
      this.discussionForm.reset();
    } else {
      this.discussionForm.patchValue({
        title: this.originalDiscussionData.title,
        description: this.originalDiscussionData.description,
      });
    }
    this.router.navigate(["/discussions"]);
  }

  get f(): { [key: string]: AbstractControl } {
    return this.discussionForm.controls;
  }

  get cf(): { [key: string]: AbstractControl } {
    return this.commentForm.controls;
  }
}
