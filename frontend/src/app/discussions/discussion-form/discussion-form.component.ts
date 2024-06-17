import {
  Component,
  OnInit,
  ViewChild,
  ElementRef,
  AfterViewInit,
} from "@angular/core";
import {
  FormGroup,
  FormBuilder,
  Validators,
  FormArray,
  AbstractControl,
} from "@angular/forms";
import { ActivatedRoute, Route, Router } from "@angular/router";
import { MatAutocompleteTrigger } from "@angular/material/autocomplete";
import { DiscussionService } from "../discussions.service";
import { UserResponse } from "src/app/shared/users/user.models";
import { UserService } from "src/app/shared/users/user.service";
import { AuthService } from "src/app/shared/auth.service";
import { minLengthArray } from "src/app/shared/min-length-array.validator";
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
  filteredMembers: UserResponse[] = [];
  filteredLeaders: UserResponse[] = [];
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
  ) {
    this.discussionForm = this.fb.group({
      title: ["", [Validators.required, Validators.minLength(3)]],
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

  saveComment(): void {
    if (this.commentForm.valid) {
      const commentCreate: CommentCreate = {
        description: this.commentForm.value.description,
        project_id: null,
        discussion_id: this.discussion_id,
        user_id: this.currentUser?.id!,
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
