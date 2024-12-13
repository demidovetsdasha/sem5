import { Injectable } from '@angular/core';
import {HTTP_INTERCEPTORS, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {catchError, Observable} from "rxjs";
import {TokenStorageService} from "../service/token-storage.service";
import {Router} from "@angular/router";
import {Constants} from "../constants/Constants";

@Injectable({
  providedIn: 'root'
})
export class AuthInterceptorService implements HttpInterceptor{

  constructor(private tokenService: TokenStorageService,
              private router: Router) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    console.log(req)
    let authRequest = req;
    const token = this.tokenService.getToken();
    if (token!==null){
      authRequest = req.clone({headers: req.headers.set(Constants.TOKEN_HEADER_KEY, token)});
    }
    return next.handle(authRequest).pipe(
      catchError((error) => {
        if (error.status === 401) {
          this.router.navigate(['/login']); // Перенаправление на страницу логина
        }
        throw error;
      })
    );
  }
}

export const authInterceptorProvider = [
  {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true}
];
