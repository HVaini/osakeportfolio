

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);



CREATE TABLE public.portfolio_stocks (
    portfolio_id integer NOT NULL,
    stock_id integer NOT NULL,
    quantity integer NOT NULL
);



CREATE TABLE public.portfolios (
    id integer NOT NULL,
    user_id integer NOT NULL,
    stock_id integer,
    quantity integer,
    name text NOT NULL
);



CREATE SEQUENCE public.portfolios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE public.portfolios_id_seq OWNED BY public.portfolios.id;



CREATE TABLE public.stock_transactions (
    id integer NOT NULL,
    portfolio_id integer,
    stock_id integer,
    quantity integer NOT NULL,
    purchase_price numeric(10,2) NOT NULL,
    purchase_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);



CREATE SEQUENCE public.stock_transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE public.stock_transactions_id_seq OWNED BY public.stock_transactions.id;



CREATE TABLE public.stocks (
    id integer NOT NULL,
    symbol character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    price double precision,
    pe_ratio double precision,
    market_cap bigint
);



CREATE SEQUENCE public.stocks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE public.stocks_id_seq OWNED BY public.stocks.id;



CREATE TABLE public.transactions (
    id integer NOT NULL,
    portfolio_id integer NOT NULL,
    stock_id integer NOT NULL,
    transaction_type character varying(10),
    quantity numeric,
    price_per_share numeric,
    transaction_date timestamp without time zone DEFAULT now(),
    CONSTRAINT transactions_price_per_share_check CHECK ((price_per_share > (0)::numeric)),
    CONSTRAINT transactions_quantity_check CHECK ((quantity > (0)::numeric)),
    CONSTRAINT transactions_transaction_type_check CHECK (((transaction_type)::text = ANY ((ARRAY['buy'::character varying, 'sell'::character varying])::text[])))
);



CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;



CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(200) NOT NULL
);



CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;



CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    password_hash character varying(200) NOT NULL
);



CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;



ALTER TABLE ONLY public.portfolios ALTER COLUMN id SET DEFAULT nextval('public.portfolios_id_seq'::regclass);



ALTER TABLE ONLY public.stock_transactions ALTER COLUMN id SET DEFAULT nextval('public.stock_transactions_id_seq'::regclass);



ALTER TABLE ONLY public.stocks ALTER COLUMN id SET DEFAULT nextval('public.stocks_id_seq'::regclass);



ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);



ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);



ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);



ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);



ALTER TABLE ONLY public.portfolio_stocks
    ADD CONSTRAINT portfolio_stocks_pkey PRIMARY KEY (portfolio_id, stock_id);



ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.stock_transactions
    ADD CONSTRAINT stock_transactions_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_symbol_key UNIQUE (symbol);



ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);



ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);



ALTER TABLE ONLY public.portfolio_stocks
    ADD CONSTRAINT portfolio_stocks_portfolio_id_fkey FOREIGN KEY (portfolio_id) REFERENCES public.portfolios(id) ON DELETE CASCADE;



ALTER TABLE ONLY public.portfolio_stocks
    ADD CONSTRAINT portfolio_stocks_stock_id_fkey FOREIGN KEY (stock_id) REFERENCES public.stocks(id) ON DELETE CASCADE;



ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_stock_id_fkey FOREIGN KEY (stock_id) REFERENCES public.stocks(id);



ALTER TABLE ONLY public.portfolios
    ADD CONSTRAINT portfolios_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);



ALTER TABLE ONLY public.stock_transactions
    ADD CONSTRAINT stock_transactions_portfolio_id_fkey FOREIGN KEY (portfolio_id) REFERENCES public.portfolios(id) ON DELETE CASCADE;



ALTER TABLE ONLY public.stock_transactions
    ADD CONSTRAINT stock_transactions_stock_id_fkey FOREIGN KEY (stock_id) REFERENCES public.stocks(id) ON DELETE CASCADE;



ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_portfolio_id_fkey FOREIGN KEY (portfolio_id) REFERENCES public.portfolios(id);



ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_stock_id_fkey FOREIGN KEY (stock_id) REFERENCES public.stocks(id);



