CREATE DATABASE biomio_db;
CREATE USER 'biomio_admin'@'localhost' IDENTIFIED BY 'gate';
GRANT ALL PRIVILEGES ON biomio_db . * TO 'biomio_admin'@'localhost';

CREATE USER 'biomio_admin'@'%' IDENTIFIED BY 'gate';
GRANT ALL PRIVILEGES ON * . * TO 'biomio_admin'@'%';

ALTER TABLE Profiles ADD externalId VARCHAR(128);

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
);


ALTER TABLE Profiles MODIFY COLUMN api_id INT DEFAULT 0;
ALTER TABLE Profiles MODIFY COLUMN phones VARCHAR(255) NULL DEFAULT NULL ;
ALTER TABLE Profiles MODIFY COLUMN password VARCHAR(50) NULL DEFAULT NULL ;
ALTER TABLE Profiles MODIFY COLUMN temp_pass VARCHAR(50) NULL DEFAULT NULL ;
ALTER TABLE Profiles MODIFY COLUMN acc_type INT DEFAULT 0;
ALTER TABLE Profiles MODIFY COLUMN last_ip VARCHAR(20) NULL DEFAULT NULL ;


ALTER TABLE UserInfo MODIFY COLUMN voice TINYINT DEFAULT 0;
ALTER TABLE UserInfo MODIFY COLUMN motto VARCHAR(255) NULL DEFAULT NULL ;
ALTER TABLE UserInfo MODIFY COLUMN bday DATE NULL DEFAULT NULL ;
ALTER TABLE UserInfo MODIFY COLUMN occupation VARCHAR(255) NULL DEFAULT NULL ;

CREATE TABLE ProviderJWTKeys (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `ProviderId` INT(11) NOT NULL,
  `private_key` LONGTEXT NOT NULL,
  `public_key` LONGTEXT NOT NULL,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`providerId`) REFERENCES Providers(`id`)
);