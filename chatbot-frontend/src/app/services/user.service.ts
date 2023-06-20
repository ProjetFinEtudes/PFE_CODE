import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { User } from '../interfaces/user';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

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
  }


 async  getUser():Promise<User> {
    const token = this.authService.getAccessToken()
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
    
    let user = await this.http.get<User>(`http://localhost:3212/api/user`, { headers }).toPromise()
    return user!
  }

  updateUser(user: User): Observable<User> {
    const token = this.authService.getAccessToken()
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    return this.http.patch<User>(`http://localhost:3212/api/user`, user, { headers });
  }


}
