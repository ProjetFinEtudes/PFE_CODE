import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InscriptionComponent } from './pages/authentication/inscription/inscription.component';
import { HomeComponent } from './pages/home/home.component';
import { ConnexionComponent } from './pages/authentication/connexion/connexion.component';
import { ChatComponent } from './pages/chat/chat.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { AuthGuard } from './securite/auth.guard';
import { NotFoundComponent } from './pages/common/not-found/not-found.component';
import { AccessDeniedComponent } from './pages/common/access-denied/access-denied.component';

const routes: Routes = [
  { path: '', component: HomeComponent},
  { path: 'register', component: InscriptionComponent },
  { path: 'connexion', component: ConnexionComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'chat', component: ChatComponent, canActivate: [AuthGuard] },
  { path: 'access-denied', component: AccessDeniedComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
