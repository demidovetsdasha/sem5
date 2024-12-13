import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Constants} from "../constants/Constants";
import {AccessRespose} from "../model/AccessRespose";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  public login(user: any){
    return this.http.post(Constants.AUTH_API+'signin',{
      username: user.username,
      password: user.password
    });
  }

  public register(user: any){
    return this.http.post(Constants.AUTH_API + 'signup', {
      email: user.email,
      username: user.username,
      firstname: user.firstname,
      lastname: user.lastname,
      password: user.password,
      confirmPassword: user.confirmPassword
    })
  }
}
