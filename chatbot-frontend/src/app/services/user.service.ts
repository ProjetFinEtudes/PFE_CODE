import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { User } from '../interfaces/user';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

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
    this.getUser()
      .subscribe(
        (user: User) => {
          this.user = user;
        }
      );

  }


  getUser(): Observable<User> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.token}`
    });

    return this.http.get<User>(`http://localhost:3212/api/user`, { headers });
  }

  updateUser(user: User): Observable<User> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.token}`
    });

    return this.http.put<User>(`http://localhost:3212/api/user`, user, { headers });
  }


}
