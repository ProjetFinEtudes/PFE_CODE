import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'src/app/services/auth.service';
import { Auth } from 'src/app/interfaces/auth';
import { Token } from 'src/app/interfaces/token';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-connexion',
  templateUrl: './connexion.component.html',
  styleUrls: ['./connexion.component.css']
})
export class ConnexionComponent {

  auth: Auth = {
    email: '',
    password: ''
  };

  error: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private userService:UserService
  ) { }

  onLogin() {
    this.authService.login(this.auth)
      .subscribe({
        next: (res: any) => {
          const token: Token = {
            access_token: res.access_token,
            token_type: res.token_type
          };
          this.authService.setToken(token);

          this.userService.getUser().then((res) => this.userService.user = res)

          this.router.navigate(['/']);
        },
        error: (err: any) => {
          console.log(err) ;
          this.error = true;
        }
    });
  }


}
