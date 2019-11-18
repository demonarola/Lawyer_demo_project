CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");
CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");
CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");
CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action_time" datetime NOT NULL, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0));
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE TABLE IF NOT EXISTS "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "first_name" varchar(30) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "last_name" varchar(150) NOT NULL);
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "lawyer_practice_area" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "practice" varchar(128) NULL);
CREATE TABLE IF NOT EXISTS "lawyer_state" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "state_name" varchar(400) NULL);
CREATE TABLE IF NOT EXISTS "lawyer_sub_practice_area" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "practice_type" varchar(128) NULL, "practice_id_id" integer NULL REFERENCES "lawyer_practice_area" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "lawyer_lawyer_practice_area" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "sub_practice_area" varchar(200) NULL, "lawyer_id_id" integer NULL REFERENCES "lawyer_lawyer" ("id") DEFERRABLE INITIALLY DEFERRED, "practice_area_id" integer NULL REFERENCES "lawyer_practice_area" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "lawyer_sub_practice_area_practice_id_id_a0956ee6" ON "lawyer_sub_practice_area" ("practice_id_id");
CREATE INDEX "lawyer_lawyer_practice_area_lawyer_id_id_c93c1db9" ON "lawyer_lawyer_practice_area" ("lawyer_id_id");
CREATE INDEX "lawyer_lawyer_practice_area_practice_area_id_80d4fbf1" ON "lawyer_lawyer_practice_area" ("practice_area_id");
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
CREATE TABLE IF NOT EXISTS "lawyer_review_lawyer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(228) NOT NULL, "review" varchar(5000) NOT NULL, "rating" integer NOT NULL, "lawyer_id_id" integer NOT NULL REFERENCES "lawyer_lawyer" ("id") DEFERRABLE INITIALLY DEFERRED, "date" date NOT NULL, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "lawyer_review_lawyer_lawyer_id_id_cc30862f" ON "lawyer_review_lawyer" ("lawyer_id_id");
CREATE INDEX "lawyer_review_lawyer_user_id_e7913aad" ON "lawyer_review_lawyer" ("user_id");
CREATE TABLE IF NOT EXISTS "lawyer_lawyer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "address1" varchar(400) NOT NULL, "address2" varchar(400) NOT NULL, "zipcode" varchar(128) NOT NULL, "phone_number" varchar(128) NOT NULL, "license_id" varchar(128) NOT NULL, "year_admitted" varchar(128) NOT NULL, "profile_image" varchar(100) NOT NULL, "license_in_id" integer NOT NULL REFERENCES "lawyer_state" ("id") DEFERRABLE INITIALLY DEFERRED, "state_id" integer NOT NULL REFERENCES "lawyer_state" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "city" varchar(128) NOT NULL);
CREATE INDEX "lawyer_lawyer_license_in_id_c443f4ae" ON "lawyer_lawyer" ("license_in_id");
CREATE INDEX "lawyer_lawyer_state_id_ba8e2215" ON "lawyer_lawyer" ("state_id");
CREATE TABLE IF NOT EXISTS "registration_registrationprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activation_key" varchar(40) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "activated" bool NOT NULL);
CREATE TABLE IF NOT EXISTS "registration_supervisedregistrationprofile" ("registrationprofile_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "registration_registrationprofile" ("id") DEFERRABLE INITIALLY DEFERRED);
