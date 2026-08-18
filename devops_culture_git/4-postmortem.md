## Task 4 : When prod breaks: chase the cause, not the culprit

### Timeline

**Friday 5:40pm**: A fix requested by the marketing team is made for deployment to the prod server.

**Friday 5:52pm (Occured)**: The config file is edited on the prod server. A syntax error is introduced to the database URL = breaks the checkout process.

**Friday 8:30pm (Deteected by users)**: Customer report the checkout failure on social media. Team is unaware because no automated alerting.

**Saturday 9.15 am (Detected by team)**: Discovery of the customer complaints.

**Saturday 11.40 am (Resolved)**: After identifying the cause of the bug, the file is fixed by hand, service restored after 15hours of downtime.

### Systemic causes

Manual deployment Process: this process bypasses version control
Lack of Environment Parity: No staging or test environment, changes are validated locally. Making it impossible to catch errors before release
Zero Observability: No automated monitoring and alerting for critical business paths. The detection relies entirely on customer complaints.
Access and Knowledge Silos: Deployment knowledge and server access are centralizes. When issues occur out of work hours, nobody had access to what was required to investigate what had changed.
No Rollback Mechanism: because the deployment is manual and undocumented, there is no way to quickly revert the system. 

### 3 Priority actions & DORA metrics degraded

**Action 1 : Implement an Automated CI/CD pipeline**

Justification : Stop all manual SSH deployments and direct config audits. Everything must be committed to version control and deployed via an automated pipeline.
Degraded DORA metric : Change Failure Rate and lead time changes.

**Action 2 : Set up synthetic Monitoring and automated alerting**

Justification : The dev team must be the first to know when a critical path goes down. They need to implement monitoring then automated monitoring and automated alerting.
Problem adressed : Relying on customers to detect outages.
Degraded DORA metric : MTTR3

**Action 3 : Establish an automated Rollback strategy**

Justification : The priority is to restore service, not fixing the bug, when a deployement breaks production. With version control any dev can revert back to a functionning version at the press of a button.
Problem adressed : acces silos and the inability to quickly revert bad changes without the original author.
Degrade DORA metric: MTTR
