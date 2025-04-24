# Streak Tracking

## User-Facing

The dashboard shows streak tracking for three social media platforms:
- TikTok (pink)
- Twitter (blue)
- Reddit (orange)

For each platform, the dashboard displays:

1. Daily Activity Grid
   - Shows the last 30 days
   - Each day is represented by a small square
   - Colored squares indicate days with posts
   - Gray squares indicate days without posts

2. Streak Statistics
   - Current streak count
   - Longest streak achieved

3. Progress Bars (when goals are set)
   - Streak Progress: Shows progress towards day-based streak goals
   - Milestone Progress: Shows total posts against the milestone goal

### "Don't Miss Twice" Rule
The streak tracking implements a forgiving "don't miss twice" rule:
- A single missed day doesn't break your streak
- Two consecutive missed days will break the streak
- The missed day isn't counted in the streak length

Examples:
- `XX-XXX` (where X=post, -=gap): Counts as a 5-day streak
- `X--XX` (where X=post, -=gap): Counts as a 2-day streak (double gap breaks it)

## Tech

### Implementation Details

1. Streak Calculation (`cms/utils/streaks.py`)
   - Uses a gap counter to track consecutive missed days
   - Resets gap counter when content is found
   - Breaks streak only on 2+ consecutive gaps
   - Tracks both current and longest streaks
   - Handles ongoing streaks properly

2. Goal Types
   - Day-based: Track posting streaks
   - Week-based: Track posts per week
   - Month-based: Track posts per month

3. Progress Tracking
   - Streak Progress: Current streak vs streak goal
   - Milestone Progress: Total posts vs milestone goal

4. Data Structure
   ```python
   {
       'current_streak': int,  # Current streak length
       'longest_streak': int,  # Longest streak achieved
       'goal_status': {
           'has_goal': bool,
           'goal_type': str,  # 'none', 'day_based', 'week_based', 'month_based'
           'progress': int,
           'target': int,
           'is_achieved': bool
       },
       'milestone_status': {
           'has_goal': bool,
           'progress': int,    # Total posts in period
           'target': int,      # Milestone goal
           'is_achieved': bool
       }
   }
   ```

### Visual Components

1. Progress Bars
   - Uses Tailwind CSS for styling
   - Platform-specific colors
   - Responsive width based on progress percentage
   - Overflow protection to prevent bar expansion

2. Daily Grid
   - Fixed-size squares (w-6 h-6)
   - Platform-specific colors for active days
   - Gray background for inactive days
   - Small date indicator in each square