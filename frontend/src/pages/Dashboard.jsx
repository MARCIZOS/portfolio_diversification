import React, { useState, useContext, useRef, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { analyzePortfolio } from '../services/api';
import { LogOut, Play, Plus, Trash2, User, Settings, CreditCard, Key, ChevronDown, Upload, Edit3, FileSpreadsheet } from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, 
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend
} from 'recharts';
import SettingsModal from '../components/SettingsModal';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useContext(AuthContext);
  
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [profileOpen, setProfileOpen] = useState(false);
  const [settingsTab, setSettingsTab] = useState(null);
  
  const profileRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setProfileOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleAddAsset = () => setAssets([...assets, { ticker: '', weight: 0 }]);
  const handleRemoveAsset = (idx) => setAssets(assets.filter((_, i) => i !== idx));
  const handleAssetChange = (idx, field, value) => {
    const newAssets = [...assets];
    newAssets[idx][field] = field === 'weight' ? parseFloat(value) || 0 : value.toUpperCase();
    setAssets(newAssets);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      const text = evt.target.result;
      const lines = text.split('\n').map(l => l.trim()).filter(l => l);
      
      const parsedAssets = [];
      const startIdx = lines.length > 0 && lines[0].toLowerCase().includes('ticker') ? 1 : 0;
      
      for (let i = startIdx; i < lines.length; i++) {
        const parts = lines[i].split(',');
        if (parts.length >= 2) {
          const ticker = parts[0].trim().toUpperCase();
          const weight = parseFloat(parts[1].trim());
          if (ticker && !isNaN(weight)) {
            parsedAssets.push({ ticker, weight });
          }
        }
      }
      
      if (parsedAssets.length > 0) {
        setAssets(parsedAssets);
        setError('');
      } else {
        setError('No valid assets found in CSV.');
      }
    };
    reader.readAsText(file);
    e.target.value = null;
  };

  const handleAnalyze = async () => {
    setError('');
    setLoading(true);
    const totalWeight = assets.reduce((sum, a) => sum + a.weight, 0);
    const normalized = assets.map(a => ({
      ticker: a.ticker,
      weight: totalWeight > 0 ? a.weight / totalWeight : 0
    })).filter(a => a.ticker && a.weight > 0);

    if (normalized.length === 0) {
      setError('Please add valid assets.');
      setLoading(false);
      return;
    }

    try {
      const data = await analyzePortfolio(normalized, true);
      setResults(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  // Color Palette
  const COLORS = ['#6ee7b7', '#34d399', '#059669', '#047857', '#064e3b', '#a7f3d0'];

  // Data Formatters
  const getStressData = () => {
    if (!results) return [];
    return [
      { name: 'VaR', Normal: results.stress.normal_var, Stressed: results.stress.stressed_var },
      { name: 'CVaR', Normal: results.stress.normal_cvar, Stressed: results.stress.stressed_cvar }
    ];
  };

  const getWeightData = () => {
    if (!results) return [];
    return results.assets.map(a => ({ name: a.ticker, value: a.weight }));
  };

  const getRiskContributionData = () => {
    if (!results) return [];
    const vol = results.metrics.volatility;
    return results.assets.map(a => ({ name: a.ticker, value: a.weight * vol }));
  };

  const getRadarData = () => {
    if (!results) return [];
    const m = results.metrics;
    const s = results.stress;
    const d = results.diversification;
    return [
      { subject: 'CVaR', A: Math.min(Math.abs(m.cvar) * 10, 1) },
      { subject: 'VaR', A: Math.min(Math.abs(m.var) * 10, 1) },
      { subject: 'Volatility', A: Math.min(m.volatility * 2, 1) },
      { subject: 'Diversity', A: d.diversification_score },
      { subject: 'Stress', A: Math.min(Math.abs(s.stressed_cvar) * 10, 1) },
      { subject: 'Drawdown', A: Math.min(Math.abs(m.max_drawdown) * 2, 1) },
    ];
  };

  const getClusterWeights = () => {
    if (!results) return [];
    const weights = {};
    Object.entries(results.clusters).forEach(([cId, tickers]) => {
      weights[`Cluster ${cId}`] = tickers.reduce((sum, t) => {
        const asset = results.assets.find(a => a.ticker === t);
        return sum + (asset ? asset.weight : 0);
      }, 0);
    });
    return Object.entries(weights).map(([name, weight]) => ({ name, weight }));
  };

  const renderMetric = (label, val, subtitle, isPct = false) => (
    <div className="glass-card metric-box">
      <div className="metric-label">{label}</div>
      <div className="metric-val">{isPct ? `${(val*100).toFixed(2)}%` : val.toFixed(4)}</div>
      <div className="metric-sub">{subtitle}</div>
    </div>
  );

  const openSettings = (tab) => {
    setSettingsTab(tab);
    setProfileOpen(false);
  };

  return (
    <div className="dashboard-layout">
      {/* Settings Modal */}
      <SettingsModal 
        isOpen={!!settingsTab} 
        onClose={() => setSettingsTab(null)} 
        initialTab={settingsTab || 'profile'} 
      />

      {/* Top Navbar */}
      <nav className="dash-nav glass-panel">
        <div className="logo text-gradient">ARAIA</div>
        
        {/* Profile Dropdown Section */}
        <div className="nav-controls" ref={profileRef}>
          <div 
            className="profile-trigger flex items-center gap-2 cursor-pointer" 
            onClick={() => setProfileOpen(!profileOpen)}
          >
            <div className="avatar bg-mint text-dark flex items-center justify-center">
              {user?.username?.charAt(0).toUpperCase() || 'U'}
            </div>
            <span className="text-primary text-sm font-medium">{user?.username}</span>
            <ChevronDown size={14} className="text-muted" />
          </div>

          {profileOpen && (
            <div className="profile-dropdown glass-card animate-fade-in">
              <div className="profile-header">
                <div className="profile-name">{user?.username}</div>
                <div className="profile-role">Quantitative Analyst</div>
              </div>
              <div className="profile-menu">
                <button className="profile-menu-item" onClick={() => openSettings('profile')}>
                  <User size={16} /> My Profile
                </button>
                <button className="profile-menu-item" onClick={() => openSettings('settings')}>
                  <Settings size={16} /> Account Settings
                </button>
                <button className="profile-menu-item" onClick={() => openSettings('billing')}>
                  <CreditCard size={16} /> Billing & Plan
                </button>
                <button className="profile-menu-item" onClick={() => openSettings('apikeys')}>
                  <Key size={16} /> API Keys
                </button>
                <div className="divider"></div>
                <button className="profile-menu-item text-danger" onClick={logout}>
                  <LogOut size={16} /> Sign Out
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      <div className="dash-grid">
        {/* Left Panel: Inputs */}
        <aside className="input-panel glass-card flex flex-col">
          <div className="panel-header mb-2">
            <h4 className="flex items-center gap-2 text-lg"><FileSpreadsheet size={18} className="text-mint"/> Configure Your Portfolio</h4>
          </div>

          <div className="upload-section mt-2">
            <div className="section-label flex items-center gap-2 mb-2">
               <FileSpreadsheet size={14} className="text-muted" /> Upload Portfolio from CSV
            </div>
            
            <p className="text-xs text-muted mb-2">Choose a CSV file</p>
            <div className="upload-dropzone glass-panel flex items-center justify-between">
              <div className="flex items-center gap-4">
                <input type="file" accept=".csv" id="csv-upload" className="hidden-input" onChange={handleFileUpload} />
                <label htmlFor="csv-upload" className="btn-upload glass-card flex items-center gap-2 cursor-pointer">
                  <Upload size={14} /> Upload
                </label>
                <span className="text-xs text-muted">200MB per file • CSV</span>
              </div>
            </div>
          </div>

          <div className="divider my-4"></div>

          <div className="manual-entry-header flex justify-between items-center mb-2">
            <div className="section-label flex items-center gap-2">
              <Edit3 size={14} className="text-muted" /> Manual Entry
            </div>
          </div>
          
          <div className="asset-headers text-xs text-muted flex mb-2 px-1">
             <span className="flex-1">Ticker</span>
             <span className="flex-1">Weight</span>
             <span className="w-8 text-center">Action</span>
          </div>

          <div className="asset-list flex-1 overflow-y-auto pr-1">
            {assets.map((a, i) => (
              <div key={i} className="asset-row mb-2">
                <input type="text" className="form-input flex-1" value={a.ticker} onChange={e => handleAssetChange(i, 'ticker', e.target.value)} placeholder="Ticker" />
                <input type="number" step="0.05" className="form-input flex-1" value={a.weight} onChange={e => handleAssetChange(i, 'weight', e.target.value)} />
                <button onClick={() => handleRemoveAsset(i)} className="btn-icon text-muted w-8 flex justify-center"><Trash2 size={14}/></button>
              </div>
            ))}
          </div>
          
          <div className="mt-2">
            <button onClick={handleAddAsset} className="btn-add-asset glass-card w-auto flex items-center gap-2 text-mint font-medium text-sm">
              <Plus size={14}/> Add Asset
            </button>
          </div>

          <button onClick={handleAnalyze} className="btn btn-primary w-full mt-6" disabled={loading}>
            <Play size={14} /> {loading ? 'Computing...' : 'Run Analysis'}
          </button>
          {error && <div className="error-text mt-4">{error}</div>}
        </aside>

        {/* Right Panel: Results */}
        <main className="results-panel">
          {!results ? (
            <div className="empty-state text-muted">Initialize portfolio configuration to view analytics.</div>
          ) : (
            <div className="analytics-content animate-fade-in">
              
              {/* Top Metrics Row */}
              <div className="metrics-row">
                {renderMetric('VOLATILITY', results.metrics.volatility, 'Annualized risk', true)}
                {renderMetric('VAR 95%', results.metrics.var, 'Downside threshold')}
                {renderMetric('CVAR 95%', results.metrics.cvar, 'Tail loss average')}
                {renderMetric('MAX DRAWDOWN', results.metrics.max_drawdown, 'Peak-to-trough', true)}
              </div>

              {/* Row 2: Clusters & Diversification */}
              <div className="grid-2-col mt-4">
                <div className="glass-card">
                  <h4>Clusters & Correlations</h4>
                  <p className="text-sub">Concentration pockets and pair relationships.</p>
                  <div className="clusters-list mt-4">
                    {Object.entries(results.clusters).map(([cId, members]) => (
                      <div key={cId} className="cluster-badge">Cluster {cId}: {members.join(', ')}</div>
                    ))}
                  </div>
                  <table className="corr-table mt-4">
                    <thead><tr><th>Asset A</th><th>Asset B</th><th>Correlation</th></tr></thead>
                    <tbody>
                      {results.high_correlation_pairs.map((pair, i) => (
                        <tr key={i}><td>{pair[0]}</td><td>{pair[1]}</td><td className="text-right">{pair[2].toFixed(4)}</td></tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="glass-card">
                  <h4>Diversification</h4>
                  <p className="text-sub">Effective number of bets and cluster concentration.</p>
                  <div className="div-badges mt-2 mb-4">
                    <span className="div-badge">ENB {results.diversification.enb.toFixed(2)}</span>
                    <span className="div-badge">Score {results.diversification.diversification_score.toFixed(2)}</span>
                  </div>
                  <div className="chart-h-200">
                    <ResponsiveContainer>
                      <BarChart data={getClusterWeights()}>
                        <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                        <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                        <Tooltip cursor={{fill: '#0f2922'}} contentStyle={{background: '#050e0b', border: '1px solid #047857'}} />
                        <Bar dataKey="weight">
                          {getClusterWeights().map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Row 3: Correlation Matrix */}
              <div className="glass-card mt-4">
                <h4>Correlation Matrix</h4>
                <p className="text-sub mb-4">Cross-asset dependency view.</p>
                <div className="corr-matrix-wrapper">
                  <div className="corr-matrix" style={{ gridTemplateColumns: `100px repeat(${Object.keys(results.correlation_matrix).length}, 1fr)` }}>
                    <div className="cell header-cell"></div>
                    {Object.keys(results.correlation_matrix).map(ticker => (
                      <div key={ticker} className="cell header-cell">{ticker}</div>
                    ))}
                    
                    {Object.entries(results.correlation_matrix).map(([rowTicker, cols]) => (
                      <React.Fragment key={rowTicker}>
                        <div className="cell row-header">{rowTicker}</div>
                        {Object.keys(results.correlation_matrix).map(colTicker => {
                          const val = cols[colTicker];
                          const opacity = val > 0 ? 0.2 + (val * 0.8) : 0.1;
                          return (
                            <div key={`${rowTicker}-${colTicker}`} className="cell data-cell" style={{ backgroundColor: `rgba(110, 231, 183, ${opacity})`, color: val > 0.6 ? '#050e0b' : '#fff' }}>
                              {val.toFixed(2)}
                            </div>
                          );
                        })}
                      </React.Fragment>
                    ))}
                  </div>
                </div>
              </div>

              {/* Row 4: Risk Contribution & Stress */}
              <div className="grid-2-col mt-4">
                <div className="glass-card">
                  <h4>Risk Contribution & Mix</h4>
                  <div className="flex chart-h-250 mt-4">
                    <div className="flex-1">
                      <ResponsiveContainer>
                        <BarChart data={getRiskContributionData()}>
                          <XAxis dataKey="name" stroke="#64748b" fontSize={10} tick={{angle: -45, textAnchor: 'end'}} height={60} />
                          <YAxis stroke="#64748b" fontSize={10} />
                          <Tooltip cursor={{fill: '#0f2922'}} contentStyle={{background: '#050e0b', border: 'none'}} />
                          <Bar dataKey="value" fill="#34d399" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                    <div className="flex-1">
                      <ResponsiveContainer>
                        <PieChart>
                          <Pie data={getWeightData()} innerRadius={40} outerRadius={80} paddingAngle={2} dataKey="value">
                            {getWeightData().map((e, i) => <Cell key={`c-${i}`} fill={COLORS[i % COLORS.length]} />)}
                          </Pie>
                          <Tooltip contentStyle={{background: '#050e0b', border: 'none'}} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                <div className="glass-card">
                  <h4>Stress Comparison</h4>
                  <p className="text-sub mb-4">Normal versus stressed tail risk.</p>
                  <div className="chart-h-250">
                    <ResponsiveContainer>
                      <BarChart data={getStressData()}>
                        <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                        <YAxis stroke="#64748b" fontSize={12} />
                        <Tooltip cursor={{fill: '#0f2922'}} contentStyle={{background: '#050e0b', border: 'none'}} />
                        <Legend wrapperStyle={{fontSize: '12px'}} />
                        <Bar dataKey="Normal" fill="#059669" />
                        <Bar dataKey="Stressed" fill="#6ee7b7" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Row 5: Radar & AI */}
              <div className="grid-2-col mt-4">
                <div className="glass-card">
                  <h4>Portfolio Radar</h4>
                  <p className="text-sub mb-4">Normalized view of portfolio health dimensions.</p>
                  <div className="chart-h-300">
                    <ResponsiveContainer>
                      <RadarChart outerRadius="70%" data={getRadarData()}>
                        <PolarGrid stroke="#1f2937" />
                        <PolarAngleAxis dataKey="subject" tick={{ fill: '#a7f3d0', fontSize: 11 }} />
                        <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
                        <Radar name="Portfolio" dataKey="A" stroke="#34d399" fill="#34d399" fillOpacity={0.3} />
                      </RadarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="glass-card">
                  <h4>AI Advisory</h4>
                  <p className="text-sub mb-4">RAG-powered qualitative insights.</p>
                  <div className="ai-text">
                    {results.ai_explanation.split('\n').map((p, i) => p && <p key={i}>{p}</p>)}
                  </div>
                </div>
              </div>

            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
