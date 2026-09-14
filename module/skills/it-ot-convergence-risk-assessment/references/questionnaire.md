# Questionnaire: Convergence Risk Assessment Input

Answer per proposed data path. Answers without specifics are returned for completion.

## Architecture

1. What data does the project move, in what direction, and at what frequency?
2. Where does the data land: enterprise data center, cloud region, SaaS platform?
3. What latency does the use case tolerate? Real-time control data or reporting data?
4. Does the platform need to send anything back into OT? Commands, configuration, or model updates?
5. Which OT systems are the sources? Name zones from the zone design.

## Platform

6. Who operates the destination platform? Internal team, cloud provider, or SaaS vendor?
7. Where is the platform geographically hosted, and under which jurisdiction?
8. What authentication protects the platform's access path?
9. Does the vendor or platform have any existing connectivity into OT?

## Data

10. Does the data contain credentials, topology details, or alarm logic worth protecting?
11. What is the data classification per the zone consequence statement?
12. Is the data derivable from other sources, or unique to OT?

## Operations

13. Who operates the path after go-live? IT, OT, or the vendor?
14. What happens to the process if the path fails?
15. What is the project timeline, and does it overlap a production freeze?

## IoT Specific

16. For sensor projects: who manufactures the sensors and what firmware update mechanism exists?
17. Do sensors authenticate to the network and to their collector?
18. What is the sensor failure behavior in the process?

