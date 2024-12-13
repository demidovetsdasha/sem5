import {Component, OnInit} from '@angular/core';
import {EventService} from "../../service/event.service";
import {NotificationService} from "../../service/notification.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-post-index',
  templateUrl: './pastIndex.component.html',
  styleUrl: './pastIndex.component.css'
})
export class PastIndexComponent  implements OnInit{

  constructor(
    private packageService: EventService,
    private notificationService: NotificationService,
    private router: Router
  ) {
  }


  ngOnInit(): void {
    console.log(1)
  }

  openIndex(){
    this.router.navigate(["index"])
  }

}
