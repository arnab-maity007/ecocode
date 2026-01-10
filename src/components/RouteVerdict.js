import React, { useState } from 'react';
import { Navigation, Car, Bike, Truck, AlertTriangle, Clock } from 'lucide-react';
import apiService from '../services/api';

const RouteVerdict = ({ onRouteAnalysis }) => {
  const [pointA, setPointA] = useState('');
  const [pointB, setPointB] = useState('');
  const [vehicleType, setVehicleType] = useState('car');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [verdict, setVerdict] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  const vehicleOptions = [
    { id: 'bike', name: 'Two-Wheeler', icon: Bike },
    { id: 'car', name: 'Four-Wheeler', icon: Car },
    { id: 'suv', name: 'SUV/Truck', icon: Truck }
  ];

  const analyzeRoute = async () => {
    if (!pointA.trim() || !pointB.trim()) {
      alert('Please enter both starting and destination points');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      // Call backend API to analyze route using Gemini AI
      const data = await apiService.analyzeRoute(pointA, pointB, vehicleType);
      
      setVerdict(data);
      setLastUpdate(new Date());
      
      if (onRouteAnalysis) {
        onRouteAnalysis(data);
      }
    } catch (error) {
      console.error('Error analyzing route:', error);
      // Fallback to mock data for development
      const mockVerdict = {
        route_status: 'moderate_risk',
        overall_score: 65,
        recommendation: 'Proceed with caution. Consider alternative routes if available.',
        factors: {
          rainfall: {
            status: 'moderate',
            description: 'Moderate rainfall expected (40-60mm)',
            impact: 30
          },
          waterlogging: {
            status: 'high',
            description: 'High waterlogging risk in low-lying areas',
            impact: 45
          },
          traffic: {
            status: 'low',
            description: 'Light traffic expected on main routes',
            impact: 15
          },
          vehicle_suitability: {
            status: 'suitable',
            description: `${vehicleType.toUpperCase()} is suitable for these conditions`,
            impact: 10
          }
        },
        estimated_time: '45-60 minutes',
        alternative_route: 'Consider NH-48 via outer ring road',
        next_update: '1 hour'
      };
      setVerdict(mockVerdict);
      setLastUpdate(new Date());
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      'safe': 'text-green-500',
      'low': 'text-green-500',
      'suitable': 'text-green-500',
      'moderate': 'text-yellow-500',
      'moderate_risk': 'text-yellow-500',
      'high': 'text-red-500',
      'critical': 'text-red-500',
      'unsafe': 'text-red-500'
    };
    return colors[status] || 'text-gray-500';
  };

  const getStatusBg = (status) => {
    const colors = {
      'safe': 'bg-green-500/20',
      'low': 'bg-green-500/20',
      'suitable': 'bg-green-500/20',
      'moderate': 'bg-yellow-500/20',
      'moderate_risk': 'bg-yellow-500/20',
      'high': 'bg-red-500/20',
      'critical': 'bg-red-500/20',
      'unsafe': 'bg-red-500/20'
    };
    return colors[status] || 'bg-gray-500/20';
  };

  return (
    <div className="bg-flood-navy/40 border border-gray-800 rounded-lg p-6">
      <div className="flex items-center gap-2 mb-6">
        <Navigation className="w-6 h-6 text-flood-cyan" />
        <h2 className="text-white font-bold text-xl">AI Route Verdict</h2>
      </div>

      {/* Input Section */}
      <div className="space-y-4 mb-6">
        <div>
          <label className="text-gray-400 text-sm mb-2 block">Starting Point (A)</label>
          <input
            type="text"
            value={pointA}
            onChange={(e) => setPointA(e.target.value)}
            placeholder="Enter starting location..."
            className="w-full bg-flood-darker border border-gray-800 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-flood-cyan transition-colors"
          />
        </div>

        <div>
          <label className="text-gray-400 text-sm mb-2 block">Destination (B)</label>
          <input
            type="text"
            value={pointB}
            onChange={(e) => setPointB(e.target.value)}
            placeholder="Enter destination..."
            className="w-full bg-flood-darker border border-gray-800 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-flood-cyan transition-colors"
          />
        </div>

        <div>
          <label className="text-gray-400 text-sm mb-2 block">Vehicle Type</label>
          <div className="grid grid-cols-3 gap-2">
            {vehicleOptions.map((vehicle) => (
              <button
                key={vehicle.id}
                onClick={() => setVehicleType(vehicle.id)}
                className={`flex flex-col items-center gap-2 p-3 rounded-lg border transition-all ${
                  vehicleType === vehicle.id
                    ? 'bg-flood-cyan/20 border-flood-cyan text-flood-cyan'
                    : 'bg-flood-darker border-gray-800 text-gray-400 hover:border-gray-700'
                }`}
              >
                <vehicle.icon className="w-6 h-6" />
                <span className="text-xs">{vehicle.name}</span>
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={analyzeRoute}
          disabled={isAnalyzing}
          className="w-full bg-flood-cyan hover:bg-[#00BFFF] text-flood-navy px-6 py-3 rounded-lg font-semibold transition-all duration-300 shadow-cyan-glow disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isAnalyzing ? 'Analyzing Route...' : 'Get AI Verdict'}
        </button>
      </div>

      {/* Verdict Display */}
      {verdict && (
        <div className="space-y-4 border-t border-gray-800 pt-6">
          {/* Overall Status */}
          <div className={`${getStatusBg(verdict.route_status)} border border-gray-700 rounded-lg p-4`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-white font-semibold">Overall Status</span>
              <span className={`${getStatusColor(verdict.route_status)} font-bold text-lg`}>
                {verdict.overall_score}/100
              </span>
            </div>
            <p className="text-gray-300 text-sm">{verdict.recommendation}</p>
          </div>

          {/* Risk Factors */}
          <div className="space-y-3">
            <h3 className="text-white font-semibold text-sm mb-2">Risk Factors</h3>
            
            {verdict.factors && Object.entries(verdict.factors).map(([key, factor]) => (
              <div key={key} className="bg-flood-darker border border-gray-800 rounded-lg p-3">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-gray-300 text-sm capitalize">{key.replace('_', ' ')}</span>
                  <span className={`${getStatusColor(factor.status)} text-sm font-semibold`}>
                    {factor.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-400 text-xs mb-1">{factor.description}</p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-gray-800 rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full ${
                        factor.impact > 70 ? 'bg-red-500' :
                        factor.impact > 40 ? 'bg-yellow-500' :
                        'bg-green-500'
                      }`}
                      style={{ width: `${factor.impact}%` }}
                    ></div>
                  </div>
                  <span className="text-gray-500 text-xs">{factor.impact}%</span>
                </div>
              </div>
            ))}
          </div>

          {/* Additional Info */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-flood-darker border border-gray-800 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <Clock className="w-4 h-4 text-gray-400" />
                <span className="text-gray-400 text-xs">Est. Time</span>
              </div>
              <p className="text-white text-sm font-semibold">{verdict.estimated_time}</p>
            </div>
            
            <div className="bg-flood-darker border border-gray-800 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <AlertTriangle className="w-4 h-4 text-gray-400" />
                <span className="text-gray-400 text-xs">Next Update</span>
              </div>
              <p className="text-white text-sm font-semibold">{verdict.next_update}</p>
            </div>
          </div>

          {/* Alternative Route */}
          {verdict.alternative_route && (
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
              <p className="text-blue-400 text-sm">
                <strong>Alternative:</strong> {verdict.alternative_route}
              </p>
            </div>
          )}

          {/* Last Updated */}
          {lastUpdate && (
            <div className="text-center text-gray-500 text-xs">
              Last updated: {lastUpdate.toLocaleTimeString()}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RouteVerdict;
