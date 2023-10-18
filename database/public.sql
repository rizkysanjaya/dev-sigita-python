/*
 Navicat Premium Data Transfer

 Source Server         : Postgre Localhost Server
 Source Server Type    : PostgreSQL
 Source Server Version : 160000 (160000)
 Source Host           : localhost:5432
 Source Catalog        : dev_sigita
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160000 (160000)
 File Encoding         : 65001

 Date: 18/10/2023 16:12:06
*/


-- ----------------------------
-- Type structure for status_hadir
-- ----------------------------
DROP TYPE IF EXISTS "public"."status_hadir";
CREATE TYPE "public"."status_hadir" AS ENUM (
  'AKAN_HADIR',
  'TIDAK_HADIR',
  'MUNGKIN_HADIR',
  'DIWAKILKAN',
  'HADIR'
);
ALTER TYPE "public"."status_hadir" OWNER TO "postgres";

-- ----------------------------
-- Type structure for type_status
-- ----------------------------
DROP TYPE IF EXISTS "public"."type_status";
CREATE TYPE "public"."type_status" AS ENUM (
  'AKAN_DATANG',
  'BATAL',
  'SELESAI'
);
ALTER TYPE "public"."type_status" OWNER TO "postgres";

-- ----------------------------
-- Sequence structure for kegiatan_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."kegiatan_id_seq";
CREATE SEQUENCE "public"."kegiatan_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for lampiran_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."lampiran_id_seq";
CREATE SEQUENCE "public"."lampiran_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for user_kegiatan_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."user_kegiatan_id_seq";
CREATE SEQUENCE "public"."user_kegiatan_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."users_id_seq";
CREATE SEQUENCE "public"."users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for kegiatan
-- ----------------------------
DROP TABLE IF EXISTS "public"."kegiatan";
CREATE TABLE "public"."kegiatan" (
  "id" int4 NOT NULL DEFAULT nextval('kegiatan_id_seq'::regclass),
  "nama_kegiatan" varchar(255) COLLATE "pg_catalog"."default",
  "tanggal" date,
  "jam_mulai" time(4),
  "jam_selesai" time(4),
  "zona_waktu" varchar(5) COLLATE "pg_catalog"."default",
  "tempat" varchar(255) COLLATE "pg_catalog"."default",
  "status" "public"."type_status",
  "is_draft" int2,
  "tanggal_selesai" date
)
;

-- ----------------------------
-- Records of kegiatan
-- ----------------------------
INSERT INTO "public"."kegiatan" VALUES (35, 'Gladi Bersih 12', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (36, 'Gladi Bersih 12', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (37, 'Gladi Bersih 13', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (39, 'Gladi Bersih 14', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (40, 'Gladi Bersih 15', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (41, 'Gladi Bersih 16', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (44, 'Test Create 1', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'BATAL', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (38, 'Gladi Bersih 13', '2023-08-31', '10:00:00', '12:00:00', 'WIB', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (30, 'Gladi Bersih 7', '2023-08-31', '10:00:00', '12:00:00', 'WIT', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (42, 'Gladi Bersih 17', '2023-08-31', '10:00:00', '12:00:00', 'WIB', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (32, 'Gladi Bersih 9', '2023-08-31', '10:00:00', '12:00:00', 'WIB', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (8, 'Test Post', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'BATAL', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (2, 'Rapat 12', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (6, 'Rapat', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'SELESAI', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (5, 'Ini juga test ajah ini mah', '2021-08-01', '09:00:00', '12:00:00', 'WITA', 'Aula Utama', 'BATAL', 1, NULL);
INSERT INTO "public"."kegiatan" VALUES (43, 'Gladi Bersih 18', '2023-08-31', '10:00:00', '12:00:00', 'WIT', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (10, 'Test Post', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (3, 'Tes update', '2023-09-21', '09:00:00', '12:00:00', 'WIB', 'Aula 2nd Floor', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (11, 'yee', '2023-09-05', '15:56:16', '17:56:20', 'WIB', 'yeeeees', 'BATAL', 1, NULL);
INSERT INTO "public"."kegiatan" VALUES (14, 'Test Post 3', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'AKAN_DATANG', 1, NULL);
INSERT INTO "public"."kegiatan" VALUES (20, 'Test ', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (9, 'Tes update', '2023-09-21', '09:00:00', '12:00:00', 'WIB', 'Aula 2nd Floor', 'SELESAI', 1, NULL);
INSERT INTO "public"."kegiatan" VALUES (12, 'Tes update', '2023-09-21', '09:00:00', '12:00:00', 'WIB', 'Aula 2nd Floor', 'SELESAI', 1, NULL);
INSERT INTO "public"."kegiatan" VALUES (13, 'Test Post 2', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'BATAL', 1, NULL);
INSERT INTO "public"."kegiatan" VALUES (21, 'Test Post 6', '2021-08-01', '08:00:00', '11:00:00', 'WIT', 'Aula Utama', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (22, 'Gladi Bersih', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (24, 'Gladi Bersih 2', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (25, 'Gladi Bersih 3', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (26, 'Gladi Bersih 4', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (27, 'Gladi Bersih 5', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (28, 'Gladi Bersih 5', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (29, 'Rapat dewan pembina saja', '2023-08-08', '09:00:00', '12:00:00', 'WITA', 'Gedung C', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (1, 'Test ajah ini mah', '2021-08-01', '09:00:00', '12:00:00', 'WITA', 'Aula Utama', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (31, 'Gladi Bersih 8', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (33, 'Gladi Bersih 10', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);
INSERT INTO "public"."kegiatan" VALUES (34, 'Gladi Bersih 10', '2023-08-31', '10:00:00', '12:00:00', 'WITA', 'Gedung Aulia', 'AKAN_DATANG', 0, NULL);

-- ----------------------------
-- Table structure for lampiran
-- ----------------------------
DROP TABLE IF EXISTS "public"."lampiran";
CREATE TABLE "public"."lampiran" (
  "id" int4 NOT NULL DEFAULT nextval('lampiran_id_seq'::regclass),
  "id_kegiatan" int4,
  "path" varchar(255) COLLATE "pg_catalog"."default",
  "nama_file" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of lampiran
-- ----------------------------
INSERT INTO "public"."lampiran" VALUES (1, 5, '/Users/Administrator/Pictures/img_082092.png', 'zvvyEAF5aB');
INSERT INTO "public"."lampiran" VALUES (2, 21, 'C:\Users\Administrator\Pictures\img_246258.jpg', 'OApbieXkHh');
INSERT INTO "public"."lampiran" VALUES (3, 8, 'C:\Users\Administrator\Pictures\img_940211.png', '9IAft0JhID');
INSERT INTO "public"."lampiran" VALUES (4, 14, '/home/Administrator/Pictures/img_754136.jpg', 'ZiGhnRyjzz');
INSERT INTO "public"."lampiran" VALUES (6, 1, '/Users/Administrator/Pictures/img_801710.jpg', '4IOhR8B5ZC');
INSERT INTO "public"."lampiran" VALUES (7, 2, '/home/Administrator/Pictures/img_903994.png', 'BmnVH9e62i');
INSERT INTO "public"."lampiran" VALUES (8, 20, '/Users/Administrator/Pictures/img_183152.png', 'OCS8UwVd1X');
INSERT INTO "public"."lampiran" VALUES (9, 8, '/home/Administrator/Pictures/img_278432.png', 'yYjz74jZHI');
INSERT INTO "public"."lampiran" VALUES (10, 3, '/home/Administrator/Pictures/img_804518.jpg', 'hpoqtZY9Nk');
INSERT INTO "public"."lampiran" VALUES (13, 29, '/path/to/file/main.min.js', 'main.min.js');
INSERT INTO "public"."lampiran" VALUES (14, 29, '/path/to/file/app.db', 'app.db');
INSERT INTO "public"."lampiran" VALUES (15, 30, '/path/to/file/bookapi.sql', 'bookapi.sql');
INSERT INTO "public"."lampiran" VALUES (16, 30, '/path/to/file/app.db', 'app.db');
INSERT INTO "public"."lampiran" VALUES (17, 31, '/path/to/file/bookapi.sql', 'bookapi.sql');
INSERT INTO "public"."lampiran" VALUES (18, 31, '/path/to/file/app.db', 'app.db');
INSERT INTO "public"."lampiran" VALUES (19, 32, '/path/to/file/respn.xlsx', 'respn.xlsx');
INSERT INTO "public"."lampiran" VALUES (21, 34, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media/user_upload/lampiranORD00010.png', 'ORD00010.png');
INSERT INTO "public"."lampiran" VALUES (22, 36, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\ORD00010.png', 'E-Tiket(ORD0004).pdf');
INSERT INTO "public"."lampiran" VALUES (23, 36, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\ORD00010.png', 'ORD00010.png');
INSERT INTO "public"."lampiran" VALUES (24, 38, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\Book1.xlsx', 'Book1.xlsx');
INSERT INTO "public"."lampiran" VALUES (25, 38, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\respon time.pdf', 'respon time.pdf');
INSERT INTO "public"."lampiran" VALUES (26, 39, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\Book1.xlsx', 'Book1.xlsx');
INSERT INTO "public"."lampiran" VALUES (27, 39, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\respon_time.pdf', 'respon time.pdf');
INSERT INTO "public"."lampiran" VALUES (28, 40, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\Book1.xlsx', 'Book1.xlsx');
INSERT INTO "public"."lampiran" VALUES (29, 40, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\respon_time.pdf', 'respon_time.pdf');
INSERT INTO "public"."lampiran" VALUES (30, 41, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\Book1_1695720702.xlsx', 'Book1_1695720702.xlsx');
INSERT INTO "public"."lampiran" VALUES (31, 41, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\respon_time_1695720702.pdf', 'respon_time_1695720702.pdf');
INSERT INTO "public"."lampiran" VALUES (32, 42, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\Book1_1695721289.xlsx', 'Book1.xlsx');
INSERT INTO "public"."lampiran" VALUES (33, 42, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\respon_time_1695721289.pdf', 'respon_time.pdf');
INSERT INTO "public"."lampiran" VALUES (34, 43, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\Book1_1695721948.xlsx', 'Book1.xlsx');
INSERT INTO "public"."lampiran" VALUES (35, 43, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\lampiran\respon_time_1695721948.pdf', 'respon_time.pdf');

-- ----------------------------
-- Table structure for user_kegiatan
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_kegiatan";
CREATE TABLE "public"."user_kegiatan" (
  "id" int4 NOT NULL DEFAULT nextval('user_kegiatan_id_seq'::regclass),
  "id_kegiatan" int4,
  "id_user" int4,
  "status_kehadiran" "public"."status_hadir",
  "status_perwakilan" int2,
  "is_protokoler" int2,
  "reason" varchar(255) COLLATE "pg_catalog"."default",
  "is_read" int2,
  "is_ignore" int2
)
;

-- ----------------------------
-- Records of user_kegiatan
-- ----------------------------
INSERT INTO "public"."user_kegiatan" VALUES (57, 31, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (58, 31, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (60, 31, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (61, 31, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (62, 32, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (63, 32, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (64, 32, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (65, 32, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (66, 32, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (72, 34, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (73, 34, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (74, 34, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (75, 34, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (76, 34, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (82, 36, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (83, 36, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (84, 36, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (85, 36, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (86, 36, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (92, 38, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (93, 38, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (94, 38, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (95, 38, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (96, 38, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (97, 39, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (98, 39, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (47, 29, 11, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (48, 29, 14, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (49, 30, 1, NULL, NULL, 1, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (50, 30, 2, NULL, NULL, 1, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (51, 30, 3, NULL, NULL, 1, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (52, 30, 4, NULL, NULL, 1, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (53, 30, 5, NULL, NULL, 0, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (99, 39, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (100, 39, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (101, 39, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (102, 40, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (103, 40, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (104, 40, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (105, 40, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (106, 40, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (107, 41, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (108, 41, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (109, 41, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (110, 41, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (111, 41, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (112, 42, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (113, 42, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (114, 42, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (115, 42, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (116, 42, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (117, 43, 1, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (118, 43, 2, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (119, 43, 3, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (120, 43, 4, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (121, 43, 5, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (54, 1, 4, NULL, NULL, 1, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (56, 1, 11, NULL, NULL, 1, NULL, 1, NULL);
INSERT INTO "public"."user_kegiatan" VALUES (1, 12, 9, 'TIDAK_HADIR', NULL, 1, 'Malas', 1, 0);
INSERT INTO "public"."user_kegiatan" VALUES (55, 1, 6, 'TIDAK_HADIR', NULL, 1, 'Malas mlas malassa amlamas', 1, 0);
INSERT INTO "public"."user_kegiatan" VALUES (59, 31, 3, 'TIDAK_HADIR', NULL, 1, 'Dinas luar kota', NULL, 1);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "nip" varchar(255) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "fcm_token" varchar(255) COLLATE "pg_catalog"."default",
  "wa_number" varchar(255) COLLATE "pg_catalog"."default",
  "is_default_password" int2,
  "role" int2,
  "status" int2,
  "avatar_url" varchar(255) COLLATE "pg_catalog"."default",
  "email_verified_at" timestamp(6),
  "password" varchar(255) COLLATE "pg_catalog"."default",
  "remember_token" varchar(100) COLLATE "pg_catalog"."default",
  "created_at" timestamp(6),
  "updated_at" timestamp(6)
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "public"."users" VALUES (18, 'Shio 2', '555556', 'sio@gmail.com', NULL, '417417417', 1, 3, 1, 'defaultAvatarUrl', NULL, 'sha256$PWfK5XwJwouq12YN$b71514fd0dd9c495ffbdfd4e6a1211c49eea53dd67c12ff24effdefaaaa0acd5', NULL, '2023-09-26 12:14:17.407237', '2023-09-26 12:14:17.407237');
INSERT INTO "public"."users" VALUES (3, 'Tiffany Soto', '999000', 'tiffanysoto68@gmail.com', 'tC9SsuW2LI', 'lq19Y2zof4', 1, 1, 1, 'https://i.pravatar.cc/150?img=7', '2002-02-14 21:55:53', 'tes123', 'lzu6jNetoL', '2023-09-13 12:18:39.228191', '2023-09-13 15:26:56.429184');
INSERT INTO "public"."users" VALUES (4, 'Lo Wing Fat', '990099', 'lowf@icloud.com', '60TOcYh23h', 'WJmc7UwG3T', 1, 2, 1, 'https://i.pravatar.cc/150?img=8', '2019-10-14 22:20:26', 'l4DANGG4vd', 'zoX8bC6zL3', '2023-09-13 12:18:39.228191', '2023-09-13 15:26:59.666728');
INSERT INTO "public"."users" VALUES (20, 'Kali', '1100', 'kali@gmail.com', NULL, '2292417', 1, 3, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$9aSbmJkevGG3TsFy$6a422fe4615ca1935c7946cdc12da4700b3bad51c1b5b6c08869b94336582aaf', NULL, '2023-09-26 14:04:30.849203', '2023-09-26 14:04:30.849203');
INSERT INTO "public"."users" VALUES (23, 'SUPER ADMIN', '666666', 'SU@gmail.com', NULL, '678979987', 1, 1, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$GvUCv4IT7wXz8Qw4$42045cb4e384bf047af773c214308ffc7e1032bfcad43a0a892a4a943fb962fb', NULL, '2023-09-27 11:56:28.663255', '2023-09-27 11:56:28.663255');
INSERT INTO "public"."users" VALUES (13, 'Rojik', '1110909', 'rojik@gmail.com', NULL, '2', 1, 2, 1, 'defaultAvatarUrl', NULL, 'r4o7zKcFyu0qzjOM', NULL, '2023-09-21 11:20:14.201386', '2023-09-27 12:24:06.195437');
INSERT INTO "public"."users" VALUES (7, 'Kao Sau Man', '122133', 'kaosm@gmail.com', 'klilcPOg6V', '8QtZZJWQce', 1, 2, 1, 'https://i.pravatar.cc/150?img=4', '2006-02-03 01:38:44', 'G9Ewi4TSNQ', 'bjVZiScwyc', '2023-09-13 12:18:39.228191', '2023-09-13 15:29:10.015852');
INSERT INTO "public"."users" VALUES (8, 'Ogawa Hazuki', '123123', 'ogawahazu@hotmail.com', '1E3npgyixC', 'HdKxxFmwSq', 0, 3, 1, 'https://i.pravatar.cc/150?img=5', '2016-04-15 08:47:50', 'G7pakwherA', 'zc6fEptf41', '2023-09-13 12:18:39.228191', '2023-09-13 15:29:14.275404');
INSERT INTO "public"."users" VALUES (9, 'Yeow Ka Ling', '111222', 'kalingy@hotmail.com', 'WSeOAYqRIG', 'KJDxL2oc8U', 0, 3, 1, 'https://i.pravatar.cc/150?img=3', '2009-03-24 09:49:45', 'PdQXo3P8Kk', '6JtqjAZ3aZ', '2023-09-13 12:18:39.228191', '2023-09-13 15:29:18.674');
INSERT INTO "public"."users" VALUES (14, 'Rojik 2', '1110902', 'rojik2@gmail.com', NULL, '2', 1, 3, 1, 'defaultAvatarUrl', NULL, 'CkWAZjbFETniFsIi', NULL, '2023-09-21 11:21:35.249387', '2023-09-27 12:26:19.874497');
INSERT INTO "public"."users" VALUES (6, 'Shimizu Hazuki', '112233', 'hazukishimizu@gmail.com', 'QZm6XGvxUB', 'B0ehFmafP9', 1, 2, 1, 'https://i.pravatar.cc/150?img=10', '2011-10-21 04:27:21', '1234', 'CFu5HQLTtZ', '2023-09-13 12:18:39.228191', '2023-09-18 14:03:33.876677');
INSERT INTO "public"."users" VALUES (12, 'rojak 2', '990011', 'rojak2@gmail.com', NULL, '62895667766551', 1, 1, 1, 'defaultAvatarUrl', NULL, 'h4Vj2CHl3LfT7q0A', NULL, '2023-09-21 11:13:46.303629', '2023-09-21 11:13:46.303629');
INSERT INTO "public"."users" VALUES (25, 'regular user', '12375632', 'ru3@gmail.com', NULL, '678979987', 1, 3, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$Cjz0t9Y4IViwAkmj$db5c12b9e6f76f6061a335b64b7f29e242e3a85e3186645aa3884e9022e69dda', NULL, '2023-09-27 12:33:10.441071', '2023-09-27 12:33:10.441071');
INSERT INTO "public"."users" VALUES (10, 'Francisco Morgan', '121212', 'francisco01@mail.com', 'JJIrzicae4', 'rguzVxMDwg', 1, 3, 1, 'C:\Users\sanja\Documents\Python Scripts\dev-sigita-python\media\user_upload\avatar\logo-tix_1695797667.jpeg', '2000-08-29 18:33:38', 'pbkdf2:sha256:600000$3M5WS9ceMPRraIZv$78e67f7e088f1ec55316b490016f777ea5920ee48d17f168e6421670cf816ff8', 'yygCo5hvrT', '2023-09-13 12:18:39.228191', '2023-09-27 13:54:27.483683');
INSERT INTO "public"."users" VALUES (5, 'admin', '12345678', 'admin@gmail.com', 'WfaSuT51De', '2', 1, 2, 1, 'https://i.pravatar.cc/150?img=9', '2019-04-20 12:31:10', 'IGD3BKjsgi', 'j9XDHC5JE5', '2023-09-13 12:18:39.228191', '2023-09-25 11:43:42.562016');
INSERT INTO "public"."users" VALUES (1, 'Kong Jiehong', '909099', 'kj1941@yahoo.com', 'amcb0nSEGE', 'AGlPDEsjdS', 1, 1, 1, 'https://i.pravatar.cc/150?img=12', '2000-03-08 14:21:09', 'pass123', '9qviHUjXQN', '2023-09-13 12:18:39.228191', '2023-09-13 15:26:23.901832');
INSERT INTO "public"."users" VALUES (16, 'ruby', '11223344', 'ruby@gmail.com', NULL, '1', 1, 1, 1, 'defaultAvatarUrl', NULL, 'Buwqm7YJTO6ncONH', NULL, '2023-09-21 11:23:33.745628', '2023-09-27 12:35:43.528849');
INSERT INTO "public"."users" VALUES (19, 'ruby', '11223344', 'ruby@gmail.com', NULL, '1', 1, 1, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$3X9b5LH8gMOTx50J$a52b7ac3a5ffd401ad5cc33ef334eeb6fe008b75c392ce287bd8ff844cf04c0e', NULL, '2023-09-26 12:56:16.142624', '2023-09-27 12:43:12.310102');
INSERT INTO "public"."users" VALUES (22, 'bejo', '11223344', 'ruby@gmail.com', NULL, '1', 1, 1, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$adW8wjqQXd5ay0lT$0a187263725efef09bcaffca653d0b28ed2eb3fc0471e69aeeb192da235c7eb2', NULL, '2023-09-27 11:49:44.436611', '2023-09-27 12:50:12.62239');
INSERT INTO "public"."users" VALUES (21, 'Oro Koni', '717447', 'oro@gmail.com', NULL, '678979987', 1, 3, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$4daaJqIVt56DKZ60$5ba198a8de999d8f5e6e61aa4b55daa1bd4bbdf74bcb6a6c7e1d4457f9815389', NULL, '2023-09-27 10:58:58.803717', '2023-09-27 13:05:55.459281');
INSERT INTO "public"."users" VALUES (26, 'bejo', '11223344', 'ruby@gmail.com', NULL, '1', 1, 2, 1, 'defaultAvatarUrl', NULL, 'pbkdf2:sha256:600000$AWoL30nBGEjuSCwT$24aaed833a0e24178616c73675ad92147e3155ae40bf276f1f8c988613f03bea', NULL, '2023-09-27 12:33:43.441934', '2023-09-27 13:06:08.881342');
INSERT INTO "public"."users" VALUES (11, 'rojak  ', '990011', 'rojak@gmail.com', NULL, '62895667766551', NULL, 1, NULL, '/path/to/file/default.jpg', NULL, NULL, NULL, '2023-09-21 10:36:41.940053', '2023-09-25 12:21:19.098326');
INSERT INTO "public"."users" VALUES (2, 'Fang Xiuying', '909098', 'fxiuying5@gmail.com', 'z1efBCjI7R', '0oMdp4cYrt', 1, 3, 0, 'https://i.pravatar.cc/150?img=6', '2006-11-28 15:48:58', 'password', 'rCsltyRfK1', '2023-09-13 12:18:39.228191', '2023-09-25 17:02:07.839495');
INSERT INTO "public"."users" VALUES (17, 'Shio', '555555', 'sio@gmail.com', NULL, '417417417', 1, 3, 1, 'defaultAvatarUrl', NULL, 'sha256$gnRGnNvzgK9rqjny$ed24a2a420451655d12a8cfed0f2bc2cbb05f259a5bb0d225f32e148a714c2af', NULL, '2023-09-26 12:11:16.24344', '2023-09-26 12:11:16.24344');

-- ----------------------------
-- Function structure for update_user_timestamp
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."update_user_timestamp"();
CREATE OR REPLACE FUNCTION "public"."update_user_timestamp"()
  RETURNS "pg_catalog"."trigger" AS $BODY$
BEGIN
    IF TG_OP = 'INSERT' THEN
        NEW.created_at = NOW();
    END IF;
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."kegiatan_id_seq"
OWNED BY "public"."kegiatan"."id";
SELECT setval('"public"."kegiatan_id_seq"', 44, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."lampiran_id_seq"
OWNED BY "public"."lampiran"."id";
SELECT setval('"public"."lampiran_id_seq"', 36, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."user_kegiatan_id_seq"
OWNED BY "public"."user_kegiatan"."id";
SELECT setval('"public"."user_kegiatan_id_seq"', 121, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."users_id_seq"
OWNED BY "public"."users"."id";
SELECT setval('"public"."users_id_seq"', 26, true);

-- ----------------------------
-- Primary Key structure for table kegiatan
-- ----------------------------
ALTER TABLE "public"."kegiatan" ADD CONSTRAINT "kegiatan_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table lampiran
-- ----------------------------
ALTER TABLE "public"."lampiran" ADD CONSTRAINT "lampiran_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_kegiatan
-- ----------------------------
ALTER TABLE "public"."user_kegiatan" ADD CONSTRAINT "user_kegiatan_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Triggers structure for table users
-- ----------------------------
CREATE TRIGGER "trigger_update_user_timestamp" BEFORE INSERT OR UPDATE OF "id", "name", "nip", "email", "fcm_token", "wa_number", "is_default_password", "role", "status", "avatar_url", "email_verified_at", "password", "remember_token", "created_at", "updated_at" ON "public"."users"
FOR EACH ROW
EXECUTE PROCEDURE "public"."update_user_timestamp"();

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "public"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table lampiran
-- ----------------------------
ALTER TABLE "public"."lampiran" ADD CONSTRAINT "lampiran_id_kegiatan_fkey" FOREIGN KEY ("id_kegiatan") REFERENCES "public"."kegiatan" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table user_kegiatan
-- ----------------------------
ALTER TABLE "public"."user_kegiatan" ADD CONSTRAINT "user_kegiatan_id_kegiatan_fkey" FOREIGN KEY ("id_kegiatan") REFERENCES "public"."kegiatan" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."user_kegiatan" ADD CONSTRAINT "user_kegiatan_id_user_fkey" FOREIGN KEY ("id_user") REFERENCES "public"."users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
