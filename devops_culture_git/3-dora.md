## Task 3 : How do you know a team is any good? You measure.

**Q1. Match each DORA metric to its definition (deployment frequency, lead time for changes, change failure rate, time to restore / MTTR).**

**Q2. A team deploys once a quarter. Which metric is poor?**

deployment frequency, once a quarter is low frequency, meaning a team of Low performers.

**Q3. You shorten the time between merging a PR and shipping it to production. Which metric improves?**

lead time for changes

**Q4. 1 deployment out of 4 causes an incident. Which metric is this, and is a high value good or bad?**

change failure rate, a high value is bad because it indicates low reliability.

**Q5. What does the acronym CALMS stand for?**

**C**ulture , **A**utomation, **L**ean, **M**easurement, **S**haring

**Q6. True or false: "elite" teams deploy less often but in bigger batches. Justify your answer.**

False, elite teams deploy frequently in smaller batches because it lowers risks. A small change is easier to test, understand and track if there is a bug.

**Q7. Which practice improves MTTR the most?**

(b) monitoring and alerting plus automated rollback


**Q8. Among the 4 DORA metrics, which measure throughput and which measure stability?**

**Throughput**: Deployment frequency, Lead time for changes
**Stability**:Change failure rate, MTTR

**Q9. Why do we run blameless post-mortems?**

We run blameless post-mortems because it raises a risk of an employee hiding a mistake/error instead of reporting it. So instead blameless post-mortems focus on what was the cause instead ou who.