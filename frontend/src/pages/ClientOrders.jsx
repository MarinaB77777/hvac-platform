import { useEffect, useState } from "react";
import axios from "axios";

export default function ClientOrders() {
  const [orders, setOrders] = useState([]);
  const [tab, setTab] = useState("new");

  const loadOrders = async () => {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://localhost:8000/orders/me", {
      headers: { Authorization: `Bearer ${token}` }
    });
    setOrders(res.data);
  };

  useEffect(() => {
    loadOrders();
  }, []);

  const filtered = orders.filter(o =>
    tab === "new" ? ["new", "accepted"].includes(o.status) : ["completed", "declined"].includes(o.status)
  );

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Мои заказы</h1>
      <div className="mb-4">
        <button onClick={() => setTab("new")} className={`px-4 py-2 mr-2 ${tab === "new" ? "bg-blue-500 text-white" : "bg-gray-200"}`}>
          Новые
        </button>
        <button onClick={() => setTab("all")} className={`px-4 py-2 ${tab === "all" ? "bg-blue-500 text-white" : "bg-gray-200"}`}>
          Все
        </button>
      </div>
      {filtered.map(order => (
        <div key={order.id} className="border p-4 mb-2">
          <div><b>Адрес:</b> {order.address}</div>
          <div><b>Статус:</b> {order.status}</div>
          <div><b>Сумма:</b> {order.price_total ?? "–"}</div>
          {order.result_file_url && (
            <div className="mt-1 text-sm">
              <a href={order.result_file_url} target="_blank" rel="noopener noreferrer" className="text-green-700 underline">
                Фото результата
              </a>
            </div>
          )}
          {order.rating && (
            <div className="text-yellow-600 text-sm mt-1">Оценка: {order.rating} / 5</div>
          )}
        </div>
      ))}
    </div>
  );
}
