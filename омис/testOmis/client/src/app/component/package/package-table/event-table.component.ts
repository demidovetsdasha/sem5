import {Component, Input, OnInit} from '@angular/core';
import {EventService} from "../../../service/event.service";
import {Router} from "@angular/router";
import {Event} from "../../../model/Event";
import {NotificationService} from "../../../service/notification.service";

@Component({
  selector: 'package-table',
  templateUrl: './event-table.component.html',
  styleUrl: './event-table.component.css'
})
export class EventTableComponent implements OnInit{

  @Input() id!: string | null;
  public event!: Event;

  constructor(private packageService: EventService,
              private notificationService: NotificationService,
              private router: Router) {
  }
  ngOnInit(): void {
    this.packageService.getById(parseInt(this.id as string, 10)).subscribe((data: Event)=>{
      this.event = data;
    });
  }

}
