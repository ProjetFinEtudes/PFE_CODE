import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class TagService {
  private apiUrl = 'http://localhost:3212/api/tag'; // Remplacez par l'URL de votre API
  token: string = ""
  constructor(private http: HttpClient,private authService: AuthService) {
    this.token = this.authService.getAccessToken()!
   }

  createTag(tagName: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`
    });
    const url = `${this.apiUrl}/`;
    return this.http.post(url+'?tag_name='+tagName, { headers: headers });
  }

  getAllTags(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`
    });
    const url = `${this.apiUrl}/get_all`;
    return this.http.get(url, { headers: headers });
  }

  getUserTags(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`
    });
    const url = `${this.apiUrl}/get_user_tags`;
    return this.http.get(url, { headers: headers });
  }

  deleteUserTag(userId: number, tagName: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.token}`
    });
    const url = `${this.apiUrl}/user_tags/${userId}/${tagName}`;
    return this.http.delete(url, { headers: headers });
  }
}
