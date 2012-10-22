"""
_Create_DBSBuffer_

Implementation of Create_DBSBuffer for MySQL.
"""





import logging
import threading

from WMCore.Database.DBCreator import DBCreator

class Create(DBCreator):

    def __init__(self, logger = None, dbi = None, params = None):
        """
        _init_

        Call the base class's constructor and create all necessary tables,
        constraints and inserts.
        """
        myThread = threading.currentThread()
        DBCreator.__init__(self, myThread.logger, myThread.dbi)

        self.create["01dbsbuffer_dataset"] = \
              """CREATE TABLE dbsbuffer_dataset
                        (
                           id           BIGINT UNSIGNED not null auto_increment,
                           path         varchar(500)    unique not null,
                           valid_status VARCHAR(20),
                           global_tag   VARCHAR(255),
                           subscribed int default 0,
                           primary key(id)
                        ) ENGINE=InnoDB"""

        self.create["02dbsbuffer_algo"] = \
              """CREATE TABLE dbsbuffer_algo
                        (
                           id     BIGINT UNSIGNED not null auto_increment,
                           app_name varchar(100),
                           app_ver  varchar(100),
                           app_fam  varchar(100),
                           pset_hash varchar(700),
                           config_content LONGTEXT,
                           in_dbs int,
                           primary key(ID),
                           unique (app_name, app_ver, app_fam, pset_hash)
                        ) ENGINE=InnoDB"""

        self.create["03dbsbuffer_algo_dataset_assoc"] = \
              """CREATE TABLE dbsbuffer_algo_dataset_assoc
                        (
                           id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                           algo_id BIGINT UNSIGNED,
                           dataset_id BIGINT UNSIGNED,
                           in_dbs INTEGER DEFAULT 0,
                           primary key(id),
                           FOREIGN KEY (algo_id) REFERENCES dbsbuffer_algo(id)
                             ON DELETE CASCADE,
                           FOREIGN KEY (dataset_id) REFERENCES dbsbuffer_dataset(id)
                             ON DELETE CASCADE
                        ) ENGINE = InnoDB"""

        self.create["04dbsbuffer_file"] = \
          """CREATE TABLE dbsbuffer_file (
             id           INTEGER      PRIMARY KEY AUTO_INCREMENT,
             lfn          VARCHAR(255) NOT NULL,
             filesize     BIGINT,
             events       INTEGER,
             dataset_algo BIGINT UNSIGNED   not null,
             block_id     BIGINT UNSIGNED,
             status       varchar(20),
             in_phedex    INTEGER DEFAULT 0,
             LastModificationDate  BIGINT,
             UNIQUE(lfn)) ENGINE=InnoDB"""

        self.create["06dbsbuffer_file_parent"] = \
          """CREATE TABLE dbsbuffer_file_parent (
             child  INTEGER NOT NULL,
             parent INTEGER NOT NULL,
             FOREIGN KEY (child)  references dbsbuffer_file(id)
               ON DELETE CASCADE,
             FOREIGN KEY (parent) references dbsbuffer_file(id),
             UNIQUE(child, parent))ENGINE=InnoDB"""

        self.create["07dbsbuffer_file_runlumi_map"] = \
          """CREATE TABLE dbsbuffer_file_runlumi_map (
             filename    INTEGER NOT NULL,
             run         INTEGER NOT NULL,
             lumi        INTEGER NOT NULL,
             FOREIGN KEY (filename) references dbsbuffer_file(id)
               ON DELETE CASCADE)ENGINE=InnoDB"""

        self.create["08dbsbuffer_location"] = \
          """CREATE TABLE dbsbuffer_location (
             id      INTEGER      PRIMARY KEY AUTO_INCREMENT,
             se_name VARCHAR(255) NOT NULL,
             UNIQUE(se_name))ENGINE=InnoDB"""

        self.create["09dbsbuffer_file_location"] = \
          """CREATE TABLE dbsbuffer_file_location (
             filename INTEGER NOT NULL,
             location INTEGER NOT NULL,
             UNIQUE(filename, location)) ENGINE=InnoDB"""

        self.create["10dbsbuffer_block"] = \
          """CREATE TABLE dbsbuffer_block (
             id           INTEGER      PRIMARY KEY AUTO_INCREMENT,
             blockname    VARCHAR(250) NOT NULL,
             location     INTEGER      NOT NULL,
             create_time  INTEGER,
             status       VARCHAR(20),
             UNIQUE(blockname, location))ENGINE=InnoDB"""

        self.create["11dbsbuffer_checksum_type"] = \
          """CREATE TABLE dbsbuffer_checksum_type (
              id            INTEGER      PRIMARY KEY AUTO_INCREMENT,
              type          VARCHAR(255) ) ENGINE=InnoDB"""


        self.create["12dbsbuffer_file_checksums"] = \
          """CREATE TABLE dbsbuffer_file_checksums (
              fileid        INTEGER,
              typeid        INTEGER,
              cksum         VARCHAR(100),
              UNIQUE (fileid, typeid),
              FOREIGN KEY (typeid) REFERENCES dbsbuffer_checksum_type(id)
                ON DELETE CASCADE,
              FOREIGN KEY (fileid) REFERENCES dbsbuffer_file(id)
                ON DELETE CASCADE) ENGINE=InnoDB"""


        checksumTypes = ['cksum', 'adler32', 'md5']
        for i in checksumTypes:
            checksumTypeQuery = """INSERT INTO dbsbuffer_checksum_type (type) VALUES ('%s')
            """ % (i)
            self.inserts["wmbs_checksum_type_%s" % (i)] = checksumTypeQuery
