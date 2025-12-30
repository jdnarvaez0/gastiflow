-- Migración de Tabla Users v1 -> v2
-- Ejecutar este script en la base de datos de producción (EC2)

ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(255) NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verification_sent_at TIMESTAMP WITHOUT TIME ZONE NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(200) NULL;
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_picture_url VARCHAR(500) NULL;

-- Nota: Si ya existen usuarios, estas columnas se inicializarán en FALSE o NULL.
