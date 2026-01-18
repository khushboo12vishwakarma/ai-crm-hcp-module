/**
 * Redux slice for managing interaction form state and chat messages.
 */
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  // Form data (auto-filled by AI, never manually edited)
  form: {
    hcp_name: '',
    date: '',
    sentiment: 'Neutral',
    materials_shared: [],
    discussion_summary: '',
    products_discussed: [],
    follow_up_date: '',
    key_insights: ''
  },
  
  // Chat messages history
  messages: [],
  
  // UI state
  loading: false,
  error: null,
  
  // Saved interaction ID (if saved to database)
  savedInteractionId: null
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    // Set entire form data (when AI returns extracted data)
    setFormData: (state, action) => {
      state.form = {
        ...state.form,
        ...action.payload
      };
    },
    
    // Add a chat message
    addMessage: (state, action) => {
      state.messages.push({
        id: Date.now(),
        role: action.payload.role, // 'user' or 'assistant'
        content: action.payload.content,
        timestamp: new Date().toISOString()
      });
    },
    
    // Set loading state
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    
    // Set error
    setError: (state, action) => {
      state.error = action.payload;
    },
    
    // Clear error
    clearError: (state) => {
      state.error = null;
    },
    
    // Set saved interaction ID
    setSavedInteractionId: (state, action) => {
      state.savedInteractionId = action.payload;
    },
    
    // Clear entire form
    clearForm: (state) => {
      state.form = initialState.form;
      state.messages = [];
      state.savedInteractionId = null;
      state.error = null;
    }
  }
});

export const {
  setFormData,
  addMessage,
  setLoading,
  setError,
  clearError,
  setSavedInteractionId,
  clearForm
} = interactionSlice.actions;

export default interactionSlice.reducer;
