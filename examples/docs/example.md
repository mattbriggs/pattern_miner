The finance team manages hundreds of Excel files.  
Context: This causes version-control nightmares.

Problem: Analysts waste hours reconciling differing figures.

Forces: Tight reporting deadlines, limited engineering budget,
need for auditability.

Solution: Move raw data to a single source of truth in a
PostgreSQL warehouse and generate dashboards via Metabase.