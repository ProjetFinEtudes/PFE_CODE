import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InscriptionComponent } from './pages/authentication/inscription/inscription.component';
import { ChatComponent } from './pages/chat/chat.component';
import { HomeComponent } from './pages/home/home.component';
const routes: Routes = [
  { path: 'register', component: InscriptionComponent },
  { path: 'inscription', component: InscriptionComponent },
  {path: 'chat',component:ChatComponent},
  {path: '',component:HomeComponent,}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
