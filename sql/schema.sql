-- file: schema.sql
\echo Dropping the shutter schema
drop schema shutter cascade;
\echo Creating the shutter schema
create schema shutter authorization shutter;

comment on schema shutter is 'Stores information about website snapshots';

\echo Creating the urls table
create table shutter.urls(
      "id" serial primary key
     ,"url" text not null
     ,unique("url")
);

comment on table shutter.urls is 'Website URL addresses';
comment on column shutter.urls.id is 'Unique url identifier';
comment on column shutter.urls.url is 'The website URL';

\echo Creating the snapshots table
create table shutter.snapshots(
      id serial primary key
     ,url_id integer not null references shutter.urls(id) on delete cascade
     ,"created_at" timestamp default now()
     ,file_path text not null
);

comment on table shutter.snapshots is 'Contains application screenshots';
comment on column shutter.snapshots.id is 'Unique snapshot identifier';
comment on column shutter.snapshots.url_id is 'URL the snapshot is tied to';
comment on column shutter.snapshots.created_at is 'Time when this snapshot was created';
comment on column shutter.snapshots.file_path is 'File on disk containing the screenshot';