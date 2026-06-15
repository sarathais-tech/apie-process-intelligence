CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE events (
    id UUID PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    source VARCHAR(100) NOT NULL,
    user_id VARCHAR(120),
    session_id VARCHAR(120),
    process_name VARCHAR(255),
    window_title TEXT,
    activity VARCHAR(255),
    event_metadata JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE processes (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'discovered',
    confidence_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE process_steps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    process_id UUID NOT NULL REFERENCES processes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    "order" INTEGER NOT NULL,
    application VARCHAR(255),
    step_metadata JSONB NOT NULL DEFAULT '{}'
);
