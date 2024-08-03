import { Component } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { JoinProjectRequestResponse } from '../project.models';
import { ProjectService } from '../projects.service';

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
  projectId!: number;

  constructor(private projectService: ProjectService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params: { get: (arg0: string) => any; }) => {
      this.projectId = +params.get('id')!;
      this.loadPendingJoinRequests(this.projectId);
    });
  }

  loadPendingJoinRequests(projectId: number): void {
    this.projectService.getPendingJoinRequestsByProject(projectId).subscribe(
      
      (      requests: JoinProjectRequestResponse[]) => {
        this.joinRequests = requests;
        console.log(this.joinRequests);
      },
      (      error: any) => {
        console.error('Error loading join requests', error);
      }
    );
  }

  approveRequest(requestId: number): void {
    this.projectService.approveJoinRequest(requestId).subscribe(
      () => {
        this.joinRequests = this.joinRequests.filter(request => request.id !== requestId);
      },
      (      error: any) => {
        console.error('Error approving join request', error);
      }
    );
  }

  rejectRequest(requestId: number): void {
    this.projectService.rejectJoinRequest(requestId).subscribe(
      () => {
        this.joinRequests = this.joinRequests.filter(request => request.id !== requestId);
      },
      (      error: any) => {
        console.error('Error rejecting join request', error);
      }
    );
  }
}
