import { Component } from "@angular/core";
import { Route } from "@angular/router";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.css"],
})
export class HomeComponent {
  public static Route: Route = {
    path: "",
    component: HomeComponent,
    title: "Home Page",
  };
}
