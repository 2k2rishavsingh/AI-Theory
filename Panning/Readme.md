# Module-3: Planning Placement Strategy using GraphPlan and POP

Formulate a multi-week placement preparation plan as an automated planning problem with
actions such as DSAPractice, MockInterview, ResumeOptimization, CompanyResearch.
Implement both GraphPlan and POP to generate structured preparation plans: GraphPlan,
POP. Submit the plan outputs and explain why POP offers better real-world adaptability
or vice versa.

This module has 2 dataset files - **plots.csv** and **constraints.json**
## **plots.csv:-**
Defines the agricultural land divided into individual plots and marks which ones are high-risk 
based on pest/moisture conditions.

columns:
**plot** -> Plot Number (P1, P2, …, P50). 
**high_risk** -> Binary flag (1 = plot requires attention, 0 = normal).

## **constraints.json:-**
Contains all fixed constraints required by the planning system, including: 
**A. Action Durations**
Defines the time requirements for tasks such as: 
• CheckMoisture 
• CheckPest 
• Irrigate 
• Spray 
**B. Resource Constraints**
Includes system-wide resources such as: 
• Daily irrigation water quota 
• Drone & AGV vehicle availability 
• Battery capacity per drone 
• Number of days available 
These constraints guide the GraphPlan algorithm to produce feasible plans that respect real
world limits.

## **GraphPlan.ipynb**
**Code Overview**  
The entire workflow is implemented in GraphPlan.ipynb, containing 6 cells. Each cell 
performs a specific part of the planning pipeline. 
**Cell 1 — Load Dataset & Constraints** 
Purpose: 
• Load plots.csv into a dataframe. 
• Load constraints.json. 
• Extract lists of plots, high-risk plots, durations, and resource quotas. 
This sets up the data foundation for the planner. 
**Cell 2 — Action Definitions** 
Purpose: 
Defines all possible actions and their preconditions and effects. 
Examples: 
• CheckMoisture(plot) 
• CheckPest(plot) 
• Irrigate(plot) 
• Spray(plot) 
Each action uses: 
• Constraints from the JSON file 
• Plot-specific information from the CSV file 
This cell constructs the action schema required by GraphPlan. 
**Cell 3 — Goal State Definition** 
Purpose: 
Defines what conditions must be satisfied by the planner. 
Examples: 
• All high-risk plots must be checked or treated. 
• All required resources must remain within limits. 
This becomes the target state the GraphPlan algorithm will try to achieve. 
**Cell 4 — GraphPlan Algorithm Implementation** 
Purpose: 
Implements the classical GraphPlan algorithm, including: 
• Propositional level construction 
• Action level construction 
• Mutex propagation 
• Goal layer checking 
• Backtracking to extract a valid plan 
This is the core reasoning engine of the system. 
**Cell 5 — Visualizing the Planning Graph** 
Purpose: 
Generates a visualization of: 
• Propositional levels 
• Action levels 
• Mutex relationships 
Visualization helps understand how actions propagate effects through levels. 
**Cell 6 — Visualizing Final Plan** 
Purpose: 
Displays the final schedule/plan produced by the GraphPlan algorithm. 
Common formats: 
• Step-by-step action sequences 
• Gantt-like plotting 
• Timeline visualization 
This cell makes the plan interpretable for end-users or evaluators.

**3. Partial Order Planning:**
**3.1 Code Overview** 
**Cell 1 — Load Dataset & Constraints** 
Purpose: 
Loads all required data for planning. 
Functions: 
• Load Plot.CSV → list of plots + high-risk plots 
• Load constraints.json → durations, vehicles, water quota, battery limit, days 
• Compute daily & weekly available water 
Outcome: 
Environment and resource limits become available for the POP planner. 
**Cell 2 — Action Definitions** 
Purpose: 
Defines STRIPS-like action templates for each day. 
Actions created per plot: 
• CheckMoisture 
• Irrigate 
• CheckPest 
• Spray 
• ScheduleNextCycle (meta-action) 
Each action includes: 
preconditions, add effects, delete effects, duration, water use, and vehicle-validity. 
Outcome: 
Full action library for a given day. 
**Cell 3 — Goal Creation (Start / Finish Setup)** 
Purpose: 
Defines what must be achieved on each day. 
Goals include: 
• {plot}_D{day}_Irrigated (for high-risk plots) 
• {plot}_D{day}_Sprayed 
• NextCycleScheduled 
Creates: 
• Start action → initial facts 
• Finish action → requires all goals 
Outcome: 
POP gets its initial open-goal list. 
**Cell 4 — POP Plan Data Structure** 
Purpose: 
Stores the partial-order plan. 
Includes: 
• List of actions 
• Ordering constraints (A → B) 
• Causal links (A produces fact for B) 
Outcome: 
Internal structure the POP algorithm manipulates. 
**Cell 5 — POP Algorithm**
Purpose: 
Backward-chaining partial-order planner. 
Main steps: 
1. Pick an open goal. 
2. Find or create an action that produces it. 
3. Link producer → consumer (causal link). 
4. Add ordering constraints. 
5. Add new preconditions to open goals. 
6. Resolve threats using promotion/demotion. 
Includes resource checks: 
• Action duration ≤ battery capacity 
• Action water use ≤ remaining daily quota 
Outcome: 
Produces a valid partial-order plan for that day (if possible). 
**Cell 6 — Daily/Weekly Planning Loop** 
Purpose: 
Runs POP for each day of the week. 
Tracks: 
• Remaining weekly water 
• Daily water allocation 
• Success/failure of POP plan for each day 
Prints the daily POP plan if successful. 
Outcome: 
Weekly POP schedule with constraints applied. 
**Cell 7 — POP Visualization**
Purpose: 
Draws the POP plan as a graph: 
• Actions = nodes 
• Orderings = solid edges 
• Causal links = dashed edges 
Outcome: 
Easy-to-understand visual explanation of the produced POP schedule.
