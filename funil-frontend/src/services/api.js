// Configuração da API para comunicação com o backend
const API_BASE_URL = 'http://localhost:5000/api'

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token')
  }

  // Configuração padrão para requisições
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    }
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }
    
    return headers
  }

  // Método genérico para fazer requisições
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: this.getHeaders(),
      ...options,
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || 'Erro na requisição')
      }

      return data
    } catch (error) {
      console.error('Erro na API:', error)
      throw error
    }
  }

  // Autenticação
  async login(email, password) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    
    if (response.access_token) {
      this.token = response.access_token
      localStorage.setItem('token', this.token)
    }
    
    return response
  }

  async logout() {
    this.token = null
    localStorage.removeItem('token')
  }

  async getCurrentUser() {
    return this.request('/auth/me')
  }

  // Credenciais
  async getCredentials() {
    return this.request('/credentials')
  }

  async createCredential(credentialData) {
    return this.request('/credentials', {
      method: 'POST',
      body: JSON.stringify(credentialData),
    })
  }

  async updateCredential(id, credentialData) {
    return this.request(`/credentials/${id}`, {
      method: 'PUT',
      body: JSON.stringify(credentialData),
    })
  }

  async deleteCredential(id) {
    return this.request(`/credentials/${id}`, {
      method: 'DELETE',
    })
  }

  // Funis
  async getFunnels() {
    return this.request('/funnels')
  }

  async createFunnel(funnelData) {
    return this.request('/funnels', {
      method: 'POST',
      body: JSON.stringify(funnelData),
    })
  }

  async updateFunnel(id, funnelData) {
    return this.request(`/funnels/${id}`, {
      method: 'PUT',
      body: JSON.stringify(funnelData),
    })
  }

  async deleteFunnel(id) {
    return this.request(`/funnels/${id}`, {
      method: 'DELETE',
    })
  }

  async cloneFunnel(id) {
    return this.request(`/funnels/${id}/clone`, {
      method: 'POST',
    })
  }

  async toggleFunnelStatus(id) {
    return this.request(`/funnels/${id}/toggle`, {
      method: 'POST',
    })
  }

  // Etapas do funil
  async getFunnelSteps(funnelId) {
    return this.request(`/funnels/${funnelId}/steps`)
  }

  async createFunnelStep(funnelId, stepData) {
    return this.request(`/funnels/${funnelId}/steps`, {
      method: 'POST',
      body: JSON.stringify(stepData),
    })
  }

  async updateFunnelStep(funnelId, stepId, stepData) {
    return this.request(`/funnels/${funnelId}/steps/${stepId}`, {
      method: 'PUT',
      body: JSON.stringify(stepData),
    })
  }

  async deleteFunnelStep(funnelId, stepId) {
    return this.request(`/funnels/${funnelId}/steps/${stepId}`, {
      method: 'DELETE',
    })
  }

  async reorderFunnelSteps(funnelId, stepIds) {
    return this.request(`/funnels/${funnelId}/steps/reorder`, {
      method: 'POST',
      body: JSON.stringify({ step_ids: stepIds }),
    })
  }

  // Checkout
  async getCheckoutConfig(funnelId) {
    return this.request(`/checkout/${funnelId}`)
  }

  async updateCheckoutConfig(funnelId, configData) {
    return this.request(`/checkout/${funnelId}`, {
      method: 'PUT',
      body: JSON.stringify(configData),
    })
  }

  async previewCheckout(funnelId) {
    return this.request(`/checkout/${funnelId}/preview`)
  }

  // Monitoramento
  async getActiveVisitors() {
    return this.request('/monitoring/visitors')
  }

  async getVisitorEvents(visitorId) {
    return this.request(`/monitoring/visitors/${visitorId}/events`)
  }

  async getDashboardStats() {
    return this.request('/monitoring/stats')
  }

  // Tracking
  async getTrackingPixels(funnelId) {
    return this.request(`/tracking/${funnelId}/pixels`)
  }

  async createTrackingPixel(funnelId, pixelData) {
    return this.request(`/tracking/${funnelId}/pixels`, {
      method: 'POST',
      body: JSON.stringify(pixelData),
    })
  }

  async updateTrackingPixel(funnelId, pixelId, pixelData) {
    return this.request(`/tracking/${funnelId}/pixels/${pixelId}`, {
      method: 'PUT',
      body: JSON.stringify(pixelData),
    })
  }

  async deleteTrackingPixel(funnelId, pixelId) {
    return this.request(`/tracking/${funnelId}/pixels/${pixelId}`, {
      method: 'DELETE',
    })
  }

  async toggleTrackingPixel(funnelId, pixelId) {
    return this.request(`/tracking/${funnelId}/pixels/${pixelId}/toggle`, {
      method: 'POST',
    })
  }

  // Pagamentos
  async getPayments(funnelId) {
    return this.request(`/payments/${funnelId}`)
  }

  async getPaymentStats(funnelId) {
    return this.request(`/payments/${funnelId}/stats`)
  }
}

// Instância singleton da API
const apiService = new ApiService()

export default apiService

