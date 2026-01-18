/**
 * InteractionForm Component (Left Panel)
 * Displays auto-filled form data - ALL FIELDS ARE READ-ONLY
 */
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { clearForm, setError } from '../redux/slices/interactionSlice';
import { saveInteraction } from '../services/api';
import '../styles/InteractionForm.css';

const InteractionForm = () => {
  const dispatch = useDispatch();
  const { form, savedInteractionId } = useSelector((state) => state.interaction);
  
  const handleSave = async () => {
    try {
      // Validate required fields
      if (!form.hcp_name || !form.date) {
        dispatch(setError('HCP name and date are required to save'));
        return;
      }
      
      // Save to backend
      const result = await saveInteraction(form);
      
      alert(`✅ Interaction saved successfully! ID: ${result.id}`);
      
    } catch (error) {
      console.error('Save error:', error);
      dispatch(setError('Failed to save interaction: ' + error.message));
    }
  };
  
  const handleClear = () => {
    if (window.confirm('Are you sure you want to clear the form and start over?')) {
      dispatch(clearForm());
    }
  };
  
  return (
    <div className="interaction-form">
      <div className="form-header">
        <h2>📋 Interaction Details</h2>
        <p className="form-subtitle">All fields auto-filled by AI assistant →</p>
      </div>
      
      <div className="form-content">
        {/* HCP Name */}
        <div className="form-group">
          <label htmlFor="hcp_name">Healthcare Professional</label>
          <input
            id="hcp_name"
            type="text"
            value={form.hcp_name}
            readOnly
            placeholder="Will be auto-filled..."
            className="read-only-input"
          />
        </div>
        
        {/* Date */}
        <div className="form-group">
          <label htmlFor="date">Date of Interaction</label>
          <input
            id="date"
            type="date"
            value={form.date}
            readOnly
            className="read-only-input"
          />
        </div>
        
        {/* Sentiment */}
        <div className="form-group">
          <label htmlFor="sentiment">Sentiment</label>
          <select
            id="sentiment"
            value={form.sentiment}
            disabled
            className="read-only-select"
          >
            <option value="Positive">😊 Positive</option>
            <option value="Neutral">😐 Neutral</option>
            <option value="Negative">😞 Negative</option>
          </select>
        </div>
        
        {/* Materials Shared */}
        <div className="form-group">
          <label>Materials Shared</label>
          <div className="checkbox-group">
            {['Brochures', 'Samples', 'Clinical Data', 'Presentation'].map((material) => (
              <label key={material} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={form.materials_shared.includes(material.toLowerCase())}
                  readOnly
                  disabled
                />
                <span>{material}</span>
              </label>
            ))}
          </div>
          {form.materials_shared.length > 0 && (
            <div className="selected-items">
              {form.materials_shared.map((item, idx) => (
                <span key={idx} className="tag">{item}</span>
              ))}
            </div>
          )}
        </div>
        
        {/* Discussion Summary */}
        <div className="form-group">
          <label htmlFor="discussion_summary">Discussion Summary</label>
          <textarea
            id="discussion_summary"
            value={form.discussion_summary}
            readOnly
            placeholder="Will be auto-filled..."
            rows="4"
            className="read-only-textarea"
          />
        </div>
        
        {/* Products Discussed */}
        <div className="form-group">
          <label htmlFor="products_discussed">Products Discussed</label>
          <input
            id="products_discussed"
            type="text"
            value={form.products_discussed.join(', ')}
            readOnly
            placeholder="Will be auto-filled..."
            className="read-only-input"
          />
        </div>
        
        {/* Follow-up Date */}
        <div className="form-group">
          <label htmlFor="follow_up_date">Follow-up Date (Optional)</label>
          <input
            id="follow_up_date"
            type="date"
            value={form.follow_up_date}
            readOnly
            className="read-only-input"
          />
        </div>
        
        {/* Key Insights */}
        <div className="form-group">
          <label htmlFor="key_insights">AI-Generated Insights</label>
          <textarea
            id="key_insights"
            value={form.key_insights}
            readOnly
            placeholder="Will be auto-filled..."
            rows="4"
            className="read-only-textarea"
          />
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="form-actions">
        <button onClick={handleSave} className="btn btn-primary">
          💾 Save Interaction
        </button>
        <button onClick={handleClear} className="btn btn-secondary">
          🗑️ Clear Form
        </button>
      </div>
    </div>
  );
};

export default InteractionForm;
