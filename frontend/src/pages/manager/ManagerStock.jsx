import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerStock() {
  const [items, setItems] = useState([])

  useEffect(() => {
    loadItems()
  }, [])

  const loadItems = async () => {
    try {
      const res = await API.get("/stock/items")
      setItems(res.data)
    } catch {
      alert("Ошибка загрузки остатков")
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Наличие материалов на складе</h1>
      {items.length === 0 ? (
        <p className="text-gray-500">Склад пуст или данные не загружены</p>
      ) : (
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">Наименование</th>
              <th className="border px-2 py-1">Марка</th>
              <th className="border px-2 py-1">Дата поступления</th>
              <th className="border px-2 py-1">Поступило</th>
              <th className="border px-2 py-1">Выдано</th>
              <th className="border px-2 py-1">Остаток</th>
              <th className="border px-2 py-1">Статус</th>
            </tr>
          </thead>
          <tbody>
            {items.map(item => (
              <tr key={item.id} className="border-t">
                <td className="border px-2 py-1">{item.name}</td>
                <td className="border px-2 py-1">{item.brand}</td>
                <td className="border px-2 py-1">{item.date_received}</td>
                <td className="border px-2 py-1">{item.received}</td>
                <td className="border px-2 py-1">{item.issued}</td>
                <td className="border px-2 py-1">{item.remaining}</td>
                <td className="border px-2 py-1">
                  {item.remaining === 0 ? (
                    <span className="text-red-600">Нет на складе</span>
                  ) : (
                    <span className="text-green-700">В наличии</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
