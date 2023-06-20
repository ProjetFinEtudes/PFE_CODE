import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';

import { Token } from '../interfaces/token';
import { Auth } from '../interfaces/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private token: Token = {
    access_token: '',
    token_type: ''
  };
  private isConnectedSubject = new BehaviorSubject<boolean>(false);
  isConnected = this.isConnectedSubject.asObservable();

  constructor(
    private http: HttpClient
  ) {
    const accessToken = localStorage.getItem('token');
    if (accessToken) {
      this.token.access_token = accessToken;
      this.isConnectedSubject.next(true);
    }
  }

  setToken(token: Token) {
    this.token = token;
    console.log(this.token);
    sessionStorage.setItem('token', token.access_token);
    this.isConnectedSubject.next(true);
  }

  isLoggedIn() {
    return !(sessionStorage.getItem('token') === null);
  }

  getToken() {
    return this.token;
  }

  getAccessToken() {
    if (this.token.access_token === '') {
      return sessionStorage.getItem('token');
    } else {
      return this.token.access_token;
    }
  }

  clearToken() {
    this.token = {
      access_token: '',
      token_type: ''
    };
    sessionStorage.removeItem('token');
    this.isConnectedSubject.next(false);
  }

  register(json: any) {
    return this.http.post(`http://localhost:3212/api/auth/register`, json);
  }

  login(auth: Auth) {
    let formData = new FormData()
    formData.append('username', auth.email);
    formData.append('password', auth.password);
    return this.http.post(`http://localhost:3212/api/auth/login`, formData);
  }

}
