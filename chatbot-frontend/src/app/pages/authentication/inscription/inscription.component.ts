import * as moment from 'moment';
//import * as bcrypt from 'bcryptjs';

import { Component, OnInit } from '@angular/core';
import { FormBuilder , FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-inscription',
  templateUrl: './inscription.component.html',
  styleUrls: ['./inscription.component.css'],
  providers: []
})
export class InscriptionComponent implements OnInit {

  form!: FormGroup;
  maxDate = moment().subtract(1, 'y');
  errorServer: boolean = false;
  errorUser: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private userService: UserService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      firstname: ['', Validators.required],
      lastname: ['', Validators.required],
      birthdate: ['', Validators.required],
      genre: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  get f() { return this.form.controls; }

  onRegister() {
    const json = {
      "credentials": {
        email: this.form.value.email,
        password: this.form.value.password
      },
      "data": {
        first_name: this.form.value.firstname,
        last_name: this.form.value.lastname,
        birth_date: this.userService.formatDate(this.form.value.birthdate.toString()),
        genre: this.form.value.genre,
        id_auth: 0
      }
    };

    this.authService.register(json)
      .subscribe({
        next: (res) => {
          this.router.navigate(['/connexion']);
        },
        error: (err) => {
          this.errorUser = (err.status == 400 || err.status == 409);
          this.errorServer = (err.status == 500);
        }
      });
  }


}
