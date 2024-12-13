import {Component, OnInit} from '@angular/core';
import {Event} from "../../../model/Event";
import {EventResponse} from "../../../model/EventResponse";
import {EventService} from "../../../service/event.service";
import {Router} from "@angular/router";
import {NotificationService} from "../../../service/notification.service";



@Component({
  selector: 'all-packages-past-table',
  templateUrl: './table.component.html',
  styleUrl: './table.component.css'
})
export class PastTableComponent implements OnInit{

  events!: EventResponse[];

  constructor(
    private packageService: EventService,
    private router: Router,
    private notificationService:NotificationService
  ) {
  }


  ngOnInit(): void {
    this.packageService.getAllPast().subscribe(data => {
        this.events = data
      }, error => {
        this.notificationService.showSnackBar("Something went wrong, try again!")
      }
    )
  }

  navigateToDetails(packageId: number) {
    this.router.navigate(['/details', packageId]);
  }

  delete(id: number){
    this.packageService.delete(id).subscribe((data) => {
      console.log(data);
      this.notificationService.showSnackBar("Successfully deleted");
      window.location.reload();
    });
  }


}
