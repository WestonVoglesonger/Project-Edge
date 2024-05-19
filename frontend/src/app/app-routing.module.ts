import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { CreateAccountComponent } from "./users/create-account/create-account.component";
import { LoginComponent } from "./users/login/login.component";

const routes: Routes = [CreateAccountComponent.Route, LoginComponent.Route];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
