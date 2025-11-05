# Cricket Engine Migration Status

## Overview
Migration of game logic from frontend (match.html JavaScript) to backend (cricket_engine.py + routes.py) is **partially complete**.

---

## ✅ **COMPLETED (Backend Migrated)**

### 1. **Delivery Simulation** ✅
- **Location**: `routes.py:simulate_delivery()` and `cricket_engine.py:simulate_delivery()`
- **Status**: Fully migrated
- **What works**:
  - Calls `engine.simulate_delivery()` with player IDs
  - Uses `simengine.events.delivery()` for actual simulation
  - Returns `DeliveryResult` object
  - Saves to database (`Delivery` table)
  - Emits WebSocket `delivery_update` event
  - Updates innings state (runs, wickets, overs)

### 2. **Engine Initialization** ✅
- **Location**: `routes.py:start_match()` and `cricket_engine.py:__init__()`
- **Status**: Fully migrated
- **What works**:
  - Creates `CricketGameEngine` instance per match
  - Stores in `active_engines` dict
  - Initializes first innings via `engine.start_first_innings()`
  - Sets location adjustments

### 3. **Basic State Management** ✅
- **Location**: `cricket_engine.py:update_match_state()`, `get_match_state()`
- **Status**: Partially migrated (structure exists but not fully utilized)
- **What works**:
  - Tracks runs, wickets, balls faced
  - Updates partnership runs
  - Tracks current over/ball

---

## ⚠️ **PARTIALLY MIGRATED (Needs Completion)**

### 4. **Stats Tracking (Batting/Bowling)** ⚠️
- **Frontend**: `match.html` has `ScorecardManager`, `BattingScore`, `BowlingFigures` classes
- **Backend**: Database models exist (`BattingStats`, `BowlingStats`) but **NOT being updated**
- **Gap**: 
  - Backend saves `Delivery` records but doesn't update `BattingStats`/`BowlingStats` tables
  - Frontend still calculates all stats client-side
  - No API endpoint to fetch aggregated stats from backend

### 5. **Match State Tracking** ⚠️
- **Frontend**: `matchState` object tracks everything (current players, scores, overs, etc.)
- **Backend**: Basic state exists in engine but not persisted/retrieved properly
- **Gap**:
  - Frontend maintains its own `matchState` separately from backend
  - No API to sync/get current match state from backend
  - `get_match_state()` endpoint exists but not used by frontend

### 6. **Innings Management** ⚠️
- **Backend**: `start_first_innings()` and `start_second_innings()` methods exist
- **Gap**: 
  - Not fully integrated with database `Innings` model
  - Second innings transition not handled in routes
  - Frontend handles innings switching independently

---

## ❌ **NOT MIGRATED (Still Frontend Only)**

### 7. **Player Selection** ❌
- **Location**: `match.html` functions: `selectOpeningPlayers()`, `selectNewBatsman()`, `selectNewBowler()`
- **Status**: Still fully frontend
- **What's missing**:
  - Backend has `get_available_bowlers()` and `get_available_batsmen()` methods in `cricket_engine.py`
  - But no API endpoints to expose these
  - Frontend calculates available players client-side

### 8. **Over Completion Logic** ❌
- **Location**: `match.html:completeOver()`
- **Status**: Frontend only
- **What's missing**:
  - No backend tracking of over completion
  - Frontend manually clears balls display and swaps strike

### 9. **Run Rate Calculations** ❌
- **Location**: `match.html:updateScoreAfterDelivery()`
- **Status**: Frontend only
- **What's missing**:
  - All run rate, required run rate, projected score calculations in frontend
  - Should be backend-calculated and sent via WebSocket

### 10. **Innings Completion Detection** ❌
- **Location**: `match.html:checkInningsCompletion()`, `endInnings()`
- **Status**: Frontend only
- **What's missing**:
  - `cricket_engine.py:is_innings_complete()` method exists but not called
  - Frontend checks overs/wickets manually
  - No backend validation or WebSocket event for innings completion

### 11. **Strike Swapping** ❌
- **Location**: `match.html:swapStrike()`
- **Status**: Frontend only
- **What's missing**:
  - Should be handled automatically by backend after deliveries
  - Backend knows runs scored but doesn't update striker/non-striker positions

### 12. **Target Calculation** ❌
- **Location**: `match.html:endInnings()`, `startSecondInnings()`
- **Status**: Frontend only
- **What's missing**:
  - Target calculation happens in frontend
  - No backend method to start second innings and set target

---

## 🔍 **SPECIFIC MIGRATION GAPS IDENTIFIED**

### **Critical Issues:**

1. **Stats Not Being Updated in Backend**
   - In `routes.py:simulate_delivery()`, after creating `Delivery` record, code should also update:
     - `BattingStats` for striker (runs, balls, 4s, 6s, etc.)
     - `BowlingStats` for bowler (runs conceded, wickets, deliveries, etc.)
   - Currently these tables are never updated after match starts

2. **Match State Desynchronization**
   - Frontend `matchState` and backend `engine` state are separate
   - Frontend still maintains: `totalRuns`, `wicketsLost`, `currentBalls`, `ballsFaced`
   - Should rely entirely on backend state from WebSocket events

3. **Missing API Endpoints:**
   - `GET /api/matches/<match_id>/available-bowlers` (uses `get_available_bowlers()`)
   - `GET /api/matches/<match_id>/available-batsmen` (uses `get_available_batsmen()`)
   - `GET /api/matches/<match_id>/scorecard` (returns aggregated stats)
   - `POST /api/matches/<match_id>/end-innings` (handle innings transition)
   - `POST /api/matches/<match_id>/select-players` (persist player selections)

4. **Incomplete WebSocket Events:**
   - Missing `innings_complete` WebSocket event emission (handler exists in frontend)
   - Missing `match_complete` WebSocket event emission
   - `delivery_update` doesn't include calculated run rates, required run rates

5. **Player Selection Not Persisted:**
   - When users select opening players or new batsmen/bowlers, this isn't saved to database
   - `Innings` model has `striker_id`, `non_striker_id` fields but they're not being set

---

## 📋 **RECOMMENDED NEXT STEPS (In Priority Order)**

1. **HIGH PRIORITY: Update Stats in Backend**
   - Modify `simulate_delivery()` in `routes.py` to update `BattingStats` and `BowlingStats`
   - This is critical for accurate scorecards

2. **HIGH PRIORITY: Enhance WebSocket Events**
   - Add run rates, required run rates to `delivery_update` event
   - Emit `innings_complete` event when detected
   - Frontend can then remove its calculation logic

3. **MEDIUM PRIORITY: Create Player Selection APIs**
   - Add endpoints for getting available players
   - Persist player selections to database (`Innings.striker_id`, etc.)

4. **MEDIUM PRIORITY: Match State Synchronization**
   - Make frontend rely entirely on WebSocket events
   - Remove redundant `matchState` tracking where backend already tracks

5. **LOW PRIORITY: Innings Transition**
   - Complete `endInnings()` and `startSecondInnings()` backend logic
   - Create proper API endpoint for innings transition

---

## 🐛 **KNOWN ISSUES**

1. **`apply_location_adjustments()` Bug in `cricket_engine.py`**
   - Line 169: Method expects dict but gets string
   - Should return dict, not call `self.game.set_location()`
   - Currently broken and will cause errors

2. **Frontend Fallback to Mock Data**
   - `simulateDelivery()` in `match.html` still has fallback to `generateMockDelivery()`
   - Should be removed once backend is fully reliable

3. **Incomplete `is_innings_complete()` Method**
   - In `cricket_engine.py:374`, method signature exists but logic incomplete
   - Missing target check for second innings
