CREATE DATABASE biomio_db;
CREATE USER 'biomio_admin'@'localhost' IDENTIFIED BY 'gate';
GRANT ALL PRIVILEGES ON biomio_db . * TO 'biomio_admin'@'localhost';

CREATE USER 'biomio_admin'@'%' IDENTIFIED BY 'gate';
GRANT ALL PRIVILEGES ON * . * TO 'biomio_admin'@'%';

update Profiles
left join Emails on Emails.profileId=Profiles.id and Emails.`primary`=TRUE
set Profiles.name = Emails.email;

ALTER TABLE UserInfo ADD middleName VARCHAR(30);
ALTER TABLE UserInfo ADD honorificPrefix VARCHAR(10);
ALTER TABLE UserInfo ADD honorificSuffix VARCHAR(10);
ALTER TABLE UserInfo ADD formatted VARCHAR(128);
ALTER TABLE Profiles ADD externalId VARCHAR(128);

CREATE TABLE WebResourceUsers (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `userId` INT(11) NOT NULL,
  `webResourceId` INT(11) NOT NULL,
  `created` DATETIME,
  `lastModified` DATETIME,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`userId`) REFERENCES Profiles(`id`),
  FOREIGN KEY (`webResourceId`) REFERENCES WebResources(`id`)
);

ALTER TABLE Policies ADD body TEXT;

CREATE TABLE WebResourcePolicies (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `policiesId` INT(11) NOT NULL,
  `webResourceId` INT(11) NOT NULL,
  `created` DATETIME,
  `lastModified` DATETIME,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`policiesId`) REFERENCES Policies(`id`),
  FOREIGN KEY (`webResourceId`) REFERENCES WebResources(`id`)
)