PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS region (
    region_id TEXT PRIMARY KEY,
    region_name TEXT NOT NULL UNIQUE,
    region_type TEXT NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS parent_company (
    parent_company_id TEXT PRIMARY KEY,
    parent_company_name TEXT NOT NULL UNIQUE,
    country TEXT,
    website TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS owner (
    owner_id TEXT PRIMARY KEY,
    owner_name TEXT NOT NULL UNIQUE,
    parent_company_id TEXT,
    country TEXT,
    website TEXT,
    notes TEXT,
    FOREIGN KEY(parent_company_id) REFERENCES parent_company(parent_company_id)
);

CREATE TABLE IF NOT EXISTS distillery (
    distillery_id TEXT PRIMARY KEY,
    official_name TEXT NOT NULL,
    preferred_name TEXT,
    region_id TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('Malt','Grain','Malt & Grain','Unknown')),
    status TEXT NOT NULL CHECK(status IN ('Operating','Silent','Mothballed','Under Construction','Planned','Closed','Unknown')),
    founded_year INTEGER,
    owner_id TEXT,
    parent_company_id TEXT,
    website TEXT,
    address TEXT,
    postcode TEXT,
    latitude REAL,
    longitude REAL,
    notes TEXT,
    FOREIGN KEY(region_id) REFERENCES region(region_id),
    FOREIGN KEY(owner_id) REFERENCES owner(owner_id),
    FOREIGN KEY(parent_company_id) REFERENCES parent_company(parent_company_id)
);

CREATE TABLE IF NOT EXISTS brand (
    brand_id TEXT PRIMARY KEY,
    distillery_id TEXT NOT NULL,
    brand_name TEXT NOT NULL,
    brand_type TEXT NOT NULL DEFAULT 'Brand',
    status TEXT NOT NULL DEFAULT 'Active',
    website TEXT,
    notes TEXT,
    FOREIGN KEY(distillery_id) REFERENCES distillery(distillery_id)
);

CREATE TABLE IF NOT EXISTS source (
    source_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    authority TEXT NOT NULL,
    title TEXT,
    url TEXT,
    reliability TEXT,
    last_checked TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS evidence (
    evidence_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    field_name TEXT NOT NULL,
    field_value TEXT,
    source_id TEXT NOT NULL,
    confidence INTEGER NOT NULL CHECK(confidence BETWEEN 1 AND 5),
    verified_date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY(source_id) REFERENCES source(source_id)
);
