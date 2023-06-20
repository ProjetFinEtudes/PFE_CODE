import { Component, OnInit, ViewChild, OnDestroy,Renderer2  } from '@angular/core';
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
export class ChatComponent implements OnInit, OnDestroy {
  userInput: string = '';
  messages: ChatMessage[] = [];
  filteredOptions: Observable<string[]> | undefined;
  @ViewChild(MatAutocomplete) auto!: MatAutocomplete;
  isModalOpen:boolean=false
  chatInput = new FormControl();
  waitingForBot: boolean = false;
  conversationHistory: ChatMessage[][] = [[]];
  constructor(private chatService: ChatService,private renderer: Renderer2) {
    this.setConversationData()
  }
  ngOnInit(): void {
    this.renderer.setStyle(document.body, 'overflow-y', 'hidden');
  }

  ngOnDestroy(): void {
    this.renderer.removeStyle(document.body, 'overflow-y');
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
      console.log(this.conversationHistory)
    })
  }
  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
  }
  onKeyPress(event: KeyboardEvent) {
    if (event.keyCode === 13) { // Vérifie si la touche appuyée est la touche Entrée
      this.sendMessage(); // Appelle la fonction sendMessage()
    }
  }
}
