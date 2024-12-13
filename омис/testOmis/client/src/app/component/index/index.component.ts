import {Component, OnInit} from '@angular/core';
import {EventService} from "../../service/event.service";
import {NotificationService} from "../../service/notification.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrl: './index.component.css'
})
export class IndexComponent  implements OnInit{

  constructor(
    private packageService: EventService,
    private notificationService: NotificationService,
    private router: Router
  ) {
  }


  ngOnInit(): void {
    console.log(1)
  }

  addEvent(){
    this.router.navigate(["add"])
  }

  openPastIndex(){
    this.router.navigate(["pastIndex"])
  }

}
