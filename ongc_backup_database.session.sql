INSERT INTO alembic_version (version_num)
VALUES ('version_num:character varyingINSERT INTO alembic_version (version_num)
VALUES ('version_num:character varyingINSERT INTO backup_record (
    id,
    backup_type,
    tape_number,
    backup_date,
    server,
    os,
    backup_contents,
    backup_format,
    remarks,
    tape_reuse_date,
    extra_info,
    backup_frequency
  )
VALUES (
    id:integerINSERT INTO monthly_backup (
        id,
        backup_type,
        tape_number,
        backup_date,
        server,
        os,
        backup_contents,
        backup_format,
        backup_media,
        remarks,
        tape_reuse_date,
        extra_info
      )
    VALUES (
        id:integer,
        'backup_type:character varying',
        'tape_number:character varying',
        'backup_date:date',
        'server:character varying',
        'os:character varying',
        'backup_contents:text',
        'backup_format:character varying',
        'backup_media:character varying',
        'remarks:text',
        'tape_reuse_date:date',
        'extra_info:text'
      );,
    'backup_type:character varying',
    'tape_number:character varying',
    'backup_date:date',
    'server:character varying',
    'os:character varying',
    'backup_contents:text',
    'backup_format:character varying',
    'remarks:text',
    'tape_reuse_date:date',
    'extra_info:text',
    'backup_frequency:character varying'
  );');');