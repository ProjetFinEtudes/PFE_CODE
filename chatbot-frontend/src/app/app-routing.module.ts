import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InscriptionComponent } from './pages/authentication/inscription/inscription.component';
import { HomeComponent } from './pages/home/home.component';
import { ConnexionComponent } from './pages/authentication/connexion/connexion.component';
import { Error404Component } from './pages/common/error404/error404.component';
import { ChatComponent } from './pages/chat/chat.component';
import { ProfileComponent } from './pages/profile/profile.component';

const routes: Routes = [
  { path: '', component: HomeComponent},
  { path: 'register', component: InscriptionComponent },
  { path: 'connexion', component: ConnexionComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'chat', component: ChatComponent },
  { path: '**', component: Error404Component }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
