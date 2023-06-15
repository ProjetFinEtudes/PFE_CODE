import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(
    private http: HttpClient
  ) { }

  register(json: any) {
    return this.http.post(`http://localhost:3212/api/auth/register`, json);
  }

}
