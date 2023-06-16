import { Component, OnInit, ViewChild, AfterContentInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { MatAutocomplete } from '@angular/material/autocomplete';
import { ChatService } from 'src/app/services/chat.service';
interface ChatMessage {
  from: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  userInput: string = '';
  messages: ChatMessage[] = [];
  filteredOptions: Observable<string[]> | undefined;
  @ViewChild(MatAutocomplete) auto!: MatAutocomplete;

  chatInput = new FormControl();
  waitingForBot: boolean = false;
  constructor(private chatService: ChatService) {}

  ngOnInit() {
  }


  sendMessage(): void {
    console.log(this.userInput)
    if (this.userInput.trim() === '') {
      console.log('ici')
      return;
    }
    this.waitingForBot=true
    this.messages.push({ from: 'user', text: this.userInput });
    this.chatService.sendMessage(this.userInput).subscribe(response => {
      this.messages.push({ from: 'bot', text: response.response });
      this.waitingForBot=false

    });
    console.log(this.messages)
    this.userInput = '';
  }
}
