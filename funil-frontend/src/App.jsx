import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  BarChart3, 
  Users, 
  Settings, 
  CreditCard, 
  Eye, 
  Target, 
  TrendingUp,
  LogIn,
  LogOut,
  Plus,
  Edit,
  Trash2,
  Play,
  Pause,
  Copy,
  Monitor,
  Smartphone,
  Globe,
  Loader2
} from 'lucide-react'
import { AuthProvider, useAuth } from './hooks/useAuth.js'
import apiService from './services/api.js'
import './App.css'

// Componente de Login
function LoginPage() {
  const [credentials, setCredentials] = useState({ email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await login(credentials.email, credentials.password)
    
    if (!result.success) {
      setError(result.error || 'Erro ao fazer login')
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold text-gray-900">Funil Digital</CardTitle>
          <CardDescription>Dashboard Administrativo</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
                {error}
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="admin@funil.com"
                value={credentials.email}
                onChange={(e) => setCredentials({...credentials, email: e.target.value})}
                required
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={credentials.password}
                onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                required
                disabled={loading}
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Entrando...
                </>
              ) : (
                <>
                  <LogIn className="w-4 h-4 mr-2" />
                  Entrar
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

// Componente de Sidebar
function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'funnels', label: 'Funis', icon: Target },
    { id: 'credentials', label: 'Credenciais', icon: Settings },
    { id: 'checkout', label: 'Checkout', icon: CreditCard },
    { id: 'monitoring', label: 'Monitoramento', icon: Eye },
    { id: 'tracking', label: 'Tracking', icon: TrendingUp },
  ]

  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900">Funil Digital</h1>
        <p className="text-sm text-gray-500">Dashboard Admin</p>
      </div>
      
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            return (
              <li key={item.id}>
                <button
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center px-3 py-2 rounded-lg text-left transition-colors ${
                    activeTab === item.id
                      ? 'bg-blue-50 text-blue-700 border border-blue-200'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.label}
                </button>
              </li>
            )
          })}
        </ul>
      </nav>
    </div>
  )
}

// Componente de Header
function Header() {
  const { logout, user } = useAuth()

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">Painel de Controle</h2>
          <p className="text-sm text-gray-500">Gerencie seus funis digitais</p>
        </div>
        <div className="flex items-center space-x-4">
          {user && (
            <span className="text-sm text-gray-600">
              Olá, {user.name || user.email}
            </span>
          )}
          <Button variant="outline" onClick={logout}>
            <LogOut className="w-4 h-4 mr-2" />
            Sair
          </Button>
        </div>
      </div>
    </header>
  )
}

// Componente Dashboard
function Dashboard() {
  const [stats, setStats] = useState({
    visitors: 0,
    conversions: 0,
    conversionRate: 0,
    revenue: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiService.getDashboardStats()
        setStats(data)
      } catch (error) {
        console.error('Erro ao carregar estatísticas:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  const statsCards = [
    { title: 'Visitantes Hoje', value: stats.visitors || '1,234', change: '+12%', icon: Users },
    { title: 'Conversões', value: stats.conversions || '89', change: '+8%', icon: Target },
    { title: 'Taxa de Conversão', value: `${stats.conversionRate || 7.2}%`, change: '+0.5%', icon: TrendingUp },
    { title: 'Receita', value: `R$ ${stats.revenue || '12,450'}`, change: '+15%', icon: CreditCard },
  ]

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h3>
        <p className="text-gray-600">Visão geral dos seus funis digitais</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                    <p className="text-sm text-green-600">{stat.change}</p>
                  </div>
                  <Icon className="w-8 h-8 text-blue-600" />
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Visitantes em Tempo Real</CardTitle>
            <CardDescription>Usuários navegando no funil agora</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  <div>
                    <p className="font-medium">Página de Captura</p>
                    <p className="text-sm text-gray-600">IP: 192.168.1.100</p>
                  </div>
                </div>
                <Badge variant="secondary">2min</Badge>
              </div>
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                  <div>
                    <p className="font-medium">VSL</p>
                    <p className="text-sm text-gray-600">IP: 192.168.1.101</p>
                  </div>
                </div>
                <Badge variant="secondary">5min</Badge>
              </div>
              <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-orange-500 rounded-full animate-pulse"></div>
                  <div>
                    <p className="font-medium">Checkout</p>
                    <p className="text-sm text-gray-600">IP: 192.168.1.102</p>
                  </div>
                </div>
                <Badge variant="secondary">1min</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Funis Ativos</CardTitle>
            <CardDescription>Status dos seus funis</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div>
                  <p className="font-medium">Funil Empréstimo</p>
                  <p className="text-sm text-gray-600">Última atualização: há 2 horas</p>
                </div>
                <Badge className="bg-green-100 text-green-800">Ativo</Badge>
              </div>
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div>
                  <p className="font-medium">Funil Cartão</p>
                  <p className="text-sm text-gray-600">Última atualização: há 1 dia</p>
                </div>
                <Badge variant="secondary">Pausado</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

// Componente de Gerenciamento de Funis
function FunnelsManagement() {
  const [funnels, setFunnels] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFunnels = async () => {
      try {
        const data = await apiService.getFunnels()
        setFunnels(data)
      } catch (error) {
        console.error('Erro ao carregar funis:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchFunnels()
  }, [])

  const handleToggleStatus = async (funnelId) => {
    try {
      await apiService.toggleFunnelStatus(funnelId)
      // Recarregar funis
      const data = await apiService.getFunnels()
      setFunnels(data)
    } catch (error) {
      console.error('Erro ao alterar status do funil:', error)
    }
  }

  const handleCloneFunnel = async (funnelId) => {
    try {
      await apiService.cloneFunnel(funnelId)
      // Recarregar funis
      const data = await apiService.getFunnels()
      setFunnels(data)
    } catch (error) {
      console.error('Erro ao clonar funil:', error)
    }
  }

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Gerenciar Funis</h3>
          <p className="text-gray-600">Configure e monitore seus funis digitais</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Novo Funil
        </Button>
      </div>

      <div className="grid gap-6">
        {funnels.length === 0 ? (
          <Card>
            <CardContent className="p-6 text-center">
              <p className="text-gray-500">Nenhum funil encontrado. Crie seu primeiro funil!</p>
            </CardContent>
          </Card>
        ) : (
          funnels.map((funnel) => (
            <Card key={funnel.id}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-4">
                    <h4 className="text-lg font-semibold">{funnel.name}</h4>
                    <Badge className={funnel.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}>
                      {funnel.is_active ? 'Ativo' : 'Pausado'}
                    </Badge>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Button variant="outline" size="sm">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => handleCloneFunnel(funnel.id)}>
                      <Copy className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => handleToggleStatus(funnel.id)}>
                      {funnel.is_active ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    </Button>
                    <Button variant="outline" size="sm">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div className="text-center p-3 bg-blue-50 rounded-lg">
                    <p className="text-2xl font-bold text-blue-600">{funnel.total_visitors || 0}</p>
                    <p className="text-sm text-gray-600">Visitantes</p>
                  </div>
                  <div className="text-center p-3 bg-green-50 rounded-lg">
                    <p className="text-2xl font-bold text-green-600">{funnel.total_conversions || 0}</p>
                    <p className="text-sm text-gray-600">Conversões</p>
                  </div>
                  <div className="text-center p-3 bg-purple-50 rounded-lg">
                    <p className="text-2xl font-bold text-purple-600">
                      {funnel.total_visitors > 0 ? ((funnel.total_conversions / funnel.total_visitors) * 100).toFixed(1) : 0}%
                    </p>
                    <p className="text-sm text-gray-600">Taxa de Conversão</p>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Descrição:</p>
                  <p className="text-sm text-gray-600">{funnel.description || 'Sem descrição'}</p>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}

// Componente de Credenciais
function CredentialsManagement() {
  const [credentials, setCredentials] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchCredentials = async () => {
      try {
        const data = await apiService.getCredentials()
        setCredentials(data)
      } catch (error) {
        console.error('Erro ao carregar credenciais:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchCredentials()
  }, [])

  if (loading) {
    return (
      <div className="p-6 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Gerenciar Credenciais</h3>
          <p className="text-gray-600">Configure as credenciais de integração</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Nova Credencial
        </Button>
      </div>

      <div className="grid gap-4">
        {credentials.length === 0 ? (
          <Card>
            <CardContent className="p-6 text-center">
              <p className="text-gray-500">Nenhuma credencial encontrada. Adicione suas primeiras credenciais!</p>
            </CardContent>
          </Card>
        ) : (
          credentials.map((cred) => (
            <Card key={cred.id}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div>
                      <h4 className="font-semibold">{cred.name}</h4>
                      <p className="text-sm text-gray-600">
                        Tipo: {cred.credential_type} • Última atualização: {new Date(cred.updated_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge className={cred.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}>
                      {cred.is_active ? 'Ativa' : 'Inativa'}
                    </Badge>
                    <Button variant="outline" size="sm">
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}

// Componente Principal da Aplicação
function AppContent() {
  const { isAuthenticated, loading } = useAuth()
  const [activeTab, setActiveTab] = useState('dashboard')

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <LoginPage />
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />
      case 'funnels':
        return <FunnelsManagement />
      case 'credentials':
        return <CredentialsManagement />
      case 'checkout':
        return (
          <div className="p-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Configurar Checkout</h3>
            <p className="text-gray-600">Personalize suas páginas de checkout</p>
            <Card className="mt-6">
              <CardContent className="p-6">
                <p className="text-center text-gray-500">Funcionalidade em desenvolvimento...</p>
              </CardContent>
            </Card>
          </div>
        )
      case 'monitoring':
        return (
          <div className="p-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Monitoramento</h3>
            <p className="text-gray-600">Acompanhe visitantes em tempo real</p>
            <Card className="mt-6">
              <CardContent className="p-6">
                <p className="text-center text-gray-500">Funcionalidade em desenvolvimento...</p>
              </CardContent>
            </Card>
          </div>
        )
      case 'tracking':
        return (
          <div className="p-6">
            <h3 className="text-2xl font-bold text-gray-900 mb-2">Pixels de Tracking</h3>
            <p className="text-gray-600">Configure pixels do Facebook, Google e TikTok</p>
            <Card className="mt-6">
              <CardContent className="p-6">
                <p className="text-center text-gray-500">Funcionalidade em desenvolvimento...</p>
              </CardContent>
            </Card>
          </div>
        )
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App

