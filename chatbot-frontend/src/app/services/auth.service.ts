import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Auth } from '../interfaces/auth';
import { User } from '../interfaces/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private GATEWAY_URL: string = 'http://localhost:3212/api/';

  constructor(
    private http: HttpClient
  ) { }

  register(formData: any) {
    //return this.http.post(`${this.GATEWAY_URL}auth/register`, { auth, user });
    return this.http.post(`http://localhost:3212/api/auth/register`, formData);
  }

}
