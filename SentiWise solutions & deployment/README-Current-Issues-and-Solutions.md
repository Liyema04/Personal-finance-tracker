# SentiWise: Addressing Gaps in Personal Finance Trackers
## Project Overview
SentiWise is an innovative personal finance tracker designed specifically for South African students and young adults, focusing on the behavioral and emotional aspects of money management.

### Identified Market Gaps & Proposed Solutions
1. Overwhelming Complexity in Existing Apps
Problem: Most finance apps bombard users with complex charts, financial jargon, and overwhelming features that discourage beginners.
SentiWise Solution: Implement a "beginner mode" with plain-language explanations and a simplified UI that focuses on daily spending guidance.

2. Lack of South African Context
Problem: International apps ignore SA-specific financial challenges.
SentiWise Solution:

- Localized expense categories (e.g., "Data Bundles", "Airtime", "EZWallet", "Load Shedding Essentials")

- Support for informal income tracking (side hustles, gig economy)

- Contextual insights based on local economic factors

3. Poor Habit Formation
Problem: Most trackers only record data without helping users change financial behaviors.
SentiWise Solution: Gamification elements, savings challenges, and behavioral nudges that reward positive financial habits.

4. Youth Financial Stress Ignored
Problem: Apps don't address unique stressors faced by SA youth.
SentiWise Solution:

- Financial "mood tracking" to correlate spending with emotional states

- "Stress meter" to identify financial anxiety triggers

- Integration with local financial wellness resources

5. Manual Entry Fatigue
Problem: Users abandon apps due to tedious data entry requirements.
SentiWise Solution: Explore SMS/WhatsApp scraping (with explicit user consent) to automatically capture transactions from major SA banks.

### Technical Implementation Strategy
- Frontend: Vue.js/React with PWA capabilities for offline functionality during load shedding

- Backend: Django with PostgreSQL

- Bank Integration: Stitch API for secure bank connections

- Deployment: Heroku or comparable platform with SA presence

### Target Audience Validation
Before development, validate assumptions with:

- Instagram/WhatsApp polls targeting SA students

- Minimal viable product (MVP) testing with screenshots/prototypes

- Focus groups on financial pain points
