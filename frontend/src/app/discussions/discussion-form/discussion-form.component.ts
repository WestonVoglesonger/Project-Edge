import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Route, Router } from "@angular/router";
import {
  FormGroup,
  FormBuilder,
  Validators,
  AbstractControl,
} from "@angular/forms";
import { AuthService } from "src/app/shared/auth.service";
import { Discussion } from "../discussion.models";
import { DiscussionService } from "../discussions.service";
import { CommentResponse } from "src/app/shared/comment.models";
import { CommentService } from "src/app/shared/comment.service";

@Component({
  selector: "app-discussion-form",
  templateUrl: "./discussion-form.component.html",
  styleUrls: ["./discussion-form.component.css"],
})
export class DiscussionFormComponent implements OnInit {
  public static Route: Route = {
    path: "discussions/:id",
    component: DiscussionFormComponent,
    title: "Discussion Form Page",
  };

  discussionForm: FormGroup;
  isNewDiscussion: boolean = true;
  currentUser: any | null = null;
  isAuthor: boolean = false;
  comments: CommentResponse[] = [];
  discussion_id!: number;

  private originalDiscussionData: any;

  constructor(
    private fb: FormBuilder,
    private discussionService: DiscussionService,
    private commentService: CommentService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
    this.discussionForm = this.fb.group({
      title: ["", [Validators.required, Validators.minLength(3)]],
      description: ["", [Validators.required, Validators.minLength(10)]],
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

  loadDiscussion(id: number): void {
    this.discussionService.getDiscussion(id).subscribe(
      (discussion) => {
        this.discussionForm.patchValue({
          title: discussion.title,
          description: discussion.description,
        });
        this.originalDiscussionData = { ...discussion };

        this.isAuthor = discussion.author_id === this.currentUser?.id;
        if (!this.isAuthor) {
          this.discussionForm.disable();
        }
      },
      (error) => {
        console.error("Error loading discussion", error);
      },
    );
  }

  loadComments(DiscussionId: number): void {
    this.commentService.getCommentsByDiscussion(DiscussionId).subscribe(
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
}
