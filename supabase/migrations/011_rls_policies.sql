-- Migration: 011_rls_policies.sql

-- USERS
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid() = auth_id);

CREATE POLICY "Users can update their own profile" ON users
    FOR UPDATE USING (auth.uid() = auth_id);

-- QUERIES
CREATE POLICY "Users can view their own queries" ON queries
    FOR SELECT USING (auth.uid() = (SELECT auth_id FROM users WHERE id = user_id));

CREATE POLICY "Users can insert their own queries" ON queries
    FOR INSERT WITH CHECK (auth.uid() = (SELECT auth_id FROM users WHERE id = user_id));

CREATE POLICY "Users can delete their own queries" ON queries
    FOR DELETE USING (auth.uid() = (SELECT auth_id FROM users WHERE id = user_id));

-- CITATIONS
CREATE POLICY "Users can view citations for their queries" ON citations
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM queries 
            JOIN users ON queries.user_id = users.id 
            WHERE queries.id = citations.query_id 
            AND users.auth_id = auth.uid()
        )
    );
    
-- DRUGS (Public Read)
ALTER TABLE drugs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access for drugs" ON drugs
    FOR SELECT USING (true);
    
-- GUIDELINES (Public Read)
ALTER TABLE guidelines ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public read access for guidelines" ON guidelines
    FOR SELECT USING (true);

-- USER PREFERENCES
CREATE POLICY "Users can manage their preferences" ON user_preferences
    FOR ALL USING (auth.uid() = (SELECT auth_id FROM users WHERE id = user_id));
