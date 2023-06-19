import { Component, OnInit } from '@angular/core';

import { User } from 'src/app/interfaces/user';
import { Password } from 'src/app/interfaces/password';
import { UserService } from 'src/app/services/user.service';
import { TagService } from 'src/app/services/tag.service';


@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit{

  user: User = <User>{};
  password: Password = <Password>{};
  availableTags: any[] = [];
  selectedTag: number | null = null;
  userTags:any[]=[]

  constructor(public userService: UserService,private tagService:TagService) {
    this.user = this.userService.user;
    console.log(this.user)
  }

  ngOnInit(): void {
    this.tagService.getAllTags().subscribe(
      (      response: any[]) => {
        this.availableTags = response;
      },
      error => {
          alert('An error occurred while fetching tags')
      }
    );
    this.tagService.getUserTags().subscribe((res)=>{
      this.userTags = res
    })
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
  onTagSelected() {
    if (this.selectedTag) {
      const selectedTagName = this.availableTags.find(tag => tag.id === this.selectedTag)?.name;
      if (selectedTagName) {
        // Ajouter le tag sélectionné à la liste des tags de l'utilisateur
        this.userTags.push(selectedTagName);
        this.tagService.createTag(selectedTagName).subscribe((res)=>console.log(res))
      }
      this.selectedTag = null; // Réinitialiser la sélection du tag
    }
  }
  changePassword() {
    console.log(this.password);
  }

}
