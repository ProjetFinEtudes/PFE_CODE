import * as moment from 'moment';
//import * as bcrypt from 'bcryptjs';

import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { MAT_MOMENT_DATE_FORMATS } from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { first } from 'rxjs';
import { HttpClient } from '@angular/common/http';


import { Auth } from 'src/app/interfaces/auth';
import { User } from 'src/app/interfaces/user';

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
    private http: HttpClient,
    private authService: AuthService,
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

  onSubmit() {
    let auth: Auth = {
      email: this.form.value.email,
      password: this.form.value.password
    }
    let user: User = {
      first_name: this.form.value.firstname,
      last_name: this.form.value.lastname,
      birth_date: this.form.value.birthdate.toLocaleDateString(),
      genre: this.form.value.genre,
      id_auth: 0
    }

    const json = {
      "data": user,
      "credentials": auth
    }

    this.http.post(`http://localhost:3212/api/auth/register`, json)
      .subscribe({
        next: (response) => {
          console.log(response);
          this.router.navigate(['/connexion']);
        },
        error: (error) => {
          console.log(error);
          this.errorUser = (error.status == 400 || error.status == 409);
          this.errorServer = (error.status == 500);
        }
      });
  }


}
