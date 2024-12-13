import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Constants} from "../constants/Constants";
import {Event} from "../model/Event";
import {EventResponse} from "../model/EventResponse";

@Injectable({
  providedIn: 'root'
})
export class EventService {

  constructor(private  http: HttpClient) {}

  getAllNew(){
    return this.http.get<EventResponse[]>(Constants.EVENTS_API + "/new")
  }

  getAllPast(){
    return this.http.get<EventResponse[]>(Constants.EVENTS_API+ "/past")
  }

  getById(id: number){
    return this.http.get<EventResponse>(Constants.EVENTS_API+"/"+id);
  }

  add(event:any){
    return this.http.post(Constants.EVENTS_API, {
      name: event.name,
      category: event.category,
      start: event.start,
      finish: event.finish,
      author: event.author
    });
  }

  delete(id: number){
    return this.http.delete(Constants.EVENTS_API+"/"+id)
  }

  updateEvent(id: number, event: any) {
    return this.http.put(Constants.EVENTS_API +"/"+ id, {
      name: event.name,
      category: event.category,
      start: event.start,
      finish: event.finish,
      author: event.author
    });
  }

  addFile(id: number, formData: FormData) {
    return this.http.put(Constants.EVENTS_API +"/file/"+ id, formData)
  }

  getFile(id: number){
    return this.http.get(Constants.EVENTS_API +"/file/get/"+ id, { responseType: 'blob' })
  }
}
