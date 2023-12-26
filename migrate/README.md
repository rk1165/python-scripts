# Migrating data from one AWS region to other

- This project can be used for migrating data from ES cluster in one region to another:
  - `daily_counts.py` gets the total count in ES between two dates in **from** cluster.
  - `scraper.py` finds the unique ids associated with those documents and inserts them in a sqlite DB
  - `writer.py` moves those documents from current ES cluster to S3 or other ES cluster.