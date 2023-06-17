import { Component, OnInit, ViewChild, AfterContentInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { MatAutocomplete } from '@angular/material/autocomplete';
import { ChatService } from 'src/app/services/chat.service';
interface ChatMessage {
  fromu: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, AfterContentInit {
  userInput: string = '';
  messages: ChatMessage[] = [];
  filteredOptions: Observable<string[]> | undefined;
  @ViewChild(MatAutocomplete) auto!: MatAutocomplete;

  chatInput = new FormControl();
  waitingForBot: boolean = false;
  conversationHistory: ChatMessage[][] = [[]];
  constructor(private chatService: ChatService) {
    this.setConversationData()
  }
  ngOnInit(): void {

  }

  ngAfterContentInit(): void {
  }
  convertConversationData(conversationData: any[]): ChatMessage[][] {
    return conversationData.map(data => {
      const conversation = JSON.parse(data.conversation);
      return conversation.messages.map((message: ChatMessage) => ({
        fromu: message.fromu,
        text: message.text
      }));
    });
  }
  async setConversationData(){
    let convDat = await this.chatService.getConversation().toPromise()
    this.conversationHistory = await this.convertConversationData(convDat!);
  }
  async sendMessage(): Promise<void> {
    this.conversationHistory
    console.log(this.userInput)
    if (this.userInput.trim() === '') {
      console.log('ici')
      return;
    }
    this.waitingForBot=true
    this.messages.push({ fromu: 'user', text: this.userInput });
    this.chatService.sendMessage(this.userInput).subscribe(response => {
      this.messages.push({ fromu: 'bot', text: response.response });
      this.waitingForBot=false
    console.log(this.messages)
    });
    console.log(this.messages)
    this.userInput = '';
  }
  displayConversation(conv:ChatMessage[]){
    this.messages = conv
  }
  saveConversation(){
    this.chatService.createConversation(this.messages).subscribe((res)=>{
      this.setConversationData()
      alert('Conversation Saved')

    })
  }
}
