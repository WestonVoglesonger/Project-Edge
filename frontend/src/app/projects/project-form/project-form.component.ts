import { Component, OnInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, AbstractControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ProjectService } from '../projects.service';
import { UserResponse } from 'src/app/shared/users/user.models';
import { UserService } from 'src/app/shared/users/user.service';
import { AuthService } from 'src/app/shared/auth.service';
import { minLengthArray } from 'src/app/shared/min-length-array.validator';
import { Subject, Observable, combineLatest, map, startWith, debounceTime, distinctUntilChanged, switchMap, takeUntil, catchError, of, fromEvent } from 'rxjs';

interface ProjectData {
  name: string;
  description: string;
  team_members: UserResponse[];
  project_leaders: UserResponse[];
}

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.css']
})
export class ProjectFormComponent implements OnInit, OnDestroy {
  public static Route = {
    path: "projects/:id",
    component: ProjectFormComponent,
    title: "Project Form Page",
  };

  projectForm: FormGroup;
  isNewProject: boolean = true;
  filteredMembers$: Observable<UserResponse[]>;
  filteredLeaders$: Observable<UserResponse[]>;
  currentUser: UserResponse | null = null;
  isLeader: boolean = false;

  @ViewChild('currentMembersInput', { static: true }) currentMembersInput!: ElementRef;
  @ViewChild('leadersInput', { static: true }) leadersInput!: ElementRef;

  private originalProjectData: ProjectData | null = null;
  private destroy$ = new Subject<void>();

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

    this.filteredMembers$ = combineLatest([
      this.currentUsers.valueChanges.pipe(
        startWith([]),
        map(currentUsers => currentUsers.map((user: UserResponse) => user.email))
      ),
      fromEvent<InputEvent>(this.currentMembersInput.nativeElement, 'input').pipe(
        debounceTime(300),
        distinctUntilChanged(),
        map((event: InputEvent) => (event.target as HTMLInputElement).value.trim())
      )
    ]).pipe(
      switchMap(([currentUserEmails, searchQuery]) =>
        this.userService.searchUsers(searchQuery).pipe(
          map(users => users.filter(user => !currentUserEmails.includes(user.email))),
          catchError(() => of([]))
        )
      ),
      takeUntil(this.destroy$)
    );
    
    this.filteredLeaders$ = combineLatest([
      this.project_leaders.valueChanges.pipe(
        startWith([]),
        map(projectLeaders => projectLeaders.map((user: UserResponse) => user.email))
      ),
      fromEvent<InputEvent>(this.leadersInput.nativeElement, 'input').pipe(
        debounceTime(300),
        distinctUntilChanged(),
        map((event: InputEvent) => (event.target as HTMLInputElement).value.trim())
      )
    ]).pipe(
      switchMap(([projectLeaderEmails, searchQuery]) =>
        this.userService.searchUsers(searchQuery).pipe(
          map(users => users.filter(user => !projectLeaderEmails.includes(user.email))),
          catchError(() => of([]))
        )
      ),
      takeUntil(this.destroy$)
    );
  }

  ngOnInit(): void {
    this.authService.fetchCurrentUser()
      .pipe(takeUntil(this.destroy$))
      .subscribe(
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

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
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
    this.projectService.getProject(id)
      .pipe(takeUntil(this.destroy$))
      .subscribe(
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

          this.isLeader = project.project_leaders.some((leader: UserResponse) => leader.email === this.currentUser?.email);
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
    this.currentUsers.clear();
    users.forEach(user => this.currentUsers.push(this.fb.control(user)));
  }

  setProjectLeaders(users: UserResponse[]): void {
    this.project_leaders.clear();
    users.forEach(user => this.project_leaders.push(this.fb.control(user)));
  }

  saveProject(): void {
    if (this.projectForm.valid) {
      const projectData: ProjectData = {
        ...this.projectForm.value,
        team_members: this.currentUsers.value.filter((user: UserResponse) => user.email),
        project_leaders: this.project_leaders.value.filter((user: UserResponse) => user.email)
      };

      if (this.isNewProject) {
        this.projectService.createProject(projectData)
          .pipe(takeUntil(this.destroy$))
          .subscribe(
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
        this.projectService.updateProject(id!, projectData)
          .pipe(takeUntil(this.destroy$))
          .subscribe(
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

  addUser(user: UserResponse, type: 'users' | 'leaders', input: HTMLInputElement): void {
    if (type === 'users') {
      this.currentUsers.push(this.fb.control(user));
    } else {
      this.project_leaders.push(this.fb.control(user));
    }
    input.value = ''; // Clear the input field
  }

  removeUser(index: number, type: 'users' | 'leaders'): void {
    if ((this.isLeader || this.isNewProject) && (type === 'users' || type === 'leaders')) {
      const formArray = type === 'users' ? this.currentUsers : this.project_leaders;
      formArray.removeAt(index);

      // Re-fetch users to update the dropdown
      const inputElement = type === 'users' ? this.currentMembersInput.nativeElement : this.leadersInput.nativeElement;
      this.searchUsers({ target: inputElement } as Event, type);
    }
  }

  cancelChanges(): void {
    if (this.isNewProject) {
      this.projectForm.reset();
      this.currentUsers.clear();
      this.project_leaders.clear();
    } else {
      this.projectForm.patchValue({
        name: this.originalProjectData!.name,
        description: this.originalProjectData!.description,
      });

      // Clear and reset team_members and project_leaders FormArrays
      this.currentUsers.clear();
      this.project_leaders.clear();
      this.originalProjectData!.team_members.forEach((user: UserResponse) => {
        this.currentUsers.push(this.fb.control(user));
      });
      this.originalProjectData!.project_leaders.forEach((user: UserResponse) => {
        this.project_leaders.push(this.fb.control(user));
      });
    }
    this.router.navigate(['/projects']);
  }

  searchUsers(event: Event, type: 'users' | 'leaders' = 'users'): void {
    const input = event.target as HTMLInputElement;
    const query = input.value;
  }

  get f(): { [key: string]: AbstractControl } {
    return this.projectForm.controls;
  }
}
