toc.dat                                                                                             0000600 0004000 0002000 00000022423 14774003400 0014441 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP                       }           tracker-wystatkow    16.2 (Debian 16.2-1.pgdg120+2)    17.1 "    9           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false         :           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false         ;           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false         <           1262    16384    tracker-wystatkow    DATABASE     ~   CREATE DATABASE "tracker-wystatkow" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';
 #   DROP DATABASE "tracker-wystatkow";
                     tracker-wystatkow    false         �            1259    57533    category    TABLE     _   CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.category;
       public         heap r       tracker-wystatkow    false         �            1259    57532    category_id_seq    SEQUENCE     �   CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.category_id_seq;
       public               tracker-wystatkow    false    218         =           0    0    category_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;
          public               tracker-wystatkow    false    217         �            1259    57542    money    TABLE     �   CREATE TABLE public.money (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying,
    type character varying,
    date timestamp without time zone,
    amount double precision,
    category character varying NOT NULL
);
    DROP TABLE public.money;
       public         heap r       tracker-wystatkow    false         �            1259    57541    money_id_seq    SEQUENCE     �   CREATE SEQUENCE public.money_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.money_id_seq;
       public               tracker-wystatkow    false    220         >           0    0    money_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.money_id_seq OWNED BY public.money.id;
          public               tracker-wystatkow    false    219         �            1259    57556    predict    TABLE     �   CREATE TABLE public.predict (
    id integer NOT NULL,
    user_id integer NOT NULL,
    predicted double precision,
    "real" double precision,
    date timestamp without time zone
);
    DROP TABLE public.predict;
       public         heap r       tracker-wystatkow    false         �            1259    57555    predict_id_seq    SEQUENCE     �   CREATE SEQUENCE public.predict_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.predict_id_seq;
       public               tracker-wystatkow    false    222         ?           0    0    predict_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.predict_id_seq OWNED BY public.predict.id;
          public               tracker-wystatkow    false    221         �            1259    57524    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying,
    name character varying,
    lastname character varying,
    password character varying
);
    DROP TABLE public.users;
       public         heap r       tracker-wystatkow    false         �            1259    57523    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public               tracker-wystatkow    false    216         @           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public               tracker-wystatkow    false    215         �           2604    57536    category id    DEFAULT     j   ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);
 :   ALTER TABLE public.category ALTER COLUMN id DROP DEFAULT;
       public               tracker-wystatkow    false    218    217    218         �           2604    57545    money id    DEFAULT     d   ALTER TABLE ONLY public.money ALTER COLUMN id SET DEFAULT nextval('public.money_id_seq'::regclass);
 7   ALTER TABLE public.money ALTER COLUMN id DROP DEFAULT;
       public               tracker-wystatkow    false    219    220    220         �           2604    57559 
   predict id    DEFAULT     h   ALTER TABLE ONLY public.predict ALTER COLUMN id SET DEFAULT nextval('public.predict_id_seq'::regclass);
 9   ALTER TABLE public.predict ALTER COLUMN id DROP DEFAULT;
       public               tracker-wystatkow    false    222    221    222         �           2604    57527    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public               tracker-wystatkow    false    216    215    216         2          0    57533    category 
   TABLE DATA           ,   COPY public.category (id, name) FROM stdin;
    public               tracker-wystatkow    false    218       3378.dat 4          0    57542    money 
   TABLE DATA           P   COPY public.money (id, user_id, name, type, date, amount, category) FROM stdin;
    public               tracker-wystatkow    false    220       3380.dat 6          0    57556    predict 
   TABLE DATA           G   COPY public.predict (id, user_id, predicted, "real", date) FROM stdin;
    public               tracker-wystatkow    false    222       3382.dat 0          0    57524    users 
   TABLE DATA           D   COPY public.users (id, login, name, lastname, password) FROM stdin;
    public               tracker-wystatkow    false    216       3376.dat A           0    0    category_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.category_id_seq', 28, true);
          public               tracker-wystatkow    false    217         B           0    0    money_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.money_id_seq', 98, true);
          public               tracker-wystatkow    false    219         C           0    0    predict_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.predict_id_seq', 17, true);
          public               tracker-wystatkow    false    221         D           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 2, true);
          public               tracker-wystatkow    false    215         �           2606    57540    category category_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.category DROP CONSTRAINT category_pkey;
       public                 tracker-wystatkow    false    218         �           2606    57549    money money_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.money
    ADD CONSTRAINT money_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.money DROP CONSTRAINT money_pkey;
       public                 tracker-wystatkow    false    220         �           2606    57561    predict predict_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.predict
    ADD CONSTRAINT predict_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.predict DROP CONSTRAINT predict_pkey;
       public                 tracker-wystatkow    false    222         �           2606    57531    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 tracker-wystatkow    false    216         �           2606    57550    money money_user_id_fkey    FK CONSTRAINT     w   ALTER TABLE ONLY public.money
    ADD CONSTRAINT money_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 B   ALTER TABLE ONLY public.money DROP CONSTRAINT money_user_id_fkey;
       public               tracker-wystatkow    false    220    216    3223         �           2606    57562    predict predict_user_id_fkey    FK CONSTRAINT     {   ALTER TABLE ONLY public.predict
    ADD CONSTRAINT predict_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 F   ALTER TABLE ONLY public.predict DROP CONSTRAINT predict_user_id_fkey;
       public               tracker-wystatkow    false    222    3223    216                                                                                                                                                                                                                                                     3378.dat                                                                                            0000600 0004000 0002000 00000000530 14774003400 0014253 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        6	oszczędności
7	wpłata
8	kawiarnia
9	fastfood
10	restauracja
11	wynagrodzenie
12	inwestycje
13	pamiątki
15	przelew
16	usługi telekomunikacyjne
17	subskrypcje
3	kosmetyki
18	rozrywka
19	podróże
20	przesyłki
21	jedzenie i chemia
22	konie
23	elektronika
24	hobby
25	ubrania i obuwie
26	edukacja
14	automaty
27	bilety ztm
28	prezenty
\.


                                                                                                                                                                        3380.dat                                                                                            0000600 0004000 0002000 00000014076 14774003400 0014256 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1	fundusz min. 5 lat	false	2024-08-06 16:49:55.168939	100	`inwestycje`
4	1	fundusz min. 1 rok	false	2024-08-06 16:54:33.355725	300	`inwestycje`
5	1	bilet bieszczady	false	2024-08-14 16:11:03.087891	9	`wyjazd`
6	1	czapka	false	2024-08-14 16:12:02.774989	39.5	`pamiątki`
7	1	za paliwo dla Kamila	false	2024-08-14 16:12:50.584542	67	`przelew`
8	1	opłata za tel i neta	false	2024-08-14 16:22:47.718949	153	`usługi
9	1	od wujka Mariusza	true	2024-08-26 18:51:13.367647	500	`wynagrodzenie`
10	1	spotify	false	2024-08-26 18:52:53.384197	29.99	`subskrypcje`
11	1	Wynagrodzenie OPTeam	true	2024-08-29 20:11:51.003466	1071	`wynagrodzenie`
12	1	kawa	false	2024-09-02 19:16:24.858308	24	`kawiarnia`
13	1	fundusz min. 5 lat	false	2024-09-02 19:17:31.368905	100	`inwestycje`
14	1	fundusz min. 1 rok	false	2024-09-02 19:17:43.618451	300	`inwestycje`
15	1	dodatek do simsów	false	2024-09-04 15:05:22.067716	235.52	`rozrywka`
16	1	lody	false	2024-09-06 22:27:45.191679	7	`kawiarnia`
17	1	bilet pks	false	2024-09-06 22:28:42.051099	11	`podróże`
18	1	telefon + internet	false	2024-09-07 21:31:18.146807	168	`usługi
19	1	bilet pkp	false	2024-09-12 14:25:02.677413	59	`podróże`
20	1	kebs	false	2024-09-12 22:50:07.287655	17	`fastfood`
21	1	poczta	false	2024-09-13 23:09:02.128424	26.64	`przesyłki`
22	1	kasa za opiekę nad sąsiadem	true	2024-09-14 16:53:12.965102	70	`wynagrodzenie`
23	1	zakupy	false	2024-09-23 21:12:20.277268	133.16	`jedzenie
24	1	konie	false	2024-09-23 21:12:45.136826	65	`konie`
25	1	pizza	false	2024-09-23 21:13:17.981135	26	`fastfood`
26	1	Wynagrodzenie OPTeam	true	2024-09-27 17:25:44.928402	1071	`wynagrodzenie`
27	1	opieka nad sąsiadem	true	2024-09-27 20:27:19.920553	70	`wpłata`
28	1	konie	false	2024-09-28 19:13:02.6658	65	`konie`
29	1	konie	false	2024-09-28 19:13:43.468919	65	`konie`
30	1	słodkie napoje w proszku	false	2024-10-02 15:01:42.674565	20	`jedzenie
31	1	mulina	false	2024-10-02 15:04:09.255415	6	`hobby`
32	1	kawa	false	2024-10-02 15:04:43.342752	15	`kawiarnia`
33	1	etui na okulary	false	2024-10-02 15:05:30.327289	15	`kosmetyki`
34	1	ładowarka do baterii	false	2024-10-02 15:05:53.199426	89.99	`elektronika`
35	1	bilet pks	false	2024-10-02 15:06:16.528177	26	`podróże`
36	1	ciuszki TEMU	false	2024-10-03 19:35:34.025004	51.39	`ubrania
37	1	zakupy	false	2024-10-03 19:35:58.0697	26.91	`jedzenie
38	1	Wynagrodzenie OPTeam	true	2024-10-03 19:36:32.088757	914.21	`wynagrodzenie`
39	1	od taty	true	2024-10-03 19:36:47.380415	300	`wpłata`
40	1	za kurs	false	2024-10-03 19:42:48.479086	438	`edukacja`
41	1	bilet ZTM	false	2024-11-19 11:43:43.299721	34	`podróże`
42	1	opieka nad sąsiadem	true	2024-11-19 11:44:08.980131	20	`wpłata`
43	1	konie	false	2024-11-19 11:44:26.990339	65	`konie`
44	1	fundusz min. 5 lat	false	2024-11-19 11:44:46.093053	300	`inwestycje`
45	1	fundusz min. 1 rok	false	2024-11-19 11:44:57.140546	100	`inwestycje`
46	1	zakupy	false	2024-11-19 11:46:00.3541	17.3	`jedzenie
47	1	obiad	false	2024-11-19 11:46:22.451	21.4	`restauracja`
48	1	kawa	false	2024-11-19 11:46:51.145897	8.5	`kawiarnia`
49	1	polregio	false	2024-11-19 11:47:10.849633	5.5	`podróże`
50	1	kosmetyki	false	2024-11-19 11:49:39.631602	60	`kosmetyki`
51	1	spotify	false	2024-11-19 11:49:53.050236	23.99	`subskrypcje`
52	1	wpłata	true	2024-12-04 13:32:52.823426	500	`wpłata`
53	1	wpłata	true	2024-12-04 13:33:04.402923	200	`wpłata`
54	1	bilet ZTM	false	2024-12-04 13:34:29.077697	22.8	`podróże`
55	1	kurs	false	2024-12-04 13:34:41.504283	219	`edukacja`
56	1	zbiórka	false	2024-12-04 14:45:56.293606	50	`przelew`
57	1	od taty	true	2025-01-10 20:42:36.268477	500	`wpłata`
58	1	kurs	false	2025-01-10 20:43:00.311009	219	`edukacja`
60	1	telefon + internet	false	2025-01-10 20:43:25.596046	153	`usługi
61	1	bilet pkp - Poznań	false	2025-01-14 13:57:05.182235	88	`podróże`
62	1	bilet pkp - Leżajsk	false	2025-01-14 13:57:34.361335	88	`podróże`
63	1	nocleg - hotel	false	2025-01-14 13:58:08.161465	230.45	`podróże`
64	1	wpłata	true	2025-01-14 13:58:21.336671	500	`wpłata`
65	1	opieka nad sąsiadem	true	2025-01-14 19:20:09.672824	50	`wpłata`
66	1	ztm Poznań	false	2025-01-22 18:18:06.259658	12	`podróże`
67	1	mcdonald	false	2025-01-22 18:18:27.855346	16.9	`fastfood`
68	1	notes	false	2025-01-22 18:22:12.725453	2.65	`edukacja`
69	1	biała czekolada do picia	false	2025-01-22 18:22:35.979726	27	`jedzenie
70	1	zabka	false	2025-01-22 18:22:57.719563	17.49	`jedzenie
71	1	mcdonald	false	2025-01-22 18:23:16.799076	12.8	`fastfood`
72	1	cappuccino	false	2025-01-22 18:23:38.725451	23	`jedzenie
73	1	rossman	false	2025-01-22 18:24:02.358738	13.99	`kosmetyki`
74	1	ztm Rzeszów	false	2025-01-22 18:24:26.957015	10	`podróże`
75	1	ztm Rzeszów	false	2025-01-22 18:24:48.037256	10	`podróże`
76	1	eleclerc	false	2025-01-22 18:25:14.161209	49.35	`jedzenie
77	1	spotify	false	2025-01-22 18:25:43.950308	23.99	`subskrypcje`
78	1	przelew od taty	true	2025-04-01 17:21:59.676116	500	`wpłata`
79	1	zakupy Dealz	false	2025-04-01 17:22:25.148205	12	`jedzenie
80	1	ztm Warszawa	false	2025-04-01 17:24:17.018136	95.8	`bilety
81	1	bilet PKP - Rzeszów	false	2025-04-01 17:24:42.140079	95	`podróże`
82	1	kurs rejestratorka medyczna	false	2025-04-01 17:25:06.695437	219	`edukacja`
86	1	kawa	false	2025-04-02 14:10:27.92653	16.9	`kawiarnia`
87	1	kasa od wujka	true	2025-04-02 14:10:42.687583	100	`wpłata`
88	1	zakupy Dealz	false	2025-04-02 14:11:20.183556	8.5	`jedzenie
89	1	zakupy TEDI	false	2025-04-02 14:20:08.433017	5	`hobby`
83	1	kawa	false	2025-04-01 17:25:24.643058	16.9	`kawiarnia`
84	1	bubble tea	false	2025-04-01 17:25:44.627693	21.9	`kawiarnia`
90	1	zakupy Carefoure	false	2025-04-02 17:22:56.02934	15.67	`jedzenie
91	1	zakupy TEDI	false	2025-04-03 18:49:15.077799	28	`hobby`
92	1	zakupy Rossman	false	2025-04-03 18:49:50.993618	23.37	`kosmetyki`
93	1	zakupy Biedronka	false	2025-04-03 18:50:18.52242	7.18	`jedzenie
94	1	zakupy Biedronka	false	2025-04-03 18:50:53.675324	8.99	`prezenty`
95	1	zakupy Action	false	2025-04-03 18:51:06.845214	8.99	`prezenty`
96	1	bilet ZTM Warszawa	false	2025-04-04 14:15:15.839122	4.4	`bilety
97	1	kanapka na mieście	false	2025-04-04 14:15:56.013407	12.9	`jedzenie
98	1	zakupy Carrefour	false	2025-04-04 14:16:20.665574	13.5	`jedzenie
\.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                  3382.dat                                                                                            0000600 0004000 0002000 00000000456 14774003400 0014255 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        1	1	1439.31	872.51	2024-09-02 19:02:36.171481
11	1	1439.29	-91.31999999999994	2024-10-02 14:59:32.263034
13	1	1439.27	525.9200000000001	2024-11-19 11:42:07.70976
14	1	1439.26	-615.69	2024-12-04 13:35:04.051493
15	1	1439.24	408.2	2025-01-10 20:58:20.039618
16	1	1439.4	0	2025-04-01 17:27:09.782396
\.


                                                                                                                                                                                                                  3376.dat                                                                                            0000600 0004000 0002000 00000000250 14774003400 0014250 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        2	ola	Ola	Ola	$2b$12$zy8zVeGI.LqYpLGN10ov6.xZtLQHRupTEa3jBN.tSGvg/ntS/5B1W
1	alorys	Aleksandra	Loryś	$2b$12$LmrCCSbW2qZOHoJHdKxyY.quNaspKbERaesNwxyap0ShXSp9mGQtu
\.


                                                                                                                                                                                                                                                                                                                                                        restore.sql                                                                                         0000600 0004000 0002000 00000017633 14774003400 0015375 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 17.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE "tracker-wystatkow";
--
-- Name: tracker-wystatkow; Type: DATABASE; Schema: -; Owner: tracker-wystatkow
--

CREATE DATABASE "tracker-wystatkow" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE "tracker-wystatkow" OWNER TO "tracker-wystatkow";

\connect -reuse-previous=on "dbname='tracker-wystatkow'"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: category; Type: TABLE; Schema: public; Owner: tracker-wystatkow
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.category OWNER TO "tracker-wystatkow";

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: tracker-wystatkow
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.category_id_seq OWNER TO "tracker-wystatkow";

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tracker-wystatkow
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- Name: money; Type: TABLE; Schema: public; Owner: tracker-wystatkow
--

CREATE TABLE public.money (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name character varying,
    type character varying,
    date timestamp without time zone,
    amount double precision,
    category character varying NOT NULL
);


ALTER TABLE public.money OWNER TO "tracker-wystatkow";

--
-- Name: money_id_seq; Type: SEQUENCE; Schema: public; Owner: tracker-wystatkow
--

CREATE SEQUENCE public.money_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.money_id_seq OWNER TO "tracker-wystatkow";

--
-- Name: money_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tracker-wystatkow
--

ALTER SEQUENCE public.money_id_seq OWNED BY public.money.id;


--
-- Name: predict; Type: TABLE; Schema: public; Owner: tracker-wystatkow
--

CREATE TABLE public.predict (
    id integer NOT NULL,
    user_id integer NOT NULL,
    predicted double precision,
    "real" double precision,
    date timestamp without time zone
);


ALTER TABLE public.predict OWNER TO "tracker-wystatkow";

--
-- Name: predict_id_seq; Type: SEQUENCE; Schema: public; Owner: tracker-wystatkow
--

CREATE SEQUENCE public.predict_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.predict_id_seq OWNER TO "tracker-wystatkow";

--
-- Name: predict_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tracker-wystatkow
--

ALTER SEQUENCE public.predict_id_seq OWNED BY public.predict.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: tracker-wystatkow
--

CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying,
    name character varying,
    lastname character varying,
    password character varying
);


ALTER TABLE public.users OWNER TO "tracker-wystatkow";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: tracker-wystatkow
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO "tracker-wystatkow";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tracker-wystatkow
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- Name: money id; Type: DEFAULT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.money ALTER COLUMN id SET DEFAULT nextval('public.money_id_seq'::regclass);


--
-- Name: predict id; Type: DEFAULT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.predict ALTER COLUMN id SET DEFAULT nextval('public.predict_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: tracker-wystatkow
--

COPY public.category (id, name) FROM stdin;
\.
COPY public.category (id, name) FROM '$$PATH$$/3378.dat';

--
-- Data for Name: money; Type: TABLE DATA; Schema: public; Owner: tracker-wystatkow
--

COPY public.money (id, user_id, name, type, date, amount, category) FROM stdin;
\.
COPY public.money (id, user_id, name, type, date, amount, category) FROM '$$PATH$$/3380.dat';

--
-- Data for Name: predict; Type: TABLE DATA; Schema: public; Owner: tracker-wystatkow
--

COPY public.predict (id, user_id, predicted, "real", date) FROM stdin;
\.
COPY public.predict (id, user_id, predicted, "real", date) FROM '$$PATH$$/3382.dat';

--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tracker-wystatkow
--

COPY public.users (id, login, name, lastname, password) FROM stdin;
\.
COPY public.users (id, login, name, lastname, password) FROM '$$PATH$$/3376.dat';

--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tracker-wystatkow
--

SELECT pg_catalog.setval('public.category_id_seq', 28, true);


--
-- Name: money_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tracker-wystatkow
--

SELECT pg_catalog.setval('public.money_id_seq', 98, true);


--
-- Name: predict_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tracker-wystatkow
--

SELECT pg_catalog.setval('public.predict_id_seq', 17, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tracker-wystatkow
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: money money_pkey; Type: CONSTRAINT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.money
    ADD CONSTRAINT money_pkey PRIMARY KEY (id);


--
-- Name: predict predict_pkey; Type: CONSTRAINT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.predict
    ADD CONSTRAINT predict_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: money money_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.money
    ADD CONSTRAINT money_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: predict predict_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tracker-wystatkow
--

ALTER TABLE ONLY public.predict
    ADD CONSTRAINT predict_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     