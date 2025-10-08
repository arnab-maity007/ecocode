import React from 'react';
import { Link } from 'react-router-dom';
import { Droplet, Github, Twitter, Mail } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-flood-navy border-t border-gray-800/50 mt-20">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-gradient-to-br from-flood-cyan to-flood-blue p-2 rounded-lg shadow-cyan-glow">
                <Droplet className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">FloodAura</span>
            </div>
            <p className="text-gray-400 text-sm leading-relaxed">
              AI-powered hyperlocal flood forecasting for safer urban communities.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/live-map" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  Live Map
                </Link>
              </li>
              <li>
                <Link to="/alerts" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  Alerts
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-white font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="/documentation" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="/api" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  API Access
                </a>
              </li>
              <li>
                <a href="/privacy" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="/terms" className="text-gray-400 hover:text-flood-cyan transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>

          {/* Connect */}
          <div>
            <h3 className="text-white font-semibold mb-4">Connect</h3>
            <div className="flex space-x-4">
              <a
                href="https://github.com/floodaura"
                className="text-gray-400 hover:text-flood-cyan transition-colors"
                aria-label="GitHub"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="w-6 h-6" />
              </a>
              <a
                href="https://twitter.com/floodaura"
                className="text-gray-400 hover:text-flood-cyan transition-colors"
                aria-label="Twitter"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Twitter className="w-6 h-6" />
              </a>
              <a
                href="mailto:contact@floodaura.com"
                className="text-gray-400 hover:text-flood-cyan transition-colors"
                aria-label="Email"
              >
                <Mail className="w-6 h-6" />
              </a>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-gray-800/50 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            © 2025 FloodWatch. Powered by AI for Climate Resilience.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
