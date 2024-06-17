import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup } from "@angular/forms";
import { UserService } from "../shared/users/user.service";
import { Route } from "@angular/router";
import { AuthService } from "../shared/auth.service";
import { UserResponse } from "../shared/users/user.models";
import { ProjectResponse } from "../projects/project.models";
import { DiscussionResponse } from "../discussions/discussion.models";
import { CommentResponse } from "../shared/comment.models";
import { DiscussionService } from "../discussions/discussions.service";
import { ProjectService } from "../projects/projects.service";
import { CommentService } from "../shared/comment.service";

@Component({
  selector: "app-profile",
  templateUrl: "./profile.component.html",
  styleUrls: ["./profile.component.css"],
})
export class ProfileComponent implements OnInit {
  public static Route: Route = {
    path: "profile",
    component: ProfileComponent,
    title: "Profile Page",
  };
  profileForm: FormGroup;
  currentUser!: UserResponse;
  isEditMode: boolean = false;
  projects!: ProjectResponse[];
  discussions!: DiscussionResponse[];
  comments!: CommentResponse[];

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private authService: AuthService,
    private projectService: ProjectService,
    private discussionService: DiscussionService,
    private commentService: CommentService,
  ) {
    this.profileForm = this.fb.group({
      first_name: [{ value: "", disabled: true }],
      last_name: [{ value: "", disabled: true }],
      email: [{ value: "", disabled: true }],
      bio: [{ value: "", disabled: true }],
      accepted_community_agreement: [{ value: true }],
    });
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe((user: UserResponse) => {
      console.log("User:", user);
      this.currentUser = user;
      this.profileForm.patchValue({
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        email: user.email || "",
        bio: user.bio || "",
        accepted_community_agreement: user.accepted_community_agreement,
      });
    });
  }

  loadProjects() {
    this.projectService.getProjectsByUser(this.currentUser.id!).subscribe({
      next: (projects: ProjectResponse[]) => {
        this.projects = projects;
      },
      error: (err) => {
        console.error("Error loading projects:", err);
      },
    });
  }

  loadDiscussions() {
    this.discussionService
      .getDiscussionsByAuthor(this.currentUser.id!)
      .subscribe({
        next: (discussions: DiscussionResponse[]) => {
          this.discussions = discussions;
        },
        error: (err) => {
          console.error("Error loading discussions:", err);
        },
      });
  }

  loadComments() {
    this.commentService.getCommentsByAuthor(this.currentUser.id!).subscribe({
      next: (comments: CommentResponse[]) => {
        this.comments = comments;
      },
      error: (err) => {
        console.error("Error loading comments:", err);
      },
    });
  }

  onEdit() {
    this.isEditMode = !this.isEditMode;
    if (this.isEditMode) {
      this.profileForm.enable();
      this.profileForm.get("email")?.disable();
    } else {
      this.profileForm.disable();
    }
  }

  onSubmit() {
    if (this.currentUser.id!) {
      const profileData = this.profileForm.getRawValue();
      const formData = new FormData();
      formData.append("first_name", profileData.first_name);
      formData.append("last_name", profileData.last_name);
      formData.append("email", profileData.email);
      formData.append("bio", profileData.bio);
      formData.append(
        "accepted_community_agreement",
        String(profileData.accepted_community_agreement),
      );

      this.userService
        .updateUserProfile(this.currentUser.id!, formData)
        .subscribe({
          next: () => {
            this.isEditMode = false;
            this.profileForm.disable();
          },
          error: (err) => {
            console.error("Error updating profile:", err);
          },
        });
    }
  }

  handleCommentDeleted(commentId: number): void {
    this.comments = this.comments.filter((comment) => comment.id !== commentId);
  }

  handleProjectDeleted(projectId: number): void {
    this.projects = this.projects.filter((project) => project.id !== projectId);
  }

  handleDiscussionDeleted(discussionId: number): void {
    this.discussions = this.discussions.filter(
      (discussion) => discussion.id !== discussionId,
    );
  }
}
