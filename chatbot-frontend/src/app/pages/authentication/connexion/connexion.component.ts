import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'src/app/services/auth.service';
import { Auth } from 'src/app/interfaces/auth';

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
    private router: Router
  ) { }

  onLogin() {
    this.authService.login(this.auth)
      .subscribe({
        next: (res: any) => {
          localStorage.setItem('token', res.token);
          this.router.navigate(['/']);
        },
        error: (err: any) => { 
          console.log(err) ;
          this.error = true;
        }
    });
  }

}
