# mysql -u <username> -p dvrpc < data/create_tables.sql  
# used DECIMAL(10,6) for x/y and lon/lat, because that is accurate to 11.1 cm
# https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude


CREATE TABLE bicycle_count (
    X DECIMAL(10,6) NOT NULL,
    Y DECIMAL(10,6) NOT NULL,
    ObjectID INT,
    RecordNum INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    SETDate DATETIME NOT NULL,
    SETYear YEAR,
    Comments TEXT,
    MCD BIGINT,
    Route INT,
    Road TEXT,
    CntDir CHAR(5),
    FromLmt TEXT,
    ToLmt TEXT,
    Type TEXT,
    Latitude DECIMAL(10,6) NOT NULL,
    Longitude DECIMAL(10,6) NOT NULL,
    Factor INT,
    Axle FLOAT,
    OutDir CHAR(1),
    InDir CHAR(1),
    AADB INT,
    Updated DATETIME DEFAULT (CURRENT_TIMESTAMP),
    Co_name TEXT,
    Mun_name TEXT,
    GlobalID TEXT,
    Program TEXT,
    BikePedGro TEXT,
    BikePedFac TEXT
);

CREATE TABLE IF NOT EXISTS weather (
    Station TEXT,
    Name TEXT,
    Date DATE PRIMARY KEY,
    Prcp FLOAT,
    Tavg INT,
    Tmax INT,
    Tmin INT
);