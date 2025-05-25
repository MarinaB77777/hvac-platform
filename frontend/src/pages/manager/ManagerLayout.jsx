import { Link, Outlet, useNavigate } from "react-router-dom"

export default function ManagerLayout() {
  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className="p-4">
      <nav className="flex gap-4 mb-6 border-b pb-2">
        <Link to="/manager/hvac" className="text-blue-600 hover:underline">Работники HVAC</Link>
        <Link to="/manager/orders" className="text-blue-600 hover:underline">Все заказы</Link>
        <Link to="/manager/efficiency" className="text-blue-600 hover:underline">Анализ эффективности</Link>
        <Link to="/manager/materials-check" className="text-blue-600 hover:underline">Контроль расходников</Link>
        <Link to="/manager/ai" className="text-blue-600 hover:underline">ИИ-анализ</Link>
        <button onClick={logout} className="ml-auto text-red-600 hover:underline">Выйти</button>
      </nav>
      <Outlet />
    </div>
  )
}
