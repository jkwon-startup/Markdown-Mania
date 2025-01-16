import React, { createContext, useContext, useReducer } from 'react';

const GameContext = createContext();

const initialState = {
  currentStage: 1,
  points: 0,
  soundEnabled: true,
  language: 'ko',
  maxStage: 20,
};

function gameReducer(state, action) {
  switch (action.type) {
    case 'NEXT_STAGE':
      return {
        ...state,
        currentStage: state.currentStage + 1,
        points: state.points + action.payload,
      };
    case 'RESET_GAME':
      return {
        ...state,
        currentStage: 1,
        points: 0,
      };
    case 'TOGGLE_SOUND':
      return {
        ...state,
        soundEnabled: !state.soundEnabled,
      };
    case 'SET_LANGUAGE':
      return {
        ...state,
        language: action.payload,
      };
    default:
      return state;
  }
}

export function GameProvider({ children }) {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  return (
    <GameContext.Provider value={{ state, dispatch }}>
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
} 