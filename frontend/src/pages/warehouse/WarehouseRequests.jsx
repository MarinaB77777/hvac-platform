import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function WarehouseRequests() {
  const [requests, setRequests] = useState([])

  useEffect(() => {
    loadRequests()
  }, [])

  const loadRequests = async () => {
    try {
      const res = await API.get("/material_requests")
      setRequests(res.data)
    } catch {
      alert("Ошибка загрузки заявок")
    }
  }

  const handleNextStatus = async (req) => {
    try {
      if (req.status === "placed") {
        await API.post(`/material_requests/${req.id}/approve`)
      } else if (req.status === "approved") {
        await API.post(`/material_requests/${req.id}/issue`)
      }
      loadRequests()
    } catch {
      alert("Не удалось обновить статус")
    }
  }

  const renderButtonText = (status) => {
    if (status === "placed") return "Подтвердить"
    if (status === "approved") return "Выдать"
    if (status === "issued") return "Выдано"
    return "-"
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Заявки на расходные материалы</h1>
      {requests.length === 0 ? (
        <p className="text-gray-500">Нет активных заявок</p>
      ) : (
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">Дата</th>
              <th className="border px-2 py-1">HVAC</th>
              <th className="border px-2 py-1">Категория</th>
              <th className="border px-2 py-1">Марка</th>
              <th className="border px-2 py-1">Кол-во</th>
              <th className="border px-2 py-1">Цена</th>
              <th className="border px-2 py-1">Шильдик</th>
              <th className="border px-2 py-1">Статус</th>
            </tr>
          </thead>
          <tbody>
            {requests.map(req => (
              <tr key={req.id} className="border-t">
                <td className="border px-2 py-1">{req.date}</td>
                <td className="border px-2 py-1">{req.hvac_name}</td>
                <td className="border px-2 py-1">{req.category}</td>
                <td className="border px-2 py-1">{req.brand}</td>
                <td className="border px-2 py-1">{req.quantity}</td>
                <td className="border px-2 py-1">{req.price}</td>
                <td className="border px-2 py-1">
                  {req.photo_url
                    ? <img src={req.photo_url} alt="шильдик" className="h-10" />
                    : <span className="text-red-600">Нет фото</span>}
                </td>
                <td className="border px-2 py-1">
                  <button
                    disabled={req.status === "issued"}
                    onClick={() => handleNextStatus(req)}
                    className={`px-3 py-1 rounded text-white ${
                      req.status === "placed" ? "bg-yellow-500" :
                      req.status === "approved" ? "bg-green-600" :
                      "bg-gray-400 cursor-default"
                    }`}
                  >
                    {renderButtonText(req.status)}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
