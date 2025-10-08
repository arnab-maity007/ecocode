import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Droplet, Home as HomeIcon, Map, Bell, Info } from 'lucide-react';

const Header = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: HomeIcon },
    { path: '/live-map', label: 'Live Map', icon: Map },
    { path: '/alerts', label: 'Alerts', icon: Bell },
    { path: '/about', label: 'About', icon: Info },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <header className="bg-flood-navy/95 backdrop-blur-md border-b border-gray-800/50 sticky top-0 z-50 shadow-lg">
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="bg-gradient-to-br from-flood-cyan to-flood-blue p-2 rounded-lg group-hover:scale-110 transition-transform duration-300 shadow-cyan-glow">
              <Droplet className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white">FloodAura</span>
          </Link>

          {/* Navigation */}
          <div className="flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                    isActive(item.path)
                      ? 'bg-flood-cyan text-flood-navy font-semibold shadow-cyan-glow'
                      : 'text-gray-300 hover:text-white hover:bg-flood-cyan/10'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
