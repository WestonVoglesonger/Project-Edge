import { Component } from "@angular/core";

@Component({
  selector: "app-navigation",
  templateUrl: "./navigation.component.html",
  styleUrls: ["./navigation.component.css"],
})
export class NavigationComponent {
  constructor() {}

  logout(): void {
    // Implement your logout logic here if needed
    console.log("Logged out");
  }
}
