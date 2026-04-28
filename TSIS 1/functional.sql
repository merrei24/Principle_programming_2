CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_id INT,
    first_name TEXT,
    surname TEXT,
    email TEXT,
    birthday DATE,
    group_name TEXT,
    phones TEXT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_query TEXT := COALESCE(TRIM(p_query), '');
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name::TEXT,
        c.surname::TEXT,
        COALESCE(c.email, '')::TEXT,
        c.birthday,
        COALESCE(g.name, 'Other')::TEXT,
        COALESCE(
            STRING_AGG(p.type || ':' || p.phone, ', ' ORDER BY p.id),
            ''
        )::TEXT
    FROM contacts AS c
    LEFT JOIN groups AS g ON g.id = c.group_id
    LEFT JOIN phones AS p ON p.contact_id = c.id
    WHERE
        v_query = ''
        OR c.first_name ILIKE '%' || v_query || '%'
        OR c.surname ILIKE '%' || v_query || '%'
        OR COALESCE(c.email, '') ILIKE '%' || v_query || '%'
        OR EXISTS (
            SELECT 1
            FROM phones AS p2
            WHERE p2.contact_id = c.id
              AND p2.phone ILIKE '%' || v_query || '%'
        )
    GROUP BY
        c.id,
        c.first_name,
        c.surname,
        c.email,
        c.birthday,
        g.name
    ORDER BY LOWER(c.first_name), LOWER(c.surname), c.id;
END;
$$;