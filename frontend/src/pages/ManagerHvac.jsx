import { useEffect, useState } from "react";
import axios from "axios";

export default function ManagerHvac() {
  const [rows, setRows] = useState([]);

  const load = async () => {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://localhost:8000/hvac-users/", {
      headers: { Authorization: `Bearer ${token}` }
    });
    setRows(res.data);
  };

  const update = async (id, field, value) => {
    const token = localStorage.getItem("token");
    await axios.patch(`http://localhost:8000/hvac-users/${id}`, { [field]: value }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Сотрудники HVAC / Тарифы</h1>
      {rows.map(user => (
        <div key={user.id} className="border p-4 mb-2 text-sm">
          <div><b>{user.name}</b> ({user.profile})</div>
          <div>Диагностика: ${user.diagnostic_fee} | Работа: ${user.work_fee} | Транспорт: ${user.transport_fee}</div>
          <div className="flex gap-2 mt-2">
            <input type="number" defaultValue={user.diagnostic_fee} onBlur={(e) => update(user.id, "diagnostic_fee", e.target.value)} className="border p-1 w-20" />
            <input type="number" defaultValue={user.work_fee} onBlur={(e) => update(user.id, "work_fee", e.target.value)} className="border p-1 w-20" />
            <input type="number" defaultValue={user.transport_fee} onBlur={(e) => update(user.id, "transport_fee", e.target.value)} className="border p-1 w-20" />
          </div>
        </div>
      ))}
    </div>
  );
}
