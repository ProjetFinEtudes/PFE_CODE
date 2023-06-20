import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { User } from '../interfaces/user';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';
import { Passwords, Password } from '../interfaces/password';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  token: string |null ='';
  user: User = <User>{};

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {
    if (this.authService.isLoggedIn()) {
      this.token = this.authService.getAccessToken()!;
      this.getUser()
      .then((user: User) => {
        this.setUser(user);
      });
    }
  }

  async getUser(): Promise<User> {
    const token = this.authService.getAccessToken()
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    
    let user = await this.http.get<User>(`http://localhost:3212/api/user`, { headers }).toPromise()
    return user!
  }

  setUser(user: User) {
    this.user = user;
  }

  clearUser() {
    this.user = <User>{};
  }

  updateUser(user: User): Observable<User> {
    const token = this.authService.getAccessToken()
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    return this.http.patch<User>(`http://localhost:3212/api/user`, user, { headers });
  }

  updatePassword(passwords: Passwords): Observable<Password> {
    const token = this.authService.getAccessToken()
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    const new_password: Password = { "password": passwords.new_password };
    return this.http.patch<Password>(`http://localhost:3212/api/auth/`, new_password, { headers });
  }


}
