import { Component } from '@angular/core';

import { User } from 'src/app/interfaces/user';
import { Password } from 'src/app/interfaces/password';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {

  user: User = <User>{};
  password: Password = <Password>{};

  changePassword() {
    console.log(this.password);
  }

}
