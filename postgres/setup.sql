-- Create users table
CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    updated_at timestamp with time zone NOT NULL DEFAULT now(),
    is_online boolean NOT NULL DEFAULT false,
    country character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

-- Create todos table
CREATE TABLE IF NOT EXISTS public.todos
(
    id integer NOT NULL DEFAULT nextval('todos_id_seq'::regclass),
    title character varying(255) COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    is_completed boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    user_id integer,
    CONSTRAINT todos_pkey PRIMARY KEY (id),
    CONSTRAINT todos_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

-- insert some sample data into users table
INSERT INTO "users" (name, email, password, country) VALUES
    ('John', 'john@example.com', 'password123', 'US'),
    ('Jane', 'jane@example.com', 'password456', 'GB');

-- insert some sample data into todos table
INSERT INTO todos (title, description, user_id) VALUES
    ('Buy groceries', 'Milk, eggs, bread', 1),
    ('Clean apartment', 'Vacuum, dust, do laundry', 1),
    ('Finish project', 'Complete tasks A, B, and C', 2),
    ('Schedule meeting', 'With client X', 2);
