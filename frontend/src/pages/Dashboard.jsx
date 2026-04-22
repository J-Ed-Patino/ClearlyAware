import React from 'react'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow p-10 text-center">
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="mt-2 text-gray-500">Welcome, {user?.email}</p>
        <button
          onClick={logout}
          className="mt-6 bg-red-500 text-white rounded-lg px-4 py-2 text-sm hover:bg-red-600"
        >
          Sign out
        </button>
      </div>
    </div>
  )
}
