export function getUserRole() {
  try {
    const token = localStorage.getItem("token")
    if (!token) return null
    const payload = JSON.parse(atob(token.split(".")[1]))
    return payload.role
  } catch (e) {
    return null
  }
}

export function isAuthenticated() {
  return !!localStorage.getItem("token")
}
