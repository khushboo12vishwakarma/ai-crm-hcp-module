/**
 * LogInteractionScreen Component (Main Layout)
 * Split-screen layout: Form (left) + Chat (right)
 */
import React from 'react';
import InteractionForm from './InteractionForm';
import ChatAssistant from './ChatAssistant';
import '../styles/LogInteractionScreen.css';

const LogInteractionScreen = () => {
  return (
    <div className="log-interaction-screen">
      {/* Header */}
      <header className="app-header">
        <h1>🏥 AI-First CRM - HCP Module</h1>
        <p>Healthcare Professional Interaction Logger</p>
      </header>
      
      {/* Main Split Screen */}
      <div className="split-container">
        {/* Left Panel: Form (auto-filled, read-only) */}
        <div className="left-panel">
          <InteractionForm />
        </div>
        
        {/* Right Panel: Chat Assistant */}
        <div className="right-panel">
          <ChatAssistant />
        </div>
      </div>
    </div>
  );
};

export default LogInteractionScreen;
