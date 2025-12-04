# Module-3: Planning Placement Strategy using GraphPlan and POP

Formulate a multi-week placement preparation plan as an automated planning problem with
actions such as DSAPractice, MockInterview, ResumeOptimization, CompanyResearch.
Implement both GraphPlan and POP to generate structured preparation plans: GraphPlan,
POP. Submit the plan outputs and explain why POP offers better real-world adaptability
or vice versa. 

This module has 2 dataset files - **plots.csv** and **constraints.json**<br>
## **plots.csv:-**<br>
Defines the agricultural land divided into individual plots and marks which ones are high-risk 
based on pest/moisture conditions. <br>

columns: <br>
**plot** -> Plot Number (P1, P2, …, P50).  <br>
**high_risk** -> Binary flag (1 = plot requires attention, 0 = normal). <br>

## **constraints.json:-** <br>
Contains all fixed constraints required by the planning system, including: <br>
**A. Action Durations** <br>
Defines the time requirements for tasks such as:  <br>
• CheckMoisture  <br>
• CheckPest  <br>
• Irrigate  <br>
• Spray  <br><br>
**B. Resource Constraints** <br>
Includes system-wide resources such as: <br>
• Daily irrigation water quota <br>
• Drone & AGV vehicle availability <br>
• Battery capacity per drone <br>
• Number of days available <br>
These constraints guide the GraphPlan algorithm to produce feasible plans that respect real
world limits. <br>

## **GraphPlan.ipynb** <br>
### **Code Overview**  <br>
The entire workflow is implemented in GraphPlan.ipynb, containing 6 cells. Each cell
performs a specific part of the planning pipeline. <br><br>
**Cell 1 — Load Dataset & Constraints** <br>
Purpose: <br>
• Load plots.csv into a dataframe. <br>
• Load constraints.json. <br>
• Extract lists of plots, high-risk plots, durations, and resource quotas. <br>
This sets up the data foundation for the planner. <br><br>
**Cell 2 — Action Definitions** <br>
Purpose:<br> 
Defines all possible actions and their preconditions and effects. 
Examples: <br>
• CheckMoisture(plot) 
• CheckPest(plot) 
• Irrigate(plot) 
• Spray(plot) 
Each action uses: <br>
• Constraints from the JSON file 
• Plot-specific information from the CSV file <br>
This cell constructs the action schema required by GraphPlan. <br><br>
**Cell 3 — Goal State Definition** <br>
Purpose: <br>
Defines what conditions must be satisfied by the planner. <br>
Examples: <br>
• All high-risk plots must be checked or treated. 
• All required resources must remain within limits. 
This becomes the target state the GraphPlan algorithm will try to achieve. <br><br>
**Cell 4 — GraphPlan Algorithm Implementation** 
Purpose: <br>
Implements the classical GraphPlan algorithm, including: <br>
• Propositional level construction 
• Action level construction 
• Mutex propagation 
• Goal layer checking 
• Backtracking to extract a valid plan 
This is the core reasoning engine of the system. <br><br>
**Cell 5 — Visualizing the Planning Graph** <br>
Purpose: <br>
Generates a visualization of: <br>
• Propositional levels 
• Action levels 
• Mutex relationships <br>
Visualization helps understand how actions propagate effects through levels. <br><br>
**Cell 6 — Visualizing Final Plan** <br>
Purpose: <br>
Displays the final schedule/plan produced by the GraphPlan algorithm. <br>
Common formats: <br>
• Step-by-step action sequences 
• Gantt-like plotting 
• Timeline visualization <br>
This cell makes the plan interpretable for end-users or evaluators.<br><br>

## **3. Partial Order Planning:** <br>
### **3.1 Code Overview** <br><br>
**Cell 1 — Load Dataset & Constraints** <br>
Purpose: <br>
Loads all required data for planning. <br>
Functions: <br>
• Load Plot.CSV → list of plots + high-risk plots 
• Load constraints.json → durations, vehicles, water quota, battery limit, days 
• Compute daily & weekly available water <br>
Outcome: <br>
Environment and resource limits become available for the POP planner. <br><br>
**Cell 2 — Action Definitions** <br>
Purpose: <br>
Defines STRIPS-like action templates for each day. <br>
Actions created per plot: <br>
• CheckMoisture 
• Irrigate 
• CheckPest 
• Spray 
• ScheduleNextCycle (meta-action) 
Each action includes: <br>
preconditions, add effects, delete effects, duration, water use, and vehicle-validity. <br>
Outcome: <br>
Full action library for a given day. <br><br>
**Cell 3 — Goal Creation (Start / Finish Setup)** <br>
Purpose: <br>
Defines what must be achieved on each day. <br>
Goals include: <br>
• {plot}_D{day}_Irrigated (for high-risk plots) 
• {plot}_D{day}_Sprayed 
• NextCycleScheduled 
Creates: <br>
• Start action → initial facts 
• Finish action → requires all goals 
Outcome: <br>
POP gets its initial open-goal list. <br><br>
**Cell 4 — POP Plan Data Structure** <br>
Purpose: <br>
Stores the partial-order plan. <br>
Includes: <br>
• List of actions 
• Ordering constraints (A → B) 
• Causal links (A produces fact for B) 
Outcome: <br>
Internal structure the POP algorithm manipulates. <br><br>
**Cell 5 — POP Algorithm** <br>
Purpose: <br>
Backward-chaining partial-order planner. <br>
Main steps: <br>
1. Pick an open goal. 
2. Find or create an action that produces it. 
3. Link producer → consumer (causal link). 
4. Add ordering constraints. 
5. Add new preconditions to open goals. 
6. Resolve threats using promotion/demotion. <br>
Includes resource checks: <br>
• Action duration ≤ battery capacity 
• Action water use ≤ remaining daily quota <br>
Outcome: <br>
Produces a valid partial-order plan for that day (if possible). <br><br>

**Cell 6 — Daily/Weekly Planning Loop** <br>
Purpose: <br>
Runs POP for each day of the week. <br>
Tracks: <br>
• Remaining weekly water 
• Daily water allocation 
• Success/failure of POP plan for each day 
Prints the daily POP plan if successful. <br>
Outcome: 
Weekly POP schedule with constraints applied. <br><br>
**Cell 7 — POP Visualization**<br>
Purpose: <br>
Draws the POP plan as a graph: <br>
• Actions = nodes 
• Orderings = solid edges 
• Causal links = dashed edges 
Outcome: <br>
Easy-to-understand visual explanation of the produced POP schedule.<br>
