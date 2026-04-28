CREATE OR REPLACE FUNCTION _resolve_contact_id(p_contact_name VARCHAR)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
    v_name TEXT := REGEXP_REPLACE(TRIM(COALESCE(p_contact_name, '')), E'\\s+', ' ', 'g');
    v_first_name TEXT;
    v_surname TEXT;
    v_contact_id INT;
    v_count INT;
BEGIN
    IF v_name = '' THEN
        RAISE EXCEPTION 'contact name cannot be empty';
    END IF;

    IF POSITION(' ' IN v_name) > 0 THEN
        v_first_name := SPLIT_PART(v_name, ' ', 1);
        v_surname := TRIM(SUBSTRING(v_name FROM LENGTH(v_first_name) + 1));

        SELECT c.id
        INTO v_contact_id
        FROM contacts AS c
        WHERE LOWER(c.first_name) = LOWER(v_first_name)
          AND LOWER(c.surname) = LOWER(v_surname)
        LIMIT 1;

        IF v_contact_id IS NULL THEN
            RAISE EXCEPTION 'contact not found: %', v_name;
        END IF;

        RETURN v_contact_id;
    END IF;

    SELECT COUNT(*), MIN(c.id)
    INTO v_count, v_contact_id
    FROM contacts AS c
    WHERE LOWER(c.first_name) = LOWER(v_name);

    IF v_count = 0 THEN
        RAISE EXCEPTION 'contact not found: %', v_name;
    END IF;

    IF v_count > 1 THEN
        RAISE EXCEPTION 'multiple contacts with first name %, use full name', v_name;
    END IF;

    RETURN v_contact_id;
END;
$$;


CREATE OR REPLACE PROCEDURE add_phone(
    IN p_contact_name VARCHAR,
    IN p_phone VARCHAR,
    IN p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
    v_phone TEXT := TRIM(COALESCE(p_phone, ''));
    v_type TEXT := LOWER(TRIM(COALESCE(p_type, '')));
BEGIN
    IF v_phone = '' THEN
        RAISE EXCEPTION 'phone cannot be empty';
    END IF;

    IF v_phone !~ E'^\\+?[0-9][0-9\\-\\s]{3,31}$' THEN
        RAISE EXCEPTION 'invalid phone format: %', v_phone;
    END IF;

    IF v_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'phone type must be home, work, or mobile';
    END IF;

    v_contact_id := _resolve_contact_id(p_contact_name);

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, v_phone, v_type)
    ON CONFLICT (contact_id, phone)
    DO UPDATE SET type = EXCLUDED.type;

    UPDATE contacts
    SET phone = v_phone
    WHERE id = v_contact_id
      AND (phone IS NULL OR TRIM(phone) = '');
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    IN p_contact_name VARCHAR,
    IN p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
    v_group_name TEXT := TRIM(COALESCE(p_group_name, ''));
    v_group_id INT;
BEGIN
    IF v_group_name = '' THEN
        RAISE EXCEPTION 'group name cannot be empty';
    END IF;

    v_contact_id := _resolve_contact_id(p_contact_name);

    SELECT g.id
    INTO v_group_id
    FROM groups AS g
    WHERE LOWER(g.name) = LOWER(v_group_name)
    LIMIT 1;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name)
        VALUES (INITCAP(v_group_name))
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;