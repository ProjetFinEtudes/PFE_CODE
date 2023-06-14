import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Auth } from '../interfaces/auth';
import { User } from '../interfaces/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private GATEWAY_URL = 'http://localhost:3212/api';

  constructor(
    private http: HttpClient
  ) { }

  register(auth: Auth, user: User) {
    return this.http.post(`${this.GATEWAY_URL}/auth/register`, { auth, user });
  }

}
