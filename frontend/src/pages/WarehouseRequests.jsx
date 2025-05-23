import { useEffect, useState } from "react";
import axios from "axios";

export default function WarehouseRequests() {
  const [requests, setRequests] = useState([]);

  const loadRequests = async () => {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://localhost:8000/material-requests/", {
      headers: { Authorization: `Bearer ${token}` }
    });
    setRequests(res.data);
  };

  useEffect(() => {
    loadRequests();
  }, []);

  const actOnRequest = async (id, action) => {
    const token = localStorage.getItem("token");
    await axios.post(`http://localhost:8000/material-requests/${id}/${action}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    loadRequests();
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Заявки на материалы</h1>
      {requests.map(req => (
        <div key={req.id} className="border p-4 mb-2">
          <div><b>Материал:</b> {req.name} ({req.brand})</div>
          <div><b>Заказ:</b> {req.order_id} | <b>HVAC:</b> {req.hvac_id}</div>
          <div><b>Кол-во:</b> {req.qty} | <b>Статус:</b> {req.status}</div>
          {req.status === "pending" && (
            <button onClick={() => actOnRequest(req.id, "confirm")} className="bg-yellow-500 text-white px-3 py-1 mt-2">
              Подтвердить
            </button>
          )}
          {req.status === "confirmed" && (
            <button onClick={() => actOnRequest(req.id, "issue")} className="bg-green-600 text-white px-3 py-1 mt-2">
              Выдать
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
