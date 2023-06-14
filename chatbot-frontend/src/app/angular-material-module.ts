import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';

@NgModule({
    declarations: [],
    imports: [
        CommonModule,
        MatCardModule,
        MatDatepickerModule,
        MatNativeDateModule
    ],
    exports: [
        MatCardModule,
        MatDatepickerModule,
        MatNativeDateModule
    ],
})
export class AngularMaterialModule { }
