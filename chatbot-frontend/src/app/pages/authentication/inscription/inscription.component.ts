import * as moment from 'moment';

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DATE_FORMATS } from '@angular/material/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';


import { first } from 'rxjs';
import { Auth } from 'src/app/interfaces/auth';
import { User } from 'src/app/interfaces/user';

export const MY_FORMATS = {
  parse: {
    dateInput: 'DD/MM/YYYY',
  },
  display: {
    dateInput: 'DD/MM/YYYY',
    monthYearLabel: 'YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'YYYY',
  },
};

@Component({
  selector: 'app-inscription',
  templateUrl: './inscription.component.html',
  styleUrls: ['./inscription.component.css']
})
export class InscriptionComponent implements OnInit {

  form!: FormGroup;
  maxDate = moment().subtract(1, 'y');
  errorServer: boolean = false;
  errorUser: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.form = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      birth_date: ['', Validators.required],
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
      first_name: this.form.value.first_name,
      last_name: this.form.value.last_name,
      birth_date: this.form.value.birth_date.format('YYYY-MM-DD'),
      genre: this.form.value.genre
    }

    this.errorServer = false;
    this.errorUser = false;

    this.authService.register(auth, user)
      .pipe(first())
      .subscribe({
        next: () => {
          this.router.navigate(['/connexion']);
        },
        error: (error: any) => {
          this.errorUser = (error.status == 400 || error.status == 409);
          this.errorServer = (error.status == 500);
        }
      });
  }


}
