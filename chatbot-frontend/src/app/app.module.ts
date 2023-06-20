import { NgModule, LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import localeFr from '@angular/common/locales/fr';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatComponent } from './pages/chat/chat.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './pages/common/header/header.component';
import { FooterComponent } from './pages/common/footer/footer.component';
import { InscriptionComponent } from './pages/authentication/inscription/inscription.component';
import { AngularMaterialModule } from './angular-material-module';
import { ConnexionComponent } from './pages/authentication/connexion/connexion.component';
import { HomeComponent } from './pages/home/home.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { NotFoundComponent } from './pages/common/not-found/not-found.component';
import { AccessDeniedComponent } from './pages/common/access-denied/access-denied.component';

@NgModule({
  declarations: [
    AppComponent,
    ChatComponent,
    InscriptionComponent,
    ConnexionComponent,
    HeaderComponent,
    FooterComponent,
    InscriptionComponent,
    HomeComponent,
    ProfileComponent,
    NotFoundComponent,
    AccessDeniedComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    AngularMaterialModule
  ],
  providers: [
    { provide: LOCALE_ID, useValue: 'fr-FR' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
