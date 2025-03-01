import { Component, OnInit, OnDestroy } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { UserService } from "../shared/users/user.service";
import { Route, Router } from "@angular/router";
import { AuthService } from "../shared/auth.service";
import { UserResponse } from "../shared/users/user.models";
import { ProjectResponse } from "../projects/project.models";
import { DiscussionResponse } from "../discussions/discussion.models";
import { CommentResponse } from "../shared/comment.models";
import { DiscussionService } from "../discussions/discussions.service";
import { ProjectService } from "../projects/projects.service";
import { CommentService } from "../shared/comment.service";
import { Subscription, forkJoin } from "rxjs";

@Component({
  selector: "app-profile",
  templateUrl: "./profile.component.html",
  styleUrls: ["./profile.component.css"],
})
export class ProfileComponent implements OnInit, OnDestroy {
  public static Route: Route = {
    path: "profile",
    component: ProfileComponent,
    title: "Profile Page",
  };
  profileForm: FormGroup;
  currentUser!: UserResponse;
  isEditMode: boolean = false;
  posts: any[] = [];
  userProjects: ProjectResponse[] = [];
  userDiscussions: DiscussionResponse[] = [];
  userComments: CommentResponse[] = [];
  isLoading: boolean = true;
  private subscriptions: Subscription[] = [];

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private authService: AuthService,
    private projectService: ProjectService,
    private discussionService: DiscussionService,
    private commentService: CommentService,
    private router: Router,
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
    this.isLoading = true;
    const userSub = this.authService
      .fetchCurrentUser()
      .subscribe((user: UserResponse) => {
        console.log("User:", user);
        this.currentUser = user;
        this.profileForm.patchValue({
          first_name: user.first_name || "",
          last_name: user.last_name || "",
          email: user.email || "",
          bio: user.bio || "",
          accepted_community_agreement: user.accepted_community_agreement,
        });

        this.loadPosts();
        this.loadUserProjects();
      });
    this.subscriptions.push(userSub);
  }

  ngOnDestroy(): void {
    // Unsubscribe from all subscriptions
    this.subscriptions.forEach((sub) => sub.unsubscribe());
  }

  loadPosts() {
    let postCount = 0;
    const totalPostSources = 3; // projects, discussions, comments
    const checkLoading = () => {
      postCount++;
      if (postCount >= totalPostSources) {
        this.isLoading = false;
      }
    };

    this.projectService.getProjectsByUser(this.currentUser.id!).subscribe({
      next: (projects: ProjectResponse[]) => {
        const projectPosts = projects
          .filter((project) =>
            project.project_leaders.some(
              (leader) => leader.id === this.currentUser.id,
            ),
          )
          .map((project) => ({
            ...project,
            type: "project",
          }));
        this.posts = [...this.posts, ...projectPosts];
        this.sortPostsByDate();
        checkLoading();
      },
      error: (err) => {
        console.error("Error loading projects:", err);
        checkLoading();
      },
    });

    this.discussionService
      .getDiscussionsByAuthor(this.currentUser.id!)
      .subscribe({
        next: (discussions: DiscussionResponse[]) => {
          const discussionPosts = discussions
            .filter(
              (discussion) => discussion.author.id === this.currentUser.id,
            )
            .map((discussion) => ({
              ...discussion,
              type: "discussion",
            }));
          this.posts = [...this.posts, ...discussionPosts];
          this.sortPostsByDate();
          checkLoading();
        },
        error: (err) => {
          console.error("Error loading discussions:", err);
          checkLoading();
        },
      });

    this.commentService.getCommentsByAuthor(this.currentUser.id!).subscribe({
      next: (comments: CommentResponse[]) => {
        console.log("Comments:", comments);
        const commentPosts = comments.map((comment) => ({
          ...comment,
          type: "comment",
        }));
        this.posts = [...this.posts, ...commentPosts];
        this.sortPostsByDate();
        checkLoading();
      },
      error: (err) => {
        console.error("Error loading comments:", err);
        checkLoading();
      },
    });
  }

  loadUserProjects() {
    this.projectService.getProjectsByUser(this.currentUser.id!).subscribe({
      next: (projects: ProjectResponse[]) => {
        this.userProjects = projects.sort(
          (a, b) =>
            new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
        );
      },
      error: (err) => {
        console.error("Error loading user projects:", err);
      },
    });
  }

  getActivityText(post: any): string {
    switch (post.type) {
      case "discussion":
        return `Started a discussion: "${post.title}"`;
      case "comment":
        return `Commented on: "${post.content.substring(0, 30)}${
          post.content.length > 30 ? "..." : ""
        }"`;
      case "project":
        return `Created a project: "${post.name}"`;
      default:
        return "Unknown activity";
    }
  }

  createNewProject(): void {
    this.router.navigate(["/projects/new"]);
  }

  sortPostsByDate() {
    this.posts.sort(
      (a, b) =>
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
    );
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
    this.posts = this.posts.filter(
      (post) => !(post.type === "comment" && post.id === commentId),
    );
  }

  handleProjectDeleted(projectId: number): void {
    this.posts = this.posts.filter(
      (post) => !(post.type === "project" && post.id === projectId),
    );
    this.userProjects = this.userProjects.filter(
      (project) => project.id !== projectId,
    );
  }

  handleDiscussionDeleted(discussionId: number): void {
    this.posts = this.posts.filter(
      (post) => !(post.type === "discussion" && post.id === discussionId),
    );
  }
}
