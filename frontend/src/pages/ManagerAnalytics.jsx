import { useEffect, useState } from "react";
import axios from "axios";

export default function ManagerAnalytics() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios.get("http://localhost:8000/analytics/hvac", {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => setData(res.data));
  }, []);

  const getInsights = (row) => {
    const insights = [];
    if (row.flags.includes("много отказов")) insights.push("Внимание: высокий процент отказов.");
    if (row.flags.includes("высокие расходы")) insights.push("Проверьте расход материалов.");
    if (insights.length === 0) insights.push("Всё стабильно.");
    return insights.join(" ");
  };

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Аналитика по сотрудникам</h1>
      {data.map(row => (
        <div key={row.hvac_id} className="border p-4 mb-2 text-sm">
          <div><b>ID:</b> {row.hvac_id}</div>
          <div><b>Заказов:</b> {row.orders_total} | <b>Отказов:</b> {row.declined}</div>
          <div><b>Сред. длит.:</b> {row.avg_duration_minutes} мин | <b>Материалы:</b> ${row.materials_cost}</div>
          <div className="text-purple-700 mt-1 italic">{getInsights(row)}</div>
        </div>
      ))}
    </div>
  );
}
