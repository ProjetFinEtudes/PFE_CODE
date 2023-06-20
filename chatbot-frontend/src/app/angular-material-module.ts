import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatCardModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSelectModule,
    MatInputModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatListModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatIconModule
  ],
  exports: [
    MatCardModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSelectModule,
    MatInputModule,
    MatAutocompleteModule,
    MatButtonModule,
    MatListModule,
    MatProgressSpinnerModule,
    MatFormFieldModule,
    MatIconModule
  ]
})
export class AngularMaterialModule { }
