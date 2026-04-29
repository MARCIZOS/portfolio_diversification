import React, { useState, useContext } from 'react';
import { X, User, Settings, CreditCard, Key, CheckCircle, Copy } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import './SettingsModal.css';

const SettingsModal = ({ isOpen, onClose, initialTab = 'profile' }) => {
  const { user } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState(initialTab);
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const handleCopyApi = () => {
    navigator.clipboard.writeText('sk_test_51NxXXXXXXXXXXXXXXXXXXXXXX');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content glass-card animate-fade-in">
        <button className="modal-close btn-icon" onClick={onClose}>
          <X size={20} />
        </button>
        
        <div className="modal-layout">
          {/* Sidebar */}
          <aside className="modal-sidebar">
            <h3 className="modal-title">Settings</h3>
            <nav className="modal-nav">
              <button 
                className={`modal-nav-item ${activeTab === 'profile' ? 'active' : ''}`}
                onClick={() => setActiveTab('profile')}
              >
                <User size={16} /> My Profile
              </button>
              <button 
                className={`modal-nav-item ${activeTab === 'settings' ? 'active' : ''}`}
                onClick={() => setActiveTab('settings')}
              >
                <Settings size={16} /> Account Settings
              </button>
              <button 
                className={`modal-nav-item ${activeTab === 'billing' ? 'active' : ''}`}
                onClick={() => setActiveTab('billing')}
              >
                <CreditCard size={16} /> Billing & Plan
              </button>
              <button 
                className={`modal-nav-item ${activeTab === 'apikeys' ? 'active' : ''}`}
                onClick={() => setActiveTab('apikeys')}
              >
                <Key size={16} /> API Keys
              </button>
            </nav>
          </aside>

          {/* Content Area */}
          <main className="modal-body">
            {activeTab === 'profile' && (
              <div className="tab-content animate-fade-in">
                <h4>Profile Information</h4>
                <p className="text-sub mb-4">Manage your public profile details.</p>
                <div className="form-group">
                  <label className="form-label">Username</label>
                  <input type="text" className="form-input" defaultValue={user?.username} readOnly />
                </div>
                <div className="form-group">
                  <label className="form-label">Role</label>
                  <input type="text" className="form-input" defaultValue="Quantitative Analyst" readOnly />
                </div>
                <button className="btn btn-primary mt-2">Save Changes</button>
              </div>
            )}

            {activeTab === 'settings' && (
              <div className="tab-content animate-fade-in">
                <h4>Account Preferences</h4>
                <p className="text-sub mb-4">Update your application preferences.</p>
                <div className="form-group">
                  <label className="form-label">Theme</label>
                  <select className="form-input">
                    <option>Institutional Dark (Current)</option>
                    <option>Light Mode</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Default Risk Threshold (VaR 95%)</label>
                  <input type="number" step="0.01" className="form-input" defaultValue="-0.02" />
                </div>
                <button className="btn btn-primary mt-2">Update Preferences</button>
              </div>
            )}

            {activeTab === 'billing' && (
              <div className="tab-content animate-fade-in">
                <h4>Billing & Plan</h4>
                <p className="text-sub mb-4">Manage your subscription.</p>
                <div className="billing-card glass-panel mb-4">
                  <div className="flex justify-between items-center mb-2">
                    <h5 className="text-primary">Pro Analyst Plan</h5>
                    <span className="badge-active">Active</span>
                  </div>
                  <h2 className="text-mint">$49<span className="text-sm text-sub">/mo</span></h2>
                  <p className="text-sub mt-2">Includes unlimited RAG queries and advanced stress testing.</p>
                </div>
                <button className="btn btn-secondary w-full">Manage Subscription (Stripe)</button>
              </div>
            )}

            {activeTab === 'apikeys' && (
              <div className="tab-content animate-fade-in">
                <h4>API Access</h4>
                <p className="text-sub mb-4">Connect external systems to ARAIA's risk engine.</p>
                <div className="form-group">
                  <label className="form-label">Secret Key (Test)</label>
                  <div className="flex gap-2">
                    <input type="password" className="form-input flex-1" defaultValue="sk_test_51NxXXXXXXXXXXXXXXXXXXXXXX" readOnly />
                    <button className="btn btn-secondary" onClick={handleCopyApi}>
                      {copied ? <CheckCircle size={16} className="text-mint" /> : <Copy size={16} />}
                    </button>
                  </div>
                </div>
                <button className="btn btn-primary mt-2"><Key size={16} /> Generate New Key</button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
