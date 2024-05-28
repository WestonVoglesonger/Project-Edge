import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Route } from '@angular/router';

@Component({
  selector: 'app-project-creation',
  templateUrl: './project-creation.component.html',
  styleUrls: ['./project-creation.component.css']
})
export class ProjectCreationComponent {
  public static Route: Route = {
    path: "projects/creation",
    component: ProjectCreationComponent,
    title: "Project Creation Page",
  };
  projectForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.projectForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(3)]],
      description: ['', [Validators.required, Validators.minLength(10)]],
      currentUsers: ['', Validators.required],
      owners: ['', Validators.required]
    });
  }

  ngOnInit(): void {}

  get f() { return this.projectForm.controls; }

  onSubmit(): void {
    if (this.projectForm.invalid) {
      return;
    }

    // Logic to handle project creation, e.g., sending data to the server
    console.log('Project created:', this.projectForm.value);

    // Reset the form
    this.projectForm.reset();
  }
}
