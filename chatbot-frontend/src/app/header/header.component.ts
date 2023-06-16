import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../services/auth.service';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  constructor(
    public authService: AuthService,
    private userService: UserService,
    private router: Router
  ) { }

  logout() {
    this.authService.clearToken();
    //this.userService.clearUser();
    window.localStorage.clear();
    window.sessionStorage.clear();

    this.router.navigate(['/']);
  }

}
