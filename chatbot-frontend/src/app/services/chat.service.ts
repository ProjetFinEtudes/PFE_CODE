import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

interface ChatMessage {
  fromu: 'user' | 'bot';
  text: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private chatUrl = 'http://localhost:3212/api/chat'; // Update with your API URL
  conversationHistory: ChatMessage[][] = []
  constructor(private http: HttpClient,private authService:AuthService) {
  }
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

    return this.http.post<any>(`${this.chatUrl}/chat`, body, { headers: headers });
  }
   convertToNewFormat(conversationHistory:ChatMessage[]) {
    const newFormat = {
      messages: conversationHistory.map(conversation => ({
        fromu: conversation.fromu,
        text: conversation.text
      }))
    };

    return newFormat;
  }

  createConversation(conv_id:number,conversation: ChatMessage[]): Observable<any> {
    const token = sessionStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };
    let conv = this.convertToNewFormat(conversation)
    if(conv_id == 0)
    {
      return this.http.post<any>(`${this.chatUrl}/chat_message`, conv, { headers });
    } else
    {
      return this.http.put<any>(`${this.chatUrl}/update_chat?id_conv=${conv_id}`, conv, { headers })
    }
  }

  getConversation(): Observable<ChatMessage[]> {
    const token = sessionStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };
    return this.http.get<ChatMessage[]>(`${this.chatUrl}/get_chat`, { headers });
  }
  deleteConversation(id:any){
    const token = sessionStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };
    return this.http.delete<ChatMessage[]>(`${this.chatUrl}/delete_chat?chat_id=${id}`, { headers });
  }
}
