import { Link, Outlet, useNavigate } from "react-router-dom"

export default function HVACLayout() {
  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className="p-4">
      <nav className="flex gap-4 mb-6 border-b pb-2">
        <Link to="/hvac/orders" className="text-blue-600 hover:underline">Новые заказы</Link>
        <Link to="/hvac/my-orders" className="text-blue-600 hover:underline">Мои заказы</Link>
        <Link to="/hvac/materials" className="text-blue-600 hover:underline">Расходные материалы</Link>
        <button onClick={logout} className="ml-auto text-red-600 hover:underline">Выйти</button>
      </nav>
      <Outlet />
    </div>
  )
}
