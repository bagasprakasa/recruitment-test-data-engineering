CREATE TABLE IF NOT EXISTS places (
  id INT AUTO_INCREMENT PRIMARY KEY,
  city VARCHAR(100),
  county VARCHAR(100),
  country VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS people (
  id INT AUTO_INCREMENT PRIMARY KEY,
  given_name VARCHAR(100),
  family_name VARCHAR(100),
  date_of_birth DATE,
  place_of_birth VARCHAR(100)
);