import { Component, OnInit, ViewChild, OnDestroy, Renderer2 } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { MatAutocomplete } from '@angular/material/autocomplete';
import { ChatService } from 'src/app/services/chat.service';

interface ConversationData {
  id: number;
  conversation: ChatMessage[];
}

interface ChatMessage {
  fromu: 'user' | 'bot';
  text: string;
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit, OnDestroy {
  userInput: string = '';
  messages: ChatMessage[] = [];
  filteredOptions: Observable<string[]> | undefined;
  @ViewChild(MatAutocomplete) auto!: MatAutocomplete;
  isModalOpen: boolean = false;
  chatInput = new FormControl();
  waitingForBot: boolean = false;
  conversationHistory: ConversationData[] = [];
  activeConvId: number = 0
  constructor(private chatService: ChatService, private renderer: Renderer2) {
    this.setConversationData();
  }

  ngOnInit(): void {
    this.renderer.setStyle(document.body, 'overflow-y', 'hidden');
  }

  ngOnDestroy(): void {
    this.renderer.removeStyle(document.body, 'overflow-y');
  }

  async convertConversationData(conversationData: any[]): Promise<ConversationData[]> {
    return Promise.all(
      conversationData.map(async (data: any) => {
        const conversation = JSON.parse(data.conversation);
        return {
          id: data.id,
          conversation: conversation.messages.map((message: ChatMessage) => ({
            fromu: message.fromu,
            text: message.text
          }))
        };
      })
    );
  }

  async setConversationData(): Promise<void> {
    const convDat = await this.chatService.getConversation().toPromise();
    this.conversationHistory = await this.convertConversationData(convDat!);
  }

  async sendMessage(): Promise<void> {
    if (this.userInput.trim() === '') {
      return;
    }
    this.waitingForBot = true;
    this.messages.push({ fromu: 'user', text: this.userInput });
    this.chatService.sendMessage(this.userInput).subscribe(response => {
      this.messages.push({ fromu: 'bot', text: response.response });
      this.waitingForBot = false;
    });
    this.userInput = '';
  }

  displayConversation(conv: ConversationData): void {
    this.activeConvId=conv.id
    this.messages = conv.conversation;
  }

  saveConversation(): void {
    const activeConversation: ConversationData = {
      id: this.conversationHistory.length + 1,
      conversation: this.messages
    };
    this.chatService.createConversation(this.activeConvId,this.messages).subscribe(res => {
      this.setConversationData();
      alert('Conversation Saved');
    });
  }

  openModal(): void {
    this.isModalOpen = true;
  }

  closeModal(): void {
    this.isModalOpen = false;
  }

  onKeyPress(event: KeyboardEvent): void {
    if (event.keyCode === 13) {
      this.sendMessage();
    }
  }
  deleteConversation(id: any){
    this.chatService.deleteConversation(id).subscribe((res)=>{
      console.log(res)
      this.setConversationData()
    })
  }
  newConv(){
    this.messages = []
  }
}
