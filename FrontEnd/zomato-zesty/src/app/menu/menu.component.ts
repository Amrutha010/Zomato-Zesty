import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
  menuItems: any[] = []; // Initialize menuItems as an empty array

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getMenuItems();
  }

  getMenuItems(): void {
    this.http.get<any[]>('/menu').subscribe(data => {
      this.menuItems = data;
    });
  }
}
