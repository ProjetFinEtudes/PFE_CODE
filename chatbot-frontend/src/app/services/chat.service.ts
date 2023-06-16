import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private chatUrl = 'http://localhost:3212/api/chat/chat'; // Update with your API URL

  constructor(private http: HttpClient,private authService:AuthService) {}

  sendMessage(message: string): Observable<any> {
    const accessToken = this.authService.getAccessToken();
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    });

    const body = {
      message: message
    };

    return this.http.post<any>(this.chatUrl, body, { headers: headers });
  }
}
