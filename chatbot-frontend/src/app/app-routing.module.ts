import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { InscriptionComponent } from './pages/authentication/inscription/inscription.component';
import { HomeComponent } from './pages/common/home/home.component';
import { ConnexionComponent } from './pages/authentication/connexion/connexion.component';
import { ChatComponent } from './pages/chat/chat.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { AuthGuard } from './securite/auth.guard';
import { NotFoundComponent } from './pages/common/not-found/not-found.component';
import { AccessDeniedComponent } from './pages/common/access-denied/access-denied.component';
import { ContactComponent } from './pages/common/contact/contact.component';
import { TermsAndConditionsComponent } from './pages/common/terms-and-conditions/terms-and-conditions.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'register', component: InscriptionComponent },
  { path: 'connexion', component: ConnexionComponent },
  { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
  { path: 'chat', component: ChatComponent, canActivate: [AuthGuard] },
  { path: 'contact-us', component: ContactComponent },
  { path: 'terms-and-conditions', component: TermsAndConditionsComponent },
  { path: 'access-denied', component: AccessDeniedComponent },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
