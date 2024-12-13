import { Component } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {EventService} from "../../service/event.service";
import {NotificationService} from "../../service/notification.service";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import { jsPDF } from 'jspdf';
import {EventResponse} from "../../model/EventResponse";
import {AuthService} from "../../service/auth.service";
import {AccessRespose} from "../../model/AccessRespose";

@Component({
  selector: 'app-package',
  templateUrl: './event.component.html',
  styleUrl: './event.component.css'
})
export class EventComponent {
  selectedFile: File | null = null;
  id!: string | null;
  intId!: number;
  fileExist: boolean = false
  private event!: EventResponse;

  constructor(private route: ActivatedRoute,
              private eventService: EventService,
              private authService : AuthService,
              private notificationService: NotificationService,
              private fb: FormBuilder,
              public router: Router) {
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id');
    this.intId = parseInt(this.id as string, 10);

    this.eventService.getFile(this.intId).subscribe((file: Blob)=> {
      if(file != null)
      {
        this.fileExist = true
      }
    }, error=> {
      this.fileExist = false
    })
  }

  delete(id: number) {

    this.eventService.delete(id).subscribe((data) => {
      console.log(data);
      this.notificationService.showSnackBar("Successfully deleted");
      this.router.navigate(["index"])
    });
  }

  editEvent(intId: number) {
    this.router.navigate(['/edit', intId]);
  }

  getFile(id: number) {
    this.eventService.getById(id).subscribe((data: EventResponse)=> {
      this.event = data
    });

    this.eventService.getFile(id).subscribe((file: Blob) => {
      //const blob = new Blob([file], { type: 'image/jpeg' });
      //const link = document.createElement('a');
      //link.href = URL.createObjectURL(blob);
      //link.download = 'file.jpeg';  // Имя файла при скачивании
      //link.click();
      // Создаем FileReader для чтения Blob как base64
      const reader = new FileReader();

      reader.onload = (e: any) => {
        const imgData = e.target.result;  // Содержимое файла в формате base64

        // Создаем объект Image
        const img = new Image();

        // Когда изображение загружено, получаем его размеры
        img.onload = () => {
          const imgWidth = img.width;  // Ширина изображения
          const imgHeight = img.height; // Высота изображения

          // Создаем новый PDF документ
          const doc = new jsPDF();

          // Вставляем изображение в PDF с полученными размерами
          const maxWidth = 180;  // Максимальная ширина на странице PDF
          const maxHeight = 160; // Максимальная высота на странице PDF

          const aspectRatio = imgWidth / imgHeight;
          let width = maxWidth;
          let height = width / aspectRatio;

          if (height > maxHeight) {
            height = maxHeight;
            width = height * aspectRatio;
          }

          doc.setFontSize(16);

          // Рассчитываем координаты для центрирования текста
          const pageWidth = doc.internal.pageSize.width;
          const pageHeight = doc.internal.pageSize.height;
          const text = 'Event Analytics File';

          const textWidth = doc.getTextWidth(text);  // Получаем ширину текста
          const x = (pageWidth - textWidth) / 2;    // Рассчитываем X координату для центрирования
          const y = 10         // Можно задать фиксированную Y координату для вертикального центрирования

          // Вставляем текст по центру
          doc.text(text, x, y);

          doc.setFontSize(14);

          doc.text('EVENT NAME: ' + this.event.name, doc.internal.pageSize.width/16, y+15);
          doc.text('CATEGORY: ' + this.event.category, doc.internal.pageSize.width/16, y+30);
          doc.text('START TIME: ' + this.event.start, doc.internal.pageSize.width/16, y+45);
          doc.text('END TIME: ' + this.event.finish, doc.internal.pageSize.width/16, y+60);
          doc.text('AUTHOR: ' + this.event.author, doc.internal.pageSize.width/16, y+75);


          doc.setFontSize(12);
          doc.text('FILES:', doc.internal.pageSize.width/16, height + 35);

          // Добавляем изображение в PDF
          doc.addImage(imgData, 'JPEG', doc.internal.pageSize.width/16, doc.internal.pageSize.height/2, width, height);



          // Скачиваем PDF
          doc.save(this.event.name + ' analytics.pdf');
        };

        // Устанавливаем источник изображения (base64 строка)
        img.src = imgData;
      };

      // Читаем файл как DataURL для использования в изображении
      reader.readAsDataURL(file);
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input?.files?.length) {
      this.selectedFile = input.files[0];
      this.onSubmit()
    }
  }

  triggerFileInput(fileInput: HTMLInputElement): void {
    fileInput.click(); // Открывает окно выбора файла
  }

  onSubmit(): void {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('file', this.selectedFile);
    this.eventService.addFile(this.intId, formData).subscribe((data) => {
      this.notificationService.showSnackBar("FileAdded");
      this.fileExist = true
    });
  }
}
