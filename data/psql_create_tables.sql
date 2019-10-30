/* psql -U <username> <database> < data/psql_create_tables.sql  
# used DECIMAL(10,6) for x/y and lon/lat, because that is accurate to 11.1 cm
# https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude */


CREATE TABLE bicycle_count (
    X DECIMAL(10,6) NOT NULL,
    Y DECIMAL(10,6) NOT NULL,
    ObjectID INT,
    RecordNum SERIAL NOT NULL PRIMARY KEY,
    SETDate TIMESTAMP (3) WITH TIME ZONE NOT NULL,
    SETYear INT,
    Comments TEXT,
    MCD BIGINT,
    Route TEXT,
    Road TEXT,
    CntDir VARCHAR(5),
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
    Updated TIMESTAMP (3) WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
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