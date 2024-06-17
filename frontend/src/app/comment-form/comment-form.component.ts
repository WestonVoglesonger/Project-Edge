import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { AuthService } from "../shared/auth.service";
import { CommentResponse } from "../shared/comment.models";
import { CommentService } from "../shared/comment.service";
import { UserResponse } from "../shared/users/user.models";

@Component({
  selector: "app-comment-form",
  templateUrl: "./comment-form.component.html",
  styleUrls: ["./comment-form.component.css"],
})
export class CommentFormComponent implements OnInit {
  public static Route = {
    path: "comments/:id",
    component: CommentFormComponent,
    title: "Comment Form Page",
  };

  comment: CommentResponse | null = null;
  currentUser!: UserResponse;

  constructor(
    private commentService: CommentService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router,
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get("id");
    if (id) {
      this.loadComment(+id); // Convert id to a number
    }

    this.authService.fetchCurrentUser().subscribe((user: any) => {
      this.currentUser = user;
    });
  }

  loadComment(id: number): void {
    this.commentService.getComment(id).subscribe(
      (comment: any) => {
        this.comment = comment;
      },
      (error: any) => {
        console.error("Error loading comment", error);
      },
    );
  }
}
