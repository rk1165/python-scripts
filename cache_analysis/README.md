### Cache Hit Analysis

- This analysis was done to ascertain what must be the optimum TTL for ElastiCache based on different statuses received.

#### Methodology
- For a particular request we receive many status at different time intervals. 
- We calculate the time difference between those statuses timestamps and put them in a bin containing two groups.
- For instance, if we want to check if we should keep the TTL as 30 minutes; we sort the time interval differences between <= 30 minutes and > 30 minutes.
- Then we count the number of events received in less than 30 minutes and calculate the cache hit percentage
- This way we check for multiple intervals : 30, 60, 120, 180, 1440 and 2880 minutes.