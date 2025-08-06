CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE TASKS (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    project_id UUID,
    isDone BOOLEAN DEFAULT FALSE,
    priority SMALLINT NOT NULL,
    due_date DATE NOT NULL,
    description VARCHAR,
    assigned_to VARCHAR,
    CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES PROJECT (project_id),
    CONSTRAINT fk_assigned_to FOREIGN KEY (assigned_to) REFERENCES users (username)
);

CREATE INDEX idx_tasks_assigned_status_priority_due ON TASKS (assigned_to, isDone, priority, due_date);
CREATE INDEX idx_priority_due_date ON TASKS(priority,due_date);
