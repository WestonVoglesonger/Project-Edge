import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { HttpClientModule } from "@angular/common/http";
import { AppRoutingModule } from "./app-routing.module";
import { ReactiveFormsModule } from "@angular/forms";
import { FormsModule } from "@angular/forms";

// Angular Material Components
import { MatButtonModule } from "@angular/material/button";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatIconModule } from "@angular/material/icon";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatListModule } from "@angular/material/list";
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatAutocompleteModule } from "@angular/material/autocomplete";

// Components
import { AppComponent } from "./app.component";
import { AuthComponent } from "./auth/auth.component";
import { NavigationComponent } from "./navigation/navigation.component";
import { HomeComponent } from "./home/home.component";
import { ProfileComponent } from "./profile/profile.component";
import { ProjectsComponent } from "./projects/projects.component";
import { ProjectFormComponent } from "./projects/project-form/project-form.component";
import { ProjectCard } from "./shared/widgets/project-card/project-card";
import { DiscussionsComponent } from "./discussions/discussions.component";
import { DiscussionCard } from "./shared/widgets/discussion-card/discussion-card";
import { DiscussionFormComponent } from "./discussions/discussion-form/discussion-form.component";

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    NavigationComponent,
    HomeComponent,
    ProfileComponent,
    ProjectsComponent,
    ProjectFormComponent,
    ProjectCard,
    DiscussionsComponent,
    DiscussionCard,
    DiscussionFormComponent,
    // Add other component declarations here
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,

    // Angular Material Modules
    MatButtonModule,
    MatToolbarModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatAutocompleteModule,
    // Add other module imports as necessary
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
