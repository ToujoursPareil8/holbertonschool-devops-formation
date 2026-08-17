## Merge Conflict Solved :

In the config.yml file line 3 caused a conflict because it received two conflicting values for the same line :
`version : 1.1.0` was the value that conflicted with `version : 2.0.0 ` which was the requirement.
Git could automatically merge `featute_dark_mode` and `replicas` because the changes did not overlap with these lines.