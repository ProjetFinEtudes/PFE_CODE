import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { InscriptionComponent } from './pages/authentication/inscription/inscription.component';

const routes: Routes = [
  { path: '', component: InscriptionComponent },
  { path: 'inscription', component: InscriptionComponent },
  { path: '**', component: InscriptionComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
