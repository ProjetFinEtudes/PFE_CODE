import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {MatCardModule} from '@angular/material/card';
import { MatDatepickerModule } from '@angular/material/datepicker';

@NgModule({
    declarations: [],
    imports: [
        CommonModule,
        MatCardModule,
        MatDatepickerModule
    ],
    exports: [
        MatCardModule,
        MatDatepickerModule
    ],
})
export class AngularMaterialModule { }
