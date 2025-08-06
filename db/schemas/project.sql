CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
 
CREATE TABLE PROJECT (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR NOT NULL,
    description VARCHAR,
    owner VARCHAR,
    isOpen BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_owner FOREIGN KEY (owner) REFERENCES users(username)
);

CREATE INDEX idx_project_owner_status ON PROJECT (owner, isOpen);
