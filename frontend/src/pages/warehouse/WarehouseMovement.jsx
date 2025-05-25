import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function WarehouseMovement() {
  const [history, setHistory] = useState([])

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const res = await API.get("/stock/history")
      setHistory(res.data)
    } catch {
      alert("Ошибка загрузки истории склада")
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Движение склада</h1>
      {history.length === 0 ? (
        <p className="text-gray-500">Нет записей</p>
      ) : (
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">Дата</th>
              <th className="border px-2 py-1">Операция</th>
              <th className="border px-2 py-1">Категория</th>
              <th className="border px-2 py-1">Марка</th>
              <th className="border px-2 py-1">Кол-во</th>
              <th className="border px-2 py-1">Кто</th>
              <th className="border px-2 py-1">Шильдик</th>
            </tr>
          </thead>
          <tbody>
            {history.map(entry => (
              <tr key={entry.id} className="border-t">
                <td className="border px-2 py-1">{entry.date}</td>
                <td className="border px-2 py-1">{entry.action}</td>
                <td className="border px-2 py-1">{entry.category}</td>
                <td className="border px-2 py-1">{entry.brand}</td>
                <td className="border px-2 py-1">{entry.quantity}</td>
                <td className="border px-2 py-1">{entry.actor}</td>
                <td className="border px-2 py-1">
                  {entry.photo_url
                    ? <img src={entry.photo_url} alt="шильдик" className="h-10" />
                    : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
