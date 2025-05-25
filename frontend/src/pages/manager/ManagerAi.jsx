import { useEffect, useState } from "react"
import API from "../../api/axios"

export default function ManagerAi() {
  const [insights, setInsights] = useState([])

  useEffect(() => {
    loadInsights()
  }, [])

  const loadInsights = async () => {
    try {
      const res = await API.get("/ai/insights") // при наличии бэка
      setInsights(res.data)
    } catch {
      // мок-данные
      setInsights([
        {
          title: "Превышение нормы фреона",
          detail: "HVAC Иванов П. часто использует 3 баллона R410 на замену компрессора вместо 2.",
          recommendation: "Провести проверку типовых операций и пересмотреть норму."
        },
        {
          title: "Материалы на исходе",
          detail: "Остаток фильтров LG составляет менее 2 шт. при средней неделе 5–7 шт.",
          recommendation: "Заказать пополнение на склад заранее."
        },
        {
          title: "Слабая оценка по одному мастеру",
          detail: "HVAC Сидоров А. имеет среднюю оценку 2.7 за последние 10 заказов.",
          recommendation: "Рассмотреть дополнительное обучение или контроль качества."
        }
      ])
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">ИИ-анализ: автоматические выводы и рекомендации</h1>

      {insights.length === 0 ? (
        <p className="text-gray-500">Нет данных для анализа</p>
      ) : (
        <div className="space-y-4">
          {insights.map((i, idx) => (
            <div key={idx} className="border rounded p-4 bg-white shadow-sm">
              <h2 className="font-bold text-lg mb-1 text-red-600">{i.title}</h2>
              <p className="mb-2 text-gray-800">{i.detail}</p>
              <p className="text-sm text-green-700"><b>Рекомендация:</b> {i.recommendation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
