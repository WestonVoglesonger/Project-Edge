import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { JoinProjectRequestResponse } from '../project.models';
import { ProjectService } from '../projects.service';
import { ProfileForm, UserResponse } from 'src/app/shared/users/user.models';
import { UserService } from 'src/app/shared/users/user.service';

@Component({
  selector: 'app-project-requests',
  templateUrl: './project-requests.component.html',
  styleUrls: ['./project-requests.component.css']
})
export class ProjectRequestsComponent {
  public static Route: Route = {
    path: "projects/requests/:id",
    component: ProjectRequestsComponent,
    title: "Project Requests Page",
  };

  joinRequests: JoinProjectRequestResponse[] = [];
  userProfiles: { [key: number]: UserResponse } = {};
  projectId!: number;

  constructor(private projectService: ProjectService, private userService: UserService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.projectId = +params.get('id')!;
      this.loadPendingJoinRequests(this.projectId);
    });
  }

  loadPendingJoinRequests(projectId: number): void {
    this.projectService.getPendingJoinRequestsByProject(projectId).subscribe(
      (requests: JoinProjectRequestResponse[]) => {
        this.joinRequests = requests;
        const userIds = requests.map(request => request.user_id);
        this.loadUserProfiles(userIds);
      },
      (error: any) => {
        console.error('Error loading join requests', error);
      }
    );
  }

  loadUserProfiles(userIds: number[]): void {
    this.userService.getUsersByIds(userIds).subscribe(
      (users: UserResponse[]) => {
        users.forEach(user => {
          this.userProfiles[user.id!] = user;
        });
        console.log(this.userProfiles);
      },
      (error: any) => {
        console.error('Error loading user profiles', error);
      }
    );
  }

  approveRequest(requestId: number): void {
    this.projectService.approveJoinRequest(requestId).subscribe(
      () => {
        this.joinRequests = this.joinRequests.filter(request => request.id !== requestId);
      },
      (error: any) => {
        console.error('Error approving join request', error);
      }
    );
  }

  rejectRequest(requestId: number): void {
    this.projectService.rejectJoinRequest(requestId).subscribe(
      () => {
        this.joinRequests = this.joinRequests.filter(request => request.id !== requestId);
      },
      (error: any) => {
        console.error('Error rejecting join request', error);
      }
    );
  }

  getUserName(userId: number): string {
    const user = this.userProfiles[userId];
    return user ? `${user.first_name} ${user.last_name}` : 'Unknown User';
  }
}