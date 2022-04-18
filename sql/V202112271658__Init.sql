DROP TABLE IF EXISTS tsq_ticket_parent;

DROP TABLE IF EXISTS tsq_ticket;
DROP TABLE IF EXISTS tsq_ticket_label;
DROP TABLE IF EXISTS tsq_ticket_status;

DROP TABLE IF EXISTS tsq_user;
DROP TABLE IF EXISTS tsq_account;

DROP TABLE IF EXISTS tsq_project;
DROP TABLE IF EXISTS tsq_organization;

DROP TABLE IF EXISTS tsq_content;

CREATE TABLE tsq_content (
  id SERIAL PRIMARY KEY,
  title TEXT,
  content TEXT
);

CREATE TABLE tsq_ticket_status (
  id SERIAL PRIMARY KEY,
  content_id INT REFERENCES tsq_content(id)
);

INSERT INTO tsq_content(title, content) VALUES('Pending', 'The task is currently in progress.');
INSERT INTO tsq_ticket_status(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Pending';
INSERT INTO tsq_content(title, content) VALUES('Done', 'The task has been completed.');
INSERT INTO tsq_ticket_status(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Done';
INSERT INTO tsq_content(title, content) VALUES('Not Started', 'The task has not been started.');
INSERT INTO tsq_ticket_status(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Not Started';

CREATE TABLE tsq_ticket_label (
  id SERIAL PRIMARY KEY,
  content_id INT REFERENCES tsq_content(id)
);

INSERT INTO tsq_content(title, content) VALUES('Milestone', 'A set of epics that form a cohesive release.');
INSERT INTO tsq_ticket_label(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Milestone';
INSERT INTO tsq_content(title, content) VALUES('Epic', 'A set of features that achieve a specific goal.');
INSERT INTO tsq_ticket_label(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Epic';
INSERT INTO tsq_content(title, content) VALUES('Feature', 'A set of stories that describe a piece of functionality.');
INSERT INTO tsq_ticket_label(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Feature';
INSERT INTO tsq_content(title, content) VALUES('Story', 'A set of tasks to accomplish a small piece of work.');
INSERT INTO tsq_ticket_label(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Story';
INSERT INTO tsq_content(title, content) VALUES('Task', 'An atomic piece of work to complete a story or task.');
INSERT INTO tsq_ticket_label(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Task';
INSERT INTO tsq_content(title, content) VALUES('Template', 'A template.');
INSERT INTO tsq_ticket_label(content_id) SELECT id as content_id FROM tsq_content WHERE tsq_content.title = 'Template';

CREATE TABLE tsq_organization (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL
);

INSERT INTO tsq_organization(title) VALUES('Eek! Labs');

CREATE TABLE tsq_project (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  organization_id INT REFERENCES tsq_organization(id)
);

INSERT INTO tsq_project(title, organization_id) SELECT 'ItsyRealm' as title, id as organization_id FROM tsq_organization where tsq_organization.title = 'Eek! Labs';

CREATE TABLE tsq_ticket (
  id SERIAL PRIMARY KEY,
  content_id INT REFERENCES tsq_content(id),
  status_id INT REFERENCES tsq_ticket_status(id),
  label_id INT REFERENCES tsq_ticket_label(id),
  project_id INT REFERENCES tsq_project(id),
  points INT NOT NULL DEFAULT 0
);

CREATE TABLE tsq_ticket_parent (
  parent_id INT REFERENCES tsq_content(id) NOT NULL,
  child_id INT REFERENCES tsq_content(id) NOT NULL,

  PRIMARY KEY(parent_id, child_id),
  UNIQUE(parent_id, child_id)
);

CREATE TABLE tsq_account (
  id SERIAL PRIMARY KEY,
  username VARCHAR(16) NOT NULL UNIQUE,
  email VARCHAR(254) NOT NULL UNIQUE, -- Email max length is 254 characters
  organization_id INT REFERENCES tsq_organization(id),
  password_hash TEXT NOT NULL
);

CREATE TABLE tsq_user (
  id INT PRIMARY KEY REFERENCES tsq_account(id),
  name TEXT NOT NULL
);
