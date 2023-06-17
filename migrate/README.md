# Migrating data from one AWS region to other

- This project can be used for migrating data from ES cluster in one region to another:
  - Get the total count in ES between two dates in **from** cluster - `daily_counts.py`
  - Find the unique ids associated with those documents and insert them in a sqlite DB - `scraper.py`
  - Moving those documents from current ES cluster and posting to S3 or other ES cluster - `writer.py`