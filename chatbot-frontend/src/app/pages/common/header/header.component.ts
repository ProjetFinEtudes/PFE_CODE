import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../../services/auth.service';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  constructor(
    public authService: AuthService,
    public userService: UserService,
    private router: Router
  ) { }

  logout() {
    // console.log('token before clear: ', this.authService.getAccessToken());
    // console.log('user before clear: ', this.userService.user);

    this.authService.clearToken();
    // console.log('token cleared: ', this.authService.getAccessToken());

    this.userService.clearUser();
    // console.log('user cleared: ', this.userService.user);

    this.router.navigate(['/']);
  }

}
