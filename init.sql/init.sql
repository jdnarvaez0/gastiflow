CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    description VARCHAR(255) NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'ARS',
    category VARCHAR(50) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX IF NOT EXISTS ix_expenses_id ON expenses (id);
CREATE INDEX IF NOT EXISTS ix_expenses_user_id ON expenses (user_id);
