import { Component } from '@angular/core';

import { User } from 'src/app/interfaces/user';
import { Password } from 'src/app/interfaces/password';
import { UserService } from 'src/app/services/user.service';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent {

  user: User = <User>{};
  password: Password = <Password>{};

  constructor(public userService: UserService) { 
    this.user = this.userService.user;
  }

  updateUser() {
    console.log(this.user);
    // this.userService.updateUser(this.user)
    //   .subscribe(
    //     (user: User) => {
    //       this.user = user;
    //       console.log(this.user);
    //     }
    //   );
  }

  changePassword() {
    console.log(this.password);
  }

}
