import { useEffect, useState } from "react";
import axios from "axios";

export default function OrdersList() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios.get("http://localhost:8000/orders/available", {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setOrders(res.data));
  }, []);

  const takeOrder = async (id) => {
    const token = localStorage.getItem("token");
    await axios.post(`http://localhost:8000/orders/${id}/take`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    setOrders((prev) => prev.filter(o => o.id !== id));
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Доступные заказы</h1>
      {orders.map(order => (
        <div key={order.id} className="border p-4 mb-2">
          <div><b>Адрес:</b> {order.address}</div>
          <div><b>Описание:</b> {order.description}</div>
          <button onClick={() => takeOrder(order.id)} className="mt-2 bg-green-500 text-white px-3 py-1">
            Принять
          </button>
        </div>
      ))}
    </div>
  );
}
