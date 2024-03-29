import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from 'src/app/services/auth.service';
import { Auth } from 'src/app/interfaces/auth';
import { Token } from 'src/app/interfaces/token';
import { UserService } from 'src/app/services/user.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-connexion',
  templateUrl: './connexion.component.html',
  styleUrls: ['./connexion.component.css']
})
export class ConnexionComponent {

  form!: FormGroup;
  error: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private userService:UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  get f() { return this.form.controls; }

  onLogin() {
    const auth: Auth = {
      email: this.form.value.email,
      password: this.form.value.password
    };

    this.authService.login(auth)
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
