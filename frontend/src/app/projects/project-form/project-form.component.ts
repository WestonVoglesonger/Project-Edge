import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, AbstractControl } from '@angular/forms';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { MatAutocompleteTrigger } from '@angular/material/autocomplete';
import { ProjectService } from '../projects.service';
import { UserResponse } from 'src/app/shared/users/user.models';
import { UserService } from 'src/app/shared/users/user.service';
import { AuthService } from 'src/app/shared/auth.service';
import { minLengthArray } from 'src/app/shared/min-length-array.validator';
import { Project } from '../project.models';

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.css']
})
export class ProjectFormComponent implements OnInit, AfterViewInit {
  public static Route: Route = {
    path: "projects/:id",
    component: ProjectFormComponent,
    title: "Project Form Page",
  };

  projectForm: FormGroup;
  isNewProject: boolean = true;
  filteredMembers: UserResponse[] = [];
  filteredLeaders: UserResponse[] = [];
  currentUser: UserResponse | null = null;
  isLeader: boolean = false;

  @ViewChild('currentUsersInput') currentUsersInput!: ElementRef;
  @ViewChild('ownersInput') ownersInput!: ElementRef;
  @ViewChild('currentUsersInput', { read: MatAutocompleteTrigger }) currentUsersInputTrigger!: MatAutocompleteTrigger;
  @ViewChild('ownersInput', { read: MatAutocompleteTrigger }) ownersInputTrigger!: MatAutocompleteTrigger;

  private originalProjectData: any;

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private userService: UserService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.projectForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      team_members: this.fb.array([]),
      project_leaders: this.fb.array([], minLengthArray(1))
    });
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser().subscribe(
      user => {
        this.currentUser = user;
        this.route.paramMap.subscribe(params => {
          const id = params.get('id');
          if (id && id !== 'new') {
            this.isNewProject = false;
            this.loadProject(id);
          } else {
            this.addCurrentUserToProjectLeaders();
          }
        });
      },
      error => {
        console.error('Error fetching current user', error);
      }
    );
  }

  ngAfterViewInit(): void {
    // Ensure input elements are available after view initialization
    if (this.currentUsersInput) {
      console.log('currentUsersInput is available');
    }
    if (this.ownersInput) {
      console.log('ownersInput is available');
    }
  }

  addCurrentUserToProjectLeaders(): void {
    if (this.currentUser) {
      this.project_leaders.push(this.fb.control(this.currentUser));
    }
  }

  get currentUsers(): FormArray {
    return this.projectForm.get('team_members') as FormArray;
  }

  get project_leaders(): FormArray {
    return this.projectForm.get('project_leaders') as FormArray;
  }

  loadProject(id: string): void {
    this.projectService.getProject(id).subscribe(
      project => {
        this.projectForm.patchValue({
          name: project.name,
          description: project.description,
        });
        this.setTeamMembers(project.team_members);
        this.setProjectLeaders(project.project_leaders);
        this.originalProjectData = {
          ...project,
          team_members: [...project.team_members],
          project_leaders: [...project.project_leaders]
        };

        this.isLeader = project.project_leaders.some((leader: { email: string | undefined; }) => leader.email === this.currentUser?.email);
        if (!this.isLeader) {
          this.projectForm.disable();
        }
      },
      error => {
        console.error('Error loading project', error);
      }
    );
  }

  setTeamMembers(users: UserResponse[]): void {
    users.forEach(user => this.currentUsers.push(this.fb.control(user)));
  }

  setProjectLeaders(users: UserResponse[]): void {
    users.forEach(user => this.project_leaders.push(this.fb.control(user)));
  }

  saveProject(): void {
    if (this.projectForm.valid) {
      const projectData: Project = {
        ...this.projectForm.value,
        team_members: this.currentUsers.value.filter((user: UserResponse) => user.email),
        project_leaders: this.project_leaders.value.filter((user: UserResponse) => user.email)
      };

      if (this.isNewProject) {
        this.projectService.createProject(projectData).subscribe(
          response => {
            console.log('Project created successfully', response);
            this.router.navigate(['/projects']);
          },
          error => {
            console.error('Error creating project', error);
          }
        );
      } else {
        const id = this.route.snapshot.paramMap.get('id');
        this.projectService.updateProject(id!, projectData).subscribe(
          response => {
            console.log('Project updated successfully', response);
            this.router.navigate(['/projects']);
          },
          error => {
            console.error('Error updating project', error);
          }
        );
      }
    }
  }

  searchUsers(event: Event, type: 'users' | 'leaders' = 'users'): void {
    const input = event.target as HTMLInputElement;
    const query = input.value;
  
    if (query.length > 2) {
      this.userService.searchUsers(query).subscribe(users => {
        console.log('Users', users);
        const selectedUsers = type === 'users' ? this.currentUsers.value : this.project_leaders.value;
        const selectedUserEmails = selectedUsers.map((user: UserResponse) => user.email);
  
        const filtered = users.filter(user => !selectedUserEmails.includes(user.email));
        
        if (type === 'users') {
          this.filteredMembers = filtered;
        } else {
          this.filteredLeaders = filtered;
        }
      },
      error => {
        console.error(`Error Code: ${error.status}\nMessage: ${error.message}`);
      });
    } else {
      if (type === 'users') {
        this.filteredMembers = [];
      } else {
        this.filteredLeaders = [];
      }
    }
  }  

  addUser(user: UserResponse, type: 'users' | 'leaders', input: HTMLInputElement): void {
    if (type === 'users') {
      this.currentUsers.push(this.fb.control(user));
      this.currentUsersInputTrigger.closePanel();
    } else {
      this.project_leaders.push(this.fb.control(user));
      this.ownersInputTrigger.closePanel();
    }
    input.value = ''; // Clear the input field
  }

  removeUser(index: number, type: 'users' | 'leaders', event: Event): void {
    event.stopPropagation(); // Prevent the input field from gaining focus
    if ((this.isLeader || this.isNewProject) && (type === 'users' || type === 'leaders')) {
      if (type === 'users') {
        this.currentUsers.removeAt(index);
        this.filteredMembers = [];
        if (this.currentUsersInput) {
          this.currentUsersInput.nativeElement.value = '';
          this.currentUsersInputTrigger.closePanel();
        }
      } else {
        this.project_leaders.removeAt(index);
        this.filteredLeaders = [];
        if (this.ownersInput) {
          this.ownersInput.nativeElement.value = '';
          this.ownersInputTrigger.closePanel();
        }
      }
    }
  }

  cancelChanges(): void {
    if (this.isNewProject) {
      this.projectForm.reset();
      this.currentUsers.clear();
      this.project_leaders.clear();
    } else {
      this.projectForm.patchValue({
        name: this.originalProjectData.name,
        description: this.originalProjectData.description,
      });

      // Clear and reset team_members and project_leaders FormArrays
      this.currentUsers.clear();
      this.project_leaders.clear();
      this.originalProjectData.team_members.forEach((user: UserResponse) => {
        this.currentUsers.push(this.fb.control(user));
      });
      this.originalProjectData.project_leaders.forEach((user: UserResponse) => {
        this.project_leaders.push(this.fb.control(user));
      });
    }
    this.router.navigate(['/projects']);
  }

  get f(): { [key: string]: AbstractControl } {
    return this.projectForm.controls;
  }
}
