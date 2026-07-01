CREATE TABLE Evidence(
  EvidenceID TEXT PRIMARY KEY,
  EntityType TEXT,
  EntityID TEXT,
  FieldName TEXT,
  Value TEXT,
  SourceID TEXT,
  Confidence INTEGER,
  VerifiedDate TEXT
);
