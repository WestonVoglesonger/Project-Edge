import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { ProjectService } from '../projects.service';
import { UserResponse } from 'src/app/shared/users/user.models';

@Component({
  selector: 'app-project-form',
  templateUrl: './project-form.component.html',
  styleUrls: ['./project-form.component.css']
})
export class ProjectFormComponent {
  public static Route: Route = {
    path: "projects/:id",
    component: ProjectFormComponent,
    title: "Project Form Page",
  };

  projectForm: FormGroup;
  isNewProject: boolean = true;

  constructor(
    private fb: FormBuilder,
    private projectService: ProjectService,
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.projectForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      current_users: [[]],
      owners: [[]]
    });
  }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id && id !== 'new') {
        this.isNewProject = false;
        this.loadProject(id);
      }
    });
  }

  loadProject(id: string): void {
    this.projectService.getProject(id).subscribe(
      project => {
        this.projectForm.patchValue(project);
      },
      error => {
        console.error('Error loading project', error);
      }
    );
  }

  saveProject(): void {
    if (this.projectForm.valid) {
      const projectData = {
        ...this.projectForm.value,
        current_users: this.projectForm.value.current_users.filter((user: UserResponse) => user.email),
        owners: this.projectForm.value.owners.filter((user: UserResponse) => user.email)
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
}