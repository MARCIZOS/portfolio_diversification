import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Globe, ChevronDown, CheckCircle2, BarChart2, Activity, Shield, Zap } from 'lucide-react';
import './Landing.css';

const Landing = () => {
  const [langOpen, setLangOpen] = useState(false);

  return (
    <div className="landing-wrapper">
      
      {/* Background Elements */}
      <div className="bg-glow"></div>
      
      {/* Top Navigation Layout */}
      <header className="top-header container">
        <div className="logo text-gradient-bright">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="mr-2 inline-block">
            <path d="M4 14L10 8L16 14" stroke="#34d399" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M10 20V8" stroke="#34d399" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M20 14L14 8L8 14" stroke="#059669" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" opacity="0.5"/>
          </svg>
          ARAIA
        </div>
        
        <nav className="glass-pill-nav">
          <a href="#home" className="nav-item active">Home</a>
          <a href="#about" className="nav-item">About</a>
          <a href="#features" className="nav-item">Features</a>
          <a href="#solution" className="nav-item">Solution</a>
          <a href="#pricing" className="nav-item">Pricing</a>
          <div className="nav-divider"></div>
          <div className="lang-container" style={{ position: 'relative' }}>
            <button className="nav-item lang-select" onClick={() => setLangOpen(!langOpen)}>
              <Globe size={14}/> English <ChevronDown size={14}/>
            </button>
            {langOpen && (
              <div className="lang-dropdown">
                <button onClick={() => setLangOpen(false)}>English</button>
                <button onClick={() => setLangOpen(false)}>Spanish</button>
                <button onClick={() => setLangOpen(false)}>French</button>
              </div>
            )}
          </div>
        </nav>
        
        <div className="nav-actions">
          <Link to="/login" className="btn-pill btn-glow">Login / Register</Link>
        </div>
      </header>

      {/* Main Hero Area */}
      <main id="home" className="hero-main">
        {/* Giant Background Text */}
        <div className="giant-bg-text">ARAIA PDMS</div>
        
        {/* Center 3D Asset */}
        <div className="hero-center-asset animate-float">
          <img src="/hero-asset.png" alt="3D Crystal Asset" />
        </div>

        {/* Left Content */}
        <div className="hero-left-content animate-fade-in-left">
          <h1 className="hero-heading">PORTFOLIO<br/>DIVERSIFICATION</h1>
          <p className="hero-description">
            Advanced risk management, stress<br/>
            testing, and quantitative insights<br/>
            for modern institutional analysts.
          </p>
          <div className="hero-buttons">
            <Link to="/signup" className="btn-pill btn-glow">Get Started</Link>
          </div>
        </div>




      </main>

      {/* About Section */}
      <section id="about" className="content-section">
        <div className="section-head text-center">
          <h2 className="section-title">About ARAIA</h2>
          <p className="section-subtitle">Born from a need for resilient portfolio architecture.</p>
        </div>
        <div className="about-content text-center max-w-3xl mx-auto">
          <p className="text-secondary leading-relaxed">
            ARAIA PDMS was built to solve the modern quantitative analyst's biggest challenge: true diversification in highly correlated markets. Traditional asset allocation models fail during market panics because correlations converge to 1. ARAIA utilizes advanced hierarchical risk parity and AI-driven insights to uncover hidden concentration pockets before they become systemic risks to your portfolio.
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="section-head text-center">
          <h2 className="section-title">Engineered for Excellence</h2>
          <p className="section-subtitle">Everything you need to analyze, stress-test, and optimize.</p>
        </div>
        
        <div className="features-grid">
          <div className="feature-box glass-card">
            <div className="feature-icon-wrapper"><BarChart2 size={24} /></div>
            <h3>Advanced Risk Metrics</h3>
            <p>Compute Expected Shortfall (CVaR), Value at Risk, and Max Drawdown instantly with institutional models.</p>
          </div>
          <div className="feature-box glass-card">
            <div className="feature-icon-wrapper"><Activity size={24} /></div>
            <h3>Stress Testing</h3>
            <p>Simulate extreme market downturns and observe how vulnerable correlations behave under pressure.</p>
          </div>
          <div className="feature-box glass-card">
            <div className="feature-icon-wrapper"><Shield size={24} /></div>
            <h3>Cluster Concentration</h3>
            <p>Identify hidden correlation pockets and ensure true diversification beyond just asset count.</p>
          </div>
          <div className="feature-box glass-card">
            <div className="feature-icon-wrapper"><Zap size={24} /></div>
            <h3>AI Advisory Engine</h3>
            <p>Leverage our proprietary Retrieval-Augmented Generation to get qualitative context on quantitative risks.</p>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section id="solution" className="content-section">
        <div className="section-head text-center">
          <h2 className="section-title">The Solution</h2>
          <p className="section-subtitle">A seamless workflow from raw data to actionable insights.</p>
        </div>
        <div className="solution-steps">
          <div className="step-card glass-card">
            <div className="step-number">1</div>
            <h4>Input Assets</h4>
            <p>Define your portfolio tickers and weights natively in our secure dashboard.</p>
          </div>
          <div className="step-card glass-card">
            <div className="step-number">2</div>
            <h4>Compute Risk</h4>
            <p>Our Fast API backend parallel-processes your data through heavy quantitative models.</p>
          </div>
          <div className="step-card glass-card">
            <div className="step-number">3</div>
            <h4>Optimize</h4>
            <p>Receive an AI-generated advisory report on exactly how to rebalance for safety.</p>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="content-section">
        <div className="section-head text-center">
          <h2 className="section-title">Transparent Pricing</h2>
          <p className="section-subtitle">Scale your risk management without scaling costs.</p>
        </div>
        <div className="pricing-grid">
          <div className="pricing-card glass-card">
            <h3>Analyst</h3>
            <div className="price">$49<span>/mo</span></div>
            <ul className="pricing-features">
              <li><CheckCircle2 size={16} className="text-mint"/> Full Dashboard Access</li>
              <li><CheckCircle2 size={16} className="text-mint"/> 100 RAG Queries/mo</li>
              <li><CheckCircle2 size={16} className="text-mint"/> Standard Stress Tests</li>
            </ul>
            <Link to="/signup" className="btn-pill btn-glass w-full">Start Trial</Link>
          </div>
          <div className="pricing-card glass-card premium">
            <div className="premium-badge">Most Popular</div>
            <h3>Institutional</h3>
            <div className="price">$299<span>/mo</span></div>
            <ul className="pricing-features">
              <li><CheckCircle2 size={16} className="text-mint"/> API Access</li>
              <li><CheckCircle2 size={16} className="text-mint"/> Unlimited RAG Queries</li>
              <li><CheckCircle2 size={16} className="text-mint"/> Custom Stress Scenarios</li>
              <li><CheckCircle2 size={16} className="text-mint"/> Priority Support</li>
            </ul>
            <Link to="/signup" className="btn-pill btn-glow w-full">Get Institutional</Link>
          </div>
        </div>
      </section>

      {/* Bottom Wave Footer */}
      <div className="bottom-wave">
        <svg viewBox="0 0 1440 120" className="wave-svg" preserveAspectRatio="none">
           <path d="M0,120 C320,120 420,0 720,0 C1020,0 1120,120 1440,120 Z" fill="#040c09" />
        </svg>
      </div>

    </div>
  );
};

export default Landing;
