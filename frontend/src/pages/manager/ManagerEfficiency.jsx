import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerEfficiency() {
  const [norms, setNorms] = useState([])
  const [newNorm, setNewNorm] = useState({ job: "", category: "", brand: "", max: 1 })
  const [orders, setOrders] = useState([])

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [normRes, orderRes] = await Promise.all([
        API.get("/material-norms"),
        API.get("/orders/all")
      ])
      setNorms(normRes.data)
      setOrders(orderRes.data.filter(o => o.status === "completed"))
    } catch {
      alert("Ошибка загрузки данных")
    }
  }

  const updateNorm = async (id, field, value) => {
    try {
      await API.patch(`/material-norms/${id}`, { [field]: value })
      loadData()
    } catch {
      alert("Ошибка при обновлении")
    }
  }

  const deleteNorm = async (id) => {
    try {
      await API.delete(`/material-norms/${id}`)
      loadData()
    } catch {
      alert("Ошибка при удалении")
    }
  }

  const addNorm = async () => {
    try {
      await API.post("/material-norms", newNorm)
      setNewNorm({ job: "", category: "", brand: "", max: 1 })
      loadData()
    } catch {
      alert("Ошибка при добавлении")
    }
  }

  const getNorm = (job, category, brand) => {
    const match = norms.find(n =>
      n.job === job &&
      n.category === category &&
      (n.brand === brand || !n.brand)
    )
    return match ? Number(match.max) : null
  }

  const analyzeMaterials = (order) => {
    if (!order.materials_used || !order.job_type) return "—"

    const summary = {}
    order.materials_used.forEach(mat => {
      const key = ${mat.category}::${mat.brand}
      summary[key] = (summary[key] || 0) + 1
    })

    const overused = Object.entries(summary).filter(([key, qty]) => {
      const [category, brand] = key.split("::")
      const norm = getNorm(order.job_type, category, brand)
      return norm !== null && qty > norm
    })

    return overused.length > 0
      ? <span className="text-red-600 font-medium">Превышение</span>
      : <span className="text-green-700">OK</span>
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Нормы расхода материалов</h1>

      <table className="w-full text-sm border mb-6">
        <thead className="bg-gray-100">
          <tr>
            <th className="border px-2 py-1">Тип работы</th>
            <th className="border px-2 py-1">Категория</th>
            <th className="border px-2 py-1">Марка</th>
            <th className="border px-2 py-1">Макс. (шт)</th>
            <th className="border px-2 py-1">Действие</th>
          </tr>
        </thead>
        <tbody>
          {norms.map(n => (
            <tr key={n.id} className="border-t">
              <td className="border px-2 py-1">
                <input defaultValue={n.job} onBlur={(e) => updateNorm(n.id, "job", e.target.value)} className="border px-1 w-full" />
              </td>
              <td className="border px-2 py-1">
                <input defaultValue={n.category} onBlur={(e) => updateNorm(n.id, "category", e.target.value)} className="border px-1 w-full" />
              </td>
              <td className="border px-2 py-1">
                <input defaultValue={n.brand} onBlur={(e) => updateNorm(n.id, "brand", e.target.value)} className="border px-1 w-full" />
              </td>
              <td className="border px-2 py-1">
                <input type="number" defaultValue={n.max} onBlur={(e) => updateNorm(n.id, "max", e.target.value)} className="border px-1 w-16" />
              </td>
              <td className="border px-2 py-1">
                <button onClick={() => deleteNorm(n.id)} className="text-red-600 hover:underline">Удалить</button>
              </td>
            </tr>
          ))}

          <tr className="border-t bg-gray-50">
            <td className="border px-2 py-1">
              <input value={newNorm.job} onChange={(e) => setNewNorm({ ...newNorm, job: e.target.value })} className="border px-1 w-full" />

</td>
            <td className="border px-2 py-1">
              <input value={newNorm.category} onChange={(e) => setNewNorm({ ...newNorm, category: e.target.value })} className="border px-1 w-full" />
            </td>
            <td className="border px-2 py-1">
              <input value={newNorm.brand} onChange={(e) => setNewNorm({ ...newNorm, brand: e.target.value })} className="border px-1 w-full" />
            </td>
            <td className="border px-2 py-1">
              <input type="number" value={newNorm.max} onChange={(e) => setNewNorm({ ...newNorm, max: e.target.value })} className="border px-1 w-16" />
            </td>
            <td className="border px-2 py-1">
              <button onClick={addNorm} className="text-blue-600 hover:underline">Добавить</button>
            </td>
          </tr>
        </tbody>
      </table>

      <h1 className="text-xl mb-4 mt-10">Анализ отклонений по заказам</h1>
      {orders.length === 0 ? (
        <p className="text-gray-500">Нет завершённых заказов</p>
      ) : (
        <table className="w-full text-sm border">
          <thead className="bg-gray-100">
            <tr>
              <th className="border px-2 py-1">Дата</th>
              <th className="border px-2 py-1">HVAC</th>
              <th className="border px-2 py-1">Тип работы</th>
              <th className="border px-2 py-1">Материалы</th>
              <th className="border px-2 py-1">Результат</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order.id} className="border-t">
                <td className="border px-2 py-1">{order.date}</td>
                <td className="border px-2 py-1">{order.hvac_name}</td>
                <td className="border px-2 py-1">{order.job_type || "—"}</td>
                <td className="border px-2 py-1">
                  {order.materials_used?.map(m => m.category + " " + m.brand).join(", ") || "—"}
                </td>
                <td className="border px-2 py-1">{analyzeMaterials(order)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

