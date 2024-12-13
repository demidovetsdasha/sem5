import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {NotificationService} from "../../service/notification.service";
import {Router} from "@angular/router";
import {EventService} from "../../service/event.service";
import {EventResponse} from "../../model/EventResponse";
import {TokenStorageService} from "../../service/token-storage.service";

@Component({
  selector: 'app-add',
  templateUrl: './add.component.html',
  styleUrl: './add.component.css'
})
export class AddComponent implements OnInit{
  addingForm!: FormGroup;

  constructor(
    private notificationService: NotificationService,
    private packageService: EventService,
    private tokenStorageService: TokenStorageService,
    public router: Router,
    private fb: FormBuilder
  ) {
  }

  createAddingForm(): FormGroup{
    return this.fb.group({
      name: ['', Validators.compose([Validators.required])],
      category: ['', Validators.compose([Validators.required])],
      start: ['', Validators.compose([Validators.required])],
      finish: ['', Validators.compose([Validators.required])],
      author: ['', Validators.compose([Validators.required])],
    })
  }

  ngOnInit(): void {
    this.addingForm = this.createAddingForm();
  }

  submit(){
    console.log(this.addingForm.value)
    this.packageService.add({
      name: this.addingForm.value.name,
      category: this.addingForm.value.category,
      start: this.addingForm.value.start,
      finish: this.addingForm.value.finish,
      author: this.addingForm.value.author
    }).subscribe((data: Object)=>{
      this.router.navigate(["index"])
    }, error=> {
      this.notificationService.showSnackBar("Something went wrong, try again!")
    });

  }

  protected readonly window = window;
}
