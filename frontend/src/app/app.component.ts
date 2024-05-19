import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  template: `
    <router-outlet>
      <app-auth></app-auth>
    </router-outlet>
  `,
})
export class AppComponent {
  title = "frontend";
}
