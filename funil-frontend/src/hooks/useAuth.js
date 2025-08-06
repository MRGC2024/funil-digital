import { useState, useEffect, createContext, useContext } from 'react'
import apiService from '../services/api.js'

// Contexto de autenticação
const AuthContext = createContext()

// Provider de autenticação
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Verificar se o usuário está autenticado ao carregar a aplicação
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      
      if (token) {
        try {
          const userData = await apiService.getCurrentUser()
          setUser(userData)
          setIsAuthenticated(true)
        } catch (error) {
          console.error('Erro ao verificar autenticação:', error)
          localStorage.removeItem('token')
          setIsAuthenticated(false)
        }
      }
      
      setLoading(false)
    }

    checkAuth()
  }, [])

  // Função de login
  const login = async (email, password) => {
    try {
      const response = await apiService.login(email, password)
      
      if (response.access_token) {
        const userData = await apiService.getCurrentUser()
        setUser(userData)
        setIsAuthenticated(true)
        return { success: true }
      }
    } catch (error) {
      console.error('Erro no login:', error)
      return { success: false, error: error.message }
    }
  }

  // Função de logout
  const logout = async () => {
    try {
      await apiService.logout()
      setUser(null)
      setIsAuthenticated(false)
    } catch (error) {
      console.error('Erro no logout:', error)
    }
  }

  const value = {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

// Hook para usar o contexto de autenticação
export function useAuth() {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  
  return context
}

export default useAuth

