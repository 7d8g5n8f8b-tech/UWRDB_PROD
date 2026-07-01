PRAGMA foreign_keys = ON;

CREATE TABLE region(region_id TEXT PRIMARY KEY, region_name TEXT NOT NULL UNIQUE, region_type TEXT NOT NULL, notes TEXT);
CREATE TABLE parent_company(parent_company_id TEXT PRIMARY KEY, parent_company_name TEXT NOT NULL UNIQUE, country TEXT, website TEXT, notes TEXT);
CREATE TABLE owner(owner_id TEXT PRIMARY KEY, owner_name TEXT NOT NULL UNIQUE, parent_company_id TEXT, country TEXT, website TEXT, notes TEXT, FOREIGN KEY(parent_company_id) REFERENCES parent_company(parent_company_id));

CREATE TABLE field_definition(
  field_name TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  definition TEXT NOT NULL,
  gold_required INTEGER NOT NULL DEFAULT 0,
  notes TEXT
);

CREATE TABLE distillery(
  distillery_id TEXT PRIMARY KEY,
  official_name TEXT NOT NULL,
  preferred_name TEXT,
  region_id TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT NOT NULL,
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

CREATE TABLE brand(
  brand_id TEXT PRIMARY KEY,
  distillery_id TEXT NOT NULL,
  brand_name TEXT NOT NULL,
  brand_type TEXT,
  status TEXT,
  website TEXT,
  notes TEXT,
  FOREIGN KEY(distillery_id) REFERENCES distillery(distillery_id)
);

CREATE TABLE source(
  source_id TEXT PRIMARY KEY,
  source_type TEXT NOT NULL,
  authority TEXT NOT NULL,
  title TEXT,
  url TEXT,
  reliability TEXT,
  last_checked TEXT,
  notes TEXT
);

CREATE TABLE evidence(
  evidence_id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  field_name TEXT NOT NULL,
  field_value TEXT,
  source_id TEXT NOT NULL,
  evidence_strength INTEGER NOT NULL CHECK(evidence_strength BETWEEN 1 AND 5),
  verification_status TEXT NOT NULL CHECK(verification_status IN ('unknown','captured','verified','reviewed','gold')),
  verified_date TEXT NOT NULL,
  notes TEXT,
  FOREIGN KEY(source_id) REFERENCES source(source_id),
  FOREIGN KEY(field_name) REFERENCES field_definition(field_name)
);
