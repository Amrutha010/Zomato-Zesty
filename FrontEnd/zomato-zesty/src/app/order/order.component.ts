import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-order',
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.css']
})
export class OrderComponent implements OnInit {
  orders: any[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getOrders();
  }

  getOrders(): void {
    this.http.get<any[]>('/orders').subscribe(data => {
      this.orders = data;
    });
  }
}
