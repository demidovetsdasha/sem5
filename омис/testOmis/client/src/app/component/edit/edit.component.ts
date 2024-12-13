import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {NotificationService} from "../../service/notification.service";
import {ActivatedRoute, Router} from "@angular/router";
import {EventService} from "../../service/event.service";
import {EventResponse} from "../../model/EventResponse";

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrl: './edit.component.css'
})
export class EditComponent implements OnInit{
  editForm!: FormGroup;
  id!: string | null;
  intId!: number;
  event!: EventResponse;

  constructor(
    private notificationService: NotificationService,
    private packageService: EventService,
    public router: Router,
    public route: ActivatedRoute,
    private fb: FormBuilder
  ) {
  }

  createAddingForm(data: EventResponse): FormGroup{
    return this.fb.group({
      id: '',
      id1: '',
      name: [data.name, Validators.compose([Validators.required])],
      category: [data.category, Validators.compose([Validators.required])],
      start: [data.start, Validators.compose([Validators.required])],
      finish: [data.finish, Validators.compose([Validators.required])],
      author: [data.author, Validators.compose([Validators.required])],
    })
  }

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.intId = parseInt(this.id as string, 10);

    this.packageService.getById(this.intId).subscribe((data: EventResponse)=>{
      this.event = data
      this.editForm = this.createAddingForm(data);
    }, error=> {
      this.notificationService.showSnackBar("Something went wrong, try again!")
    });
  }

  submit(){
    this.packageService.updateEvent(this.intId, {
      name: this.editForm.value.name,
      category: this.editForm.value.category,
      start: this.editForm.value.start,
      finish: this.editForm.value.finish,
      author: this.editForm.value.author
    }).subscribe((data: Object)=>{
      this.router.navigate(['/details', this.intId]);
    }, error=> {
      this.notificationService.showSnackBar("Something went wrong, try again!")
    })

  }

  protected readonly window = window;
}
