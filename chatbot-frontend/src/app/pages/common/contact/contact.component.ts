import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent {
  form!: FormGroup;
  isMessageSent = false;

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.form = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', Validators.required],
      message: ['', Validators.required]
    });
  }

  get f() { return this.form.controls; }

  onSend() {
    if (this.form.valid) {
      this.isMessageSent = true;
      setTimeout(() => { 
        this.isMessageSent = false; 
      }, 3000);

      this.form.reset();
    }
  }

}
