import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, AbstractControl } from '@angular/forms';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { ProjectService } from '../projects.service';
import { UserResponse } from 'src/app/shared/users/user.models';
import { UserService } from 'src/app/shared/users/user.service';
import { AuthService } from 'src/app/shared/auth.service';
import { minLengthArray } from 'src/app/shared/min-length-array.validator';

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.css']
})
export class ProjectFormComponent implements OnInit {
  public static Route: Route = {
    path: "projects/:id",
    component: ProjectFormComponent,
    title: "Project Form Page",
  };

  projectForm: FormGroup;
  isNewProject: boolean = true;
  filteredUsers: UserResponse[] = [];
  filteredOwners: UserResponse[] = [];
  currentUser: UserResponse | null = null;
  isOwner: boolean = false;

  @ViewChild('currentUsersInput') currentUsersInput!: ElementRef;
  @ViewChild('ownersInput') ownersInput!: ElementRef;

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
      current_users: this.fb.array([]),
      owners: this.fb.array([], minLengthArray(1))
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
            this.addCurrentUserToOwners();
          }
        });
      },
      error => {
        console.error('Error fetching current user', error);
      }
    );
  }

  addCurrentUserToOwners(): void {
    if (this.currentUser) {
      this.owners.push(this.fb.control(this.currentUser));
    }
  }

  get currentUsers(): FormArray {
    return this.projectForm.get('current_users') as FormArray;
  }

  get owners(): FormArray {
    return this.projectForm.get('owners') as FormArray;
  }

  loadProject(id: string): void {
    this.projectService.getProject(id).subscribe(
      project => {
        this.projectForm.patchValue({
          name: project.name,
          description: project.description,
        });
        this.setCurrentUsers(project.current_users);
        this.setOwners(project.owners);
        this.originalProjectData = {
          ...project,
          current_users: [...project.current_users],
          owners: [...project.owners]
        };

        this.isOwner = project.owners.some((owner: { email: string | undefined; }) => owner.email === this.currentUser?.email);
        if (!this.isOwner) {
          this.projectForm.disable();
        }
      },
      error => {
        console.error('Error loading project', error);
      }
    );
  }

  setCurrentUsers(users: UserResponse[]): void {
    users.forEach(user => this.currentUsers.push(this.fb.control(user)));
  }

  setOwners(users: UserResponse[]): void {
    users.forEach(user => this.owners.push(this.fb.control(user)));
  }

  saveProject(): void {
    if (this.projectForm.valid) {
      const projectData = {
        ...this.projectForm.value,
        current_users: this.currentUsers.value.filter((user: UserResponse) => user.email),
        owners: this.owners.value.filter((user: UserResponse) => user.email)
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

  searchUsers(event: Event, type: 'users' | 'owners' = 'users'): void {
    const input = event.target as HTMLInputElement;
    const query = input.value;
  
    if (query.length > 2) {
      this.userService.searchUsers(query).subscribe(users => {
        console.log('Users', users);
        const selectedUsers = type === 'users' ? this.currentUsers.value : this.owners.value;
        const selectedUserEmails = selectedUsers.map((user: UserResponse) => user.email);
  
        const filtered = users.filter(user => !selectedUserEmails.includes(user.email));
        
        if (type === 'users') {
          this.filteredUsers = filtered;
        } else {
          this.filteredOwners = filtered;
        }
      },
      error => {
        console.error(`Error Code: ${error.status}\nMessage: ${error.message}`);
      });
    } else {
      if (type === 'users') {
        this.filteredUsers = [];
      } else {
        this.filteredOwners = [];
      }
    }
  }  

  addUser(user: UserResponse, type: 'users' | 'owners', input: HTMLInputElement): void {
    if (type === 'users') {
      this.currentUsers.push(this.fb.control(user));
    } else {
      this.owners.push(this.fb.control(user));
    }
    input.value = ''; // Clear the input field
  }

  removeUser(index: number, type: 'users' | 'owners'): void {
    if ((this.isOwner || this.isNewProject) && (type === 'users' || type === 'owners')) {
      if (type === 'users') {
        this.currentUsers.removeAt(index);
      } else {
        this.owners.removeAt(index);
      }
  
      // Re-fetch users to update the dropdown
      const inputElement = type === 'users' ? this.currentUsersInput.nativeElement : this.ownersInput.nativeElement;
      this.searchUsers({ target: inputElement } as Event, type);
    }
  }

  cancelChanges(): void {
    if (this.isNewProject) {
      this.projectForm.reset();
      this.currentUsers.clear();
      this.owners.clear();
    } else {
      this.projectForm.patchValue({
        name: this.originalProjectData.name,
        description: this.originalProjectData.description,
      });

      // Clear and reset current_users and owners FormArrays
      this.currentUsers.clear();
      this.owners.clear();
      this.originalProjectData.current_users.forEach((user: UserResponse) => {
        this.currentUsers.push(this.fb.control(user));
      });
      this.originalProjectData.owners.forEach((user: UserResponse) => {
        this.owners.push(this.fb.control(user));
      });
    }
    this.router.navigate(['/projects']);
  }

  get f(): { [key: string]: AbstractControl } {
    return this.projectForm.controls;
  }
}
