import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { AuthComponent } from "./auth/auth.component";
import { HomeComponent } from "./home/home.component";
import { ProfileComponent } from "./profile/profile.component";
import { ProjectsComponent } from "./projects/projects.component";
import { ProjectFormComponent } from "./projects/project-form/project-form.component";

const routes: Routes = [
  HomeComponent.Route,
  AuthComponent.Route,
  ProfileComponent.Route,
  ProjectsComponent.Route,
  ProjectFormComponent.Route,
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
