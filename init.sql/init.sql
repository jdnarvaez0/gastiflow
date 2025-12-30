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

-- Users table for authentication and multi-tenancy
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    telegram_id VARCHAR(100) UNIQUE,
    gemini_api_key VARCHAR(255),
    interaction_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    -- Email verification fields
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(255),
    email_verification_sent_at TIMESTAMP WITHOUT TIME ZONE,
    -- Profile fields
    full_name VARCHAR(200),
    profile_picture_url VARCHAR(500),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX IF NOT EXISTS ix_users_id ON users (id);
CREATE INDEX IF NOT EXISTS ix_users_username ON users (username);
CREATE INDEX IF NOT EXISTS ix_users_telegram_id ON users (telegram_id);
