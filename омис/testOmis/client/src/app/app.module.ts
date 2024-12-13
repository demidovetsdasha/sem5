import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MaterialModule} from "./material-module";
import {HttpClientModule} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatTooltipModule} from "@angular/material/tooltip";
import { IndexComponent } from './component/index/index.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import {authErrorInterceptorProvider} from "./helper/error-interceptor.service";
import {authInterceptorProvider} from "./helper/auth-interceptor.service";
import { TableComponent } from './component/index/table/table.component';
import { AddComponent } from './component/add/add.component';
import { EventComponent } from './component/package/event.component';
import { EventTableComponent } from './component/package/package-table/event-table.component';
import {PastIndexComponent} from "./component/pastIndex/pastIndex.component";
import {PastTableComponent} from "./component/pastIndex/pastTable/pastTable.component";
import {EditComponent} from "./component/edit/edit.component";

@NgModule({
  declarations: [
    AppComponent,
    IndexComponent,
    PastIndexComponent,
    LoginComponent,
    RegisterComponent,
    TableComponent,
    PastTableComponent,
    AddComponent,
    EditComponent,
    EventComponent,
    EventTableComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatTooltipModule
  ],
  providers: [
    authInterceptorProvider,
    authErrorInterceptorProvider,
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
