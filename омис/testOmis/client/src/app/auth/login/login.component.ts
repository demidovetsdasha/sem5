import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../service/auth.service";
import {TokenStorageService} from "../../service/token-storage.service";
import {NotificationService} from "../../service/notification.service";
import {Router} from "@angular/router";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{

  public loginForm!: FormGroup;

  constructor(
    private authService: AuthService,
    private tokenStorage: TokenStorageService,
    private notificationService: NotificationService,
    private router: Router,
    private fb: FormBuilder
  ) {

  if (this.tokenStorage.getUser()){
    this.router.navigate(['index'])
  }

  }

  createLoginForm(): FormGroup{
    return this.fb.group({
      username: ['', Validators.compose([Validators.required])],
      password: ['', Validators.compose([Validators.required])],

    })
  }

  ngOnInit():  void {
    this.loginForm = this.createLoginForm();
  }

  submit() {
    console.log(this.loginForm.value.username)
    this.authService.login({
      username: this.loginForm.value.username,
      password: this.loginForm.value.password
    }).subscribe(
      (data) => {
        console.log(data);
        let token = (data as { token: string }).token; // Type assertion
        this.tokenStorage.saveToken(token);
        this.tokenStorage.saveUser(data);

        this.notificationService.showSnackBar('Successfully logged in');
        this.router.navigate(['/']);
        window.location.reload();
      },
      (error) => {
        console.log(error);
        this.notificationService.showSnackBar(error.message);
      }
    );
  }

}

