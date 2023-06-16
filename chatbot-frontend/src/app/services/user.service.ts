import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { User } from '../interfaces/user';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  token: string = '';
  user: User = <User>{};

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { 
    this.token = this.authService.getAccessToken()!;
    //this.getUser();
  }



}
