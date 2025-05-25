import { Link, Outlet, useNavigate } from "react-router-dom"

export default function ClientLayout() {
  const navigate = useNavigate()

  const logout = () => {
    localStorage.removeItem("token")
    navigate("/login")
  }

  return (
    <div className="p-4">
      <nav className="flex gap-4 mb-6 border-b pb-2">
        <Link to="/client/new" className="text-blue-600 hover:underline">Создать заказ</Link>
        <Link to="/client/orders" className="text-blue-600 hover:underline">Мои заказы</Link>
        <Link to="/client/profile" className="text-blue-600 hover:underline">Профиль</Link>
        <button onClick={logout} className="ml-auto text-red-600 hover:underline">Выйти</button>
      </nav>
      <Outlet />
    </div>
  )
}
