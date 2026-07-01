CREATE TABLE Distillery(
  DistilleryID TEXT PRIMARY KEY,
  OfficialName TEXT NOT NULL,
  RegionID TEXT,
  OwnerID TEXT,
  ParentCompanyID TEXT,
  Status TEXT,
  Founded INTEGER,
  Website TEXT
);
