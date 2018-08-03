-- Create the tables for Amazeriffic:

-- an entity for the object taskTypes:
CREATE TABLE taskTypes (
  taskTypeId int(11) NOT NULL AUTO_INCREMENT,
  description varchar(100) DEFAULT NULL,
  CUDDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CUDAction int,
  PRIMARY KEY (tasktypeId)
);

-- an entity for the object tag:
CREATE TABLE tags (
  tagId int(11) NOT NULL AUTO_INCREMENT,
  tagName varchar(100) NOT NULL,
  CUDDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CUDAction int,
  PRIMARY KEY (tagId)
);

-- a relationship table :
CREATE TABLE tasks (
  taskTypeId int(11) DEFAULT NULL,
  tagId int(11) DEFAULT NULL,
  userId int,
  CUDDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CUDAction int,
  KEY taskTypeId (taskTypeId),
  KEY tagId (tagId),
  CONSTRAINT tasks_ibfk_1 FOREIGN KEY (taskTypeId) REFERENCES taskTypes (taskTypeId),
  CONSTRAINT tasks_ibfk_2 FOREIGN KEY (tagId) REFERENCES tags (tagId)
);
