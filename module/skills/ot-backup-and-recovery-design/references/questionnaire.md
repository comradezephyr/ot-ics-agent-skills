# Questionnaire: Backup and Recovery Design Input

Answer per asset class. Answers without specifics are returned for completion.

## Process Tolerance

1. How long can the process run without each function: control, supervision, historian, engineering?
2. What is the cost of an hour of downtime per production line, in operations terms?
3. Which functions have manual fallbacks and which do not?

## Current State

4. What is backed up today per asset class? Mechanism and frequency.
5. Where does each backup live? Production network, dedicated network, media.
6. When was each class last restored successfully? Record the evidence.
7. Are project files captured together with compiled logic per controller?

## Constraints

8. What spare controllers, HMIs, and licenses exist for restore testing?
9. What budget envelope applies to backup infrastructure this cycle?
10. Who owns backup operations today, and do they own the restore too?
11. What are the works-council or data constraints on offsite copies?

## Ransomware Context

12. What did the last assessment say about backup reachability from the production network?
13. Is there a media or vault process with named custody today?
14. What is the maximum acceptable data loss for the historian, in hours?

