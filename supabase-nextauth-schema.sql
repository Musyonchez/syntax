-- NextAuth.js required tables for Supabase
-- Run this in your Supabase SQL Editor

create table if not exists verification_tokens
(
  identifier text not null,
  expires timestamptz not null,
  token text not null,

  primary key (identifier, token)
);

create table if not exists accounts
(
  id uuid default gen_random_uuid() primary key,
  user_id uuid not null,
  type varchar(255) not null,
  provider varchar(255) not null,
  provider_account_id varchar(255) not null,
  refresh_token text,
  access_token text,
  expires_at bigint,
  id_token text,
  scope text,
  session_state text,
  token_type text
);

create table if not exists sessions
(
  id uuid default gen_random_uuid() primary key,
  user_id uuid not null,
  expires timestamptz not null,
  session_token varchar(255) not null unique
);

create table if not exists users
(
  id uuid default gen_random_uuid() primary key,
  name varchar(255),
  email varchar(255) unique,
  email_verified timestamptz,
  image text
);

-- Add foreign key constraints
alter table accounts add constraint fk_accounts_user_id foreign key (user_id) references users(id) on delete cascade;
alter table sessions add constraint fk_sessions_user_id foreign key (user_id) references users(id) on delete cascade;

-- Create indexes for performance
create index if not exists accounts_provider_provider_account_id_idx on accounts(provider, provider_account_id);
create index if not exists sessions_user_id_idx on sessions(user_id);
create index if not exists sessions_session_token_idx on sessions(session_token);