### Migrations

Place migration scripts in this directory. Files must be named in
the following fashion:

    2017040500-description-of-the-changes.sql

The first element must be a number lower than 2^31-1, as it will
be stored and compared in SQLite's pragma variable `user_version`,
which is a 32 bits signed value.

As in the example above, a YYYYMMDD00 format is a sensible choice,
allowing up to 100 migrations per day.
