import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

import { User } from 'src/app/interfaces/user';
import { PasswordsAndConfirmPassword, Passwords } from 'src/app/interfaces/password';
import { UserService } from 'src/app/services/user.service';
import { TagService } from 'src/app/services/tag.service';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  user: User = <User>{};
  passwords: PasswordsAndConfirmPassword = <PasswordsAndConfirmPassword>{};
  availableTags: any[] = [];
  selectedTags: number[] = [];
  userTags: any[] = [];
  tagControl = new FormControl();

  constructor(public userService: UserService, private tagService: TagService) {
    console.log(this.user)
  }

  async ngOnInit(): Promise<void> {
    await this.userService.getUser()
      .then((user: User) => {
        this.user = user;
      });

    this.tagService.getAllTags().subscribe(
      (response: any[]) => {
        this.availableTags = response;
        this.selectedTags = this.availableTags
          .filter(tag => this.userTags.includes(tag.name))
          .map(tag => tag.id);
        this.tagControl.setValue(this.selectedTags);
      },
      error => {
        alert('An error occurred while fetching tags')

      }
    );
    this.tagService.getUserTags().subscribe((res) => {
      this.userTags = res;
    });
    this.tagControl.valueChanges.subscribe((selectedValues: number[]) => {
      selectedValues.forEach((selectedValue: number) => {
        const selectedTag = this.availableTags.find(tag => tag.id === selectedValue);
        if (selectedTag && !this.userTags.includes(selectedTag.name)) {
          this.userTags.push(selectedTag.name);
          this.tagService.createTag(selectedTag.name).subscribe(res => {
              console.log(res)
          });
        }
      });
    
      this.userTags = this.userTags.filter(tag => selectedValues.includes(this.availableTags.find(t => t.name === tag)?.id));
    });
  }

  updateUser() {
    console.log(this.user);
    this.userService.updateUser(this.user)
      .subscribe(
        (user: User) => {
          this.user = user;
          console.log(this.user);
        }
      );
  }

  deleteTag(tagId: any) {
    const tagToRemove = this.availableTags.find(tag => tag.id === tagId);
    if (tagToRemove) {
      const tagName = tagToRemove.name;
      this.userTags = this.userTags.filter(tag => tag !== tagName);
      this.tagService.deleteUserTag(tagId).subscribe((res) => console.log(res));
    }
  }

  changePassword() {
    console.log(this.passwords);
    if (this.passwords.new_password === this.passwords.confirm_password) {
      this.userService.updatePassword(this.passwords)
        .subscribe({
          next: () => {
            console.log('Password updated successfully');
          },
          error: () => {
            console.log('An error occurred while updating password. Maybe your current password is incorrect');
          }
        });
    } else {
      console.log('New passwords do not match');
    }
  }

}
