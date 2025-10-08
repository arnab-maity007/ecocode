import React from 'react';
import { Info, Target, Users, Zap } from 'lucide-react';

const About = () => {
  return (
    <div className="min-h-screen py-20 bg-flood-darker">
      <div className="container mx-auto px-6">
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-flood-cyan/10 rounded-2xl mb-6 border border-flood-cyan/30">
            <Info className="w-10 h-10 text-flood-cyan" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            About <span className="text-flood-cyan">FloodAura</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            Leveraging AI and satellite technology for climate resilience
          </p>
        </div>

        {/* Mission Section */}
        <div className="max-w-4xl mx-auto mb-16">
          <div className="bg-flood-navy/60 backdrop-blur-sm border border-gray-800 rounded-2xl p-8">
            <h2 className="text-3xl font-bold text-white mb-6">Our Mission</h2>
            <p className="text-gray-300 leading-relaxed text-lg mb-4">
              FloodAura is dedicated to protecting urban communities from the devastating impacts of flooding through cutting-edge AI technology and real-time data analysis.
            </p>
            <p className="text-gray-300 leading-relaxed text-lg">
              By combining satellite imagery, machine learning, and hyperlocal sensors, we provide unprecedented accuracy in flood prediction, giving communities the time they need to prepare and respond effectively.
            </p>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-flood-navy/60 backdrop-blur-sm border border-gray-800 rounded-xl p-6 text-center hover:border-flood-cyan/50 transition-all duration-300">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-flood-cyan/10 rounded-xl mb-4 border border-flood-cyan/30">
              <Target className="w-8 h-8 text-flood-cyan" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Precision</h3>
            <p className="text-gray-400">
              Street-level accuracy with 85%+ prediction reliability
            </p>
          </div>

          <div className="bg-flood-navy/60 backdrop-blur-sm border border-gray-800 rounded-xl p-6 text-center hover:border-flood-cyan/50 transition-all duration-300">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-flood-cyan/10 rounded-xl mb-4 border border-flood-cyan/30">
              <Zap className="w-8 h-8 text-flood-cyan" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Speed</h3>
            <p className="text-gray-400">
              Real-time processing with sub-2-minute response times
            </p>
          </div>

          <div className="bg-flood-navy/60 backdrop-blur-sm border border-gray-800 rounded-xl p-6 text-center hover:border-flood-cyan/50 transition-all duration-300">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-flood-cyan/10 rounded-xl mb-4 border border-flood-cyan/30">
              <Users className="w-8 h-8 text-flood-cyan" />
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Community</h3>
            <p className="text-gray-400">
              Protecting 10,000+ streets and countless lives
            </p>
          </div>
        </div>

        {/* Technology Stack */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-flood-navy/60 backdrop-blur-sm border border-gray-800 rounded-2xl p-8">
            <h2 className="text-3xl font-bold text-white mb-6">Technology Stack</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-xl font-semibold text-flood-cyan mb-3">Data Sources</h3>
                <ul className="space-y-2 text-gray-300">
                  <li>• Satellite imagery and remote sensing</li>
                  <li>• Weather station networks</li>
                  <li>• IoT sensor arrays</li>
                  <li>• Topographical data</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold text-flood-cyan mb-3">AI & Processing</h3>
                <ul className="space-y-2 text-gray-300">
                  <li>• Deep learning models</li>
                  <li>• Real-time data fusion</li>
                  <li>• Predictive analytics</li>
                  <li>• Computer vision</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
