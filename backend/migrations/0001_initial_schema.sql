-- Initial schema bootstrap for ComplyEdge.
-- This file is provided for controlled environments that require explicit SQL migration artifacts.
-- For local development, FastAPI startup currently executes metadata create_all.

CREATE TABLE IF NOT EXISTS tenants (
  id VARCHAR(36) PRIMARY KEY,
  legal_name VARCHAR(255) NOT NULL,
  primary_contact_email VARCHAR(255) NOT NULL UNIQUE,
  onboarding_status VARCHAR(50) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY,
  tenant_id VARCHAR(36) NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  email VARCHAR(255) NOT NULL UNIQUE,
  full_name VARCHAR(255) NOT NULL,
  role_id VARCHAR(36) NOT NULL REFERENCES roles(id),
  is_active BOOLEAN NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
