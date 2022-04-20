ALTER TABLE tsq_ticket ADD status_update DATE DEFAULT CURRENT_DATE;
UPDATE tsq_ticket SET status_update = CURRENT_DATE;
