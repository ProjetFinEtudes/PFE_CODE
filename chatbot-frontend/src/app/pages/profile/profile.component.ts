import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

import { User } from 'src/app/interfaces/user';
import { PasswordsAndConfirmPassword, Passwords } from 'src/app/interfaces/password';
import { UserService } from 'src/app/services/user.service';
import { TagService } from 'src/app/services/tag.service';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { Action } from 'src/app/interfaces/action';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  user: User = <User>{};
  passwords: PasswordsAndConfirmPassword = <PasswordsAndConfirmPassword>{};
  action: Action = <Action>{};

  availableTags: any[] = [];
  selectedTags: number[] = [];
  userTags: any[] = [];
  tagControl = new FormControl();

  constructor(private userService: UserService,
    private authService: AuthService,
    private tagService: TagService,
    private router: Router
  ) {
    console.log(this.user)
  }

  async ngOnInit(): Promise<void> {
    await this.userService.getUser()
      .then((user: User) => {
        console.log(user);
        this.user = user;
      });

    this.tagService.getAllTags()
      .subscribe({
        next: (response: any[]) => {
          this.availableTags = response;
          this.selectedTags = this.availableTags
            .filter(tag => this.userTags.includes(tag.name))
            .map(tag => tag.id);
          this.tagControl.setValue(this.selectedTags);
        },
        error: () => {
          this.displayMessageFewSeconds('An error occurred while fetching tags', 'danger');
        }
      });

    this.tagService.getUserTags()
      .subscribe((res) => {
        this.userTags = res;
      });

    this.tagControl.valueChanges
      .subscribe((selectedValues: number[]) => {
        selectedValues.forEach((selectedValue: number) => {
          const selectedTag = this.availableTags.find(tag => tag.id === selectedValue);
          if (selectedTag && !this.userTags.includes(selectedTag.name)) {
            this.userTags.push(selectedTag.name);
            this.tagService.createTag(selectedTag.name).subscribe(res => {
              this.displayMessageFewSeconds('Tag added successfully', 'success');
            });
          }
        });
    
      this.userTags = this.userTags.filter(tag => selectedValues.includes(this.availableTags.find(t => t.name === tag)?.id));
    });
  }

  setActionMessage(msg: string, className: string) {
    this.action = {
      message: msg,
      class: className
    };
  }

  clearActionMessage() {
    this.action = <Action>{};
  }

  displayMessageFewSeconds(content: string, className: string) {
    this.setActionMessage(content, className);
    setTimeout(() => this.clearActionMessage(), 5000);
  }

  isAllUserFieldsFilled() {
    return ((this.user.first_name === undefined || this.user.first_name === '')
    || (this.user.last_name === undefined || this.user.last_name === '')
    || (this.user.birth_date === undefined || this.user.birth_date === '')
    || (this.user.genre === undefined || this.user.genre === ''))
  }

  updateUser() {
    this.user.birth_date = this.userService.formatDate(this.user.birth_date);
    this.userService.updateUser(this.user)
      .subscribe(
        (user: User) => {
          this.user = user;
          this.displayMessageFewSeconds('User updated successfully', 'success');
        }
      );
  }

  deleteTag(tagId: any) {
    const tagToRemove = this.availableTags.find(tag => tag.id === tagId);
    if (tagToRemove) {
      const tagName = tagToRemove.name;
      this.userTags = this.userTags.filter(tag => tag !== tagName);
      this.tagService.deleteUserTag(tagName).subscribe((res) => console.log(res));
    }
  }

  isAllPasswordFieldsFilled() {
    return ((this.passwords.current_password === undefined || this.passwords.current_password === '')
    || (this.passwords.new_password === undefined || this.passwords.new_password === '')
    || (this.passwords.confirm_password === undefined || this.passwords.confirm_password === ''))
  }

  delayLogoutAndRoot(route: string) {
    setTimeout(() => {
      this.authService.clearToken();
      this.userService.clearUser();
      this.router.navigate([route]);
    }, 5000);
  }

  changePassword() {
    if (this.passwords.new_password === this.passwords.confirm_password) {
      this.authService.updatePassword(this.passwords)
        .subscribe({
          next: () => {
            console.log('Password updated successfully');
            this.displayMessageFewSeconds('Password updated successfully', 'success');
            this.delayLogoutAndRoot('/connexion');
          },
          error: () => {
            this.displayMessageFewSeconds('Your current password is incorrect', 'danger');
          }
        });
    } else {
      this.displayMessageFewSeconds('New passwords do not match', 'danger');
    }
  }

  deleteAccount() {
    this.authService.deleteAccount()
      .subscribe({
        next: () => {
          console.log('Account deleted successfully');
          this.displayMessageFewSeconds('Account deleted successfully', 'success');
          this.delayLogoutAndRoot('/');
        }
      });
  }

  tagClick(tagId: any) {
    const tagIndex = this.tagControl.value.indexOf(tagId);
    const isSelected = tagIndex > -1;

    if (!isSelected) {
      // La case a été décochée
      this.deleteTag(tagId);
    }
  }


}
