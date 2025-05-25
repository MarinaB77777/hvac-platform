> Муж:
import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerAnalytics() {
  const [summary, setSummary] = useState([])

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [hvacRes, ordersRes, insightRes] = await Promise.all([
        API.get("/hvac-users"),
        API.get("/orders/all"),
        API.get("/analytics/hvac")
      ])

      const hvacList = hvacRes.data
      const orders = ordersRes.data
      const insightMap = Object.fromEntries(insightRes.data.map(i => [i.hvac_id, i]))

      const result = hvacList.map(user => {
        const userOrders = orders.filter(o => o.hvac_id === user.id)
        const completed = userOrders.filter(o => o.status === "completed")

        const ratingSum = completed.reduce((sum, o) => sum + (o.rating || 0), 0)
        const diagnosticSum = completed.reduce((sum, o) => sum + (o.diagnostic_fee || 0), 0)
        const repairSum = completed.reduce((sum, o) => sum + (o.repair_fee || 0), 0)
        const normViolations = completed.filter(o => o.materials_violation === true).length

        const insight = insightMap[user.id]

        return {
          name: user.name,
          id: user.id,
          total: userOrders.length,
          completed: completed.length,
          avgRating: completed.length ? (ratingSum / completed.length).toFixed(2) : "-",
          diagnosticTotal: diagnosticSum,
          repairTotal: repairSum,
          normViolations,
          declined: insight?.declined || 0,
          avgDuration: insight?.avg_duration_minutes || "-",
          materialsCost: insight?.materials_cost || "-",
          flags: insight?.flags || []
        }
      })

      setSummary(result)
    } catch {
      alert("Ошибка загрузки аналитики")
    }
  }

  const getInsights = (row) => {
    const insights = []
    if (row.flags.includes("много отказов")) insights.push("Внимание: высокий процент отказов.")
    if (row.flags.includes("высокие расходы")) insights.push("Проверьте расход материалов.")
    if (insights.length === 0) insights.push("Всё стабильно.")
    return insights.join(" ")
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Анализ эффективности работников HVAC</h1>

      {summary.length === 0 ? (
        <p className="text-gray-500">Нет данных</p>
      ) : (
        <>
          <table className="w-full text-sm border mb-8">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-2 py-1">Имя</th>
                <th className="border px-2 py-1">Заказов</th>
                <th className="border px-2 py-1">Выполнено</th>
                <th className="border px-2 py-1">Оценка</th>
                <th className="border px-2 py-1">Диагностика</th>
                <th className="border px-2 py-1">Ремонт</th>
                <th className="border px-2 py-1">Отказы</th>
                <th className="border px-2 py-1">Время (мин)</th>
                <th className="border px-2 py-1">Материалы ($)</th>
                <th className="border px-2 py-1">Превышения норм</th>
              </tr>
            </thead>
            <tbody>
              {summary.map(r => (
                <tr key={r.id} className="border-t">
                  <td className="border px-2 py-1">{r.name}</td>
                  <td className="border px-2 py-1">{r.total}</td>
                  <td className="border px-2 py-1">{r.completed}</td>
                  <td className="border px-2 py-1 text-center">
                    {r.avgRating < 3
                      ? <span className="text-red-600 font-semibold">{r.avgRating}</span>
                      : r.avgRating}
                  </td>
                  <td className="border px-2 py-1">${r.diagnosticTotal}</td>
                  <td className="border px-2 py-1">${r.repairTotal}</td>
                  <td className="border px-2 py-1 text-center">{r.declined}</td>
                  <td className="border px-2 py-1 text-center">{r.avgDuration}</td>

> Муж:
<td className="border px-2 py-1 text-center">${r.materialsCost}</td>
                  <td className="border px-2 py-1 text-center">
                    {r.normViolations > 0
                      ? <span className="text-red-600 font-semibold">{r.normViolations}</span>
                      : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <h2 className="text-lg font-medium mb-2">Выводы и рекомендации</h2>
          <div className="space-y-3">
            {summary.map(row => (
              <div key={row.id} className="border rounded p-3 text-sm bg-gray-50">
                <div className="font-medium">{row.name}</div>
                <div className="text-gray-700 italic">{getInsights(row)}</div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
