/**
 * API Service for FloodAura Frontend
 * Handles all API calls to the FastAPI backend
 */

// Use environment variable or default to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
const API_ROOT = process.env.REACT_APP_API_URL?.replace('/api', '') || 'http://localhost:8000';

class ApiService {
  /**
   * Generic fetch wrapper with error handling
   */
  async fetchWithErrorHandling(url, options = {}) {
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  }

  // ==================== Flood Events ====================

  /**
   * Get all flood events
   */
  async getFloodEvents(skip = 0, limit = 100, severity = null) {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });
    
    if (severity) {
      params.append('severity', severity);
    }

    return this.fetchWithErrorHandling(`${API_BASE_URL}/floods/?${params}`);
  }

  /**
   * Get a specific flood event by ID
   */
  async getFloodEvent(id) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/floods/${id}`);
  }

  /**
   * Create a new flood event
   */
  async createFloodEvent(data) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/floods/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Calculate flood risk without saving
   */
  async calculateFloodRisk(latitude, longitude, locationName) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/floods/calculate-risk`, {
      method: 'POST',
      body: JSON.stringify({
        latitude,
        longitude,
        location_name: locationName,
      }),
    });
  }

  /**
   * Get nearby flood events
   */
  async getNearbyFloodEvents(latitude, longitude, radiusKm = 5) {
    const params = new URLSearchParams({
      latitude: latitude.toString(),
      longitude: longitude.toString(),
      radius_km: radiusKm.toString(),
    });

    return this.fetchWithErrorHandling(`${API_BASE_URL}/floods/nearby/?${params}`);
  }

  // ==================== Map Features ====================

  /**
   * Get last update timestamp
   */
  async getLastUpdate() {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/map/last-update`);
  }

  /**
   * Search for a location
   */
  async searchLocation(query) {
    const params = new URLSearchParams({ location: query });
    return this.fetchWithErrorHandling(`${API_BASE_URL}/map/search?${params}`);
  }

  /**
   * Send user's current location
   */
  async sendUserLocation(latitude, longitude) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/map/locate`, {
      method: 'POST',
      body: JSON.stringify({ lat: latitude, lng: longitude }),
    });
  }

  /**
   * Get heatmap data for map overlay
   */
  async getHeatmapData() {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/map/heatmap-data`);
  }

  /**
   * Get location forecast
   */
  async getLocationForecast(latitude, longitude, hours = 8) {
    return this.fetchWithErrorHandling(
      `${API_BASE_URL}/map/forecast/${latitude}/${longitude}?hours=${hours}`
    );
  }

  /**
   * Get active map alerts
   */
  async getActiveMapAlerts() {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/map/active-alerts`);
  }

  // ==================== Alerts ====================

  /**
   * Get active alerts
   */
  async getActiveAlerts(severity = null, limit = 50) {
    const params = new URLSearchParams({ limit: limit.toString() });
    
    if (severity) {
      params.append('severity', severity);
    }

    return this.fetchWithErrorHandling(`${API_BASE_URL}/alerts/active?${params}`);
  }

  /**
   * Get alert history
   */
  async getAlertHistory(days = 7) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/alerts/history?days=${days}`);
  }

  /**
   * Get alert statistics
   */
  async getAlertStatistics() {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/alerts/statistics`);
  }

  /**
   * Get nearby alerts
   */
  async getNearbyAlerts(latitude, longitude, radiusKm = 10) {
    const params = new URLSearchParams({
      latitude: latitude.toString(),
      longitude: longitude.toString(),
      radius_km: radiusKm.toString(),
    });

    return this.fetchWithErrorHandling(`${API_BASE_URL}/alerts/nearby-alerts?${params}`);
  }

  // ==================== Notifications ====================

  /**
   * Subscribe to notifications
   */
  async subscribeToNotifications(data) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/notifications/subscribe`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Get subscriptions for a user
   */
  async getSubscriptions(email) {
    const params = new URLSearchParams({ email });
    return this.fetchWithErrorHandling(`${API_BASE_URL}/notifications/subscriptions?${params}`);
  }

  /**
   * Unsubscribe from notifications
   */
  async unsubscribe(subscriptionId) {
    return this.fetchWithErrorHandling(
      `${API_BASE_URL}/notifications/unsubscribe/${subscriptionId}`,
      { method: 'DELETE' }
    );
  }

  // ==================== Health Check ====================

  /**
   * Check API health
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_ROOT}/health`);
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  /**
   * Analyze route using AI
   */
  async analyzeRoute(pointA, pointB, vehicleType) {
    return this.fetchWithErrorHandling(`${API_ROOT}/api/route-verdict`, {
      method: 'POST',
      body: JSON.stringify({
        point_a: pointA,
        point_b: pointB,
        vehicle_type: vehicleType
      }),
    });
  }

  /**
   * Get rainfall prediction for a location
   */
  async getRainfallPrediction(latitude, longitude) {
    return this.fetchWithErrorHandling(`${API_BASE_URL}/map/forecast/${latitude}/${longitude}?hours=24`);
  }
}

// Export singleton instance
const apiService = new ApiService();
export default apiService;
