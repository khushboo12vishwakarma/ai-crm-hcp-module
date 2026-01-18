/**
 * ChatAssistant Component (Right Panel)
 * Chat interface that controls the form
 */
import React, { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  addMessage,
  setFormData,
  setLoading,
  setError,
  clearError
} from '../redux/slices/interactionSlice';
import { sendMessage } from '../services/api';
import '../styles/ChatAssistant.css';

const ChatAssistant = () => {
  const dispatch = useDispatch();
  const { messages, loading, error, savedInteractionId } = useSelector(
    (state) => state.interaction
  );
  
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const handleSend = async () => {
    if (!inputValue.trim()) return;
    
    const userMessage = inputValue.trim();
    setInputValue(''); // Clear input immediately
    
    // Add user message to chat
    dispatch(addMessage({
      role: 'user',
      content: userMessage
    }));
    
    // Set loading state
    dispatch(setLoading(true));
    dispatch(clearError());
    
    try {
      // Call backend API
      const response = await sendMessage(userMessage, savedInteractionId);
      
      // Update form with extracted data
      dispatch(setFormData(response.form_data));
      
      // Add assistant response to chat
      dispatch(addMessage({
        role: 'assistant',
        content: response.chat_response
      }));
      
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Unknown error';
      
      dispatch(setError(errorMessage));
      dispatch(addMessage({
        role: 'assistant',
        content: `❌ Error: ${errorMessage}`
      }));
      
    } finally {
      dispatch(setLoading(false));
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  
  return (
    <div className="chat-assistant">
      <div className="chat-header">
        <h2>💬 AI Assistant</h2>
        <p className="chat-subtitle">Describe your interaction naturally</p>
      </div>
      
      {/* Messages Area */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>👋 Welcome!</h3>
            <p>Tell me about your HCP interaction, and I'll fill the form for you.</p>
            <div className="examples">
              <p><strong>Try saying:</strong></p>
              <ul>
                <li>"I met with Dr. Smith today and discussed product X..."</li>
                <li>"The sentiment was positive, shared brochures"</li>
                <li>"Actually, the name was Dr. John"</li>
              </ul>
            </div>
          </div>
        )}
        
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.role}`}
          >
            <div className="message-content">
              {message.content}
            </div>
            <div className="message-time">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message assistant">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              Processing...
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Error Display */}
      {error && (
        <div className="chat-error">
          ⚠️ {error}
        </div>
      )}
      
      {/* Input Area */}
      <div className="chat-input-container">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here... (Press Enter to send)"
          className="chat-input"
          rows="3"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !inputValue.trim()}
          className="btn btn-send"
        >
          {loading ? '⏳ Processing...' : '📤 Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatAssistant;
