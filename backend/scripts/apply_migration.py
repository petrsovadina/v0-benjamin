#!/usr/bin/env python3
"""
Migration Helper Script for Guidelines Table Schema Update

This script provides documentation and verification for applying the
008_guidelines_add_columns.sql migration to the Supabase database.

Usage:
    1. Go to Supabase Dashboard: https://supabase.com/dashboard
    2. Select your project
    3. Navigate to SQL Editor
    4. Copy and paste the SQL from supabase/migrations/008_guidelines_add_columns.sql
    5. Run the migration
    6. Run this script to verify: python scripts/apply_migration.py

Alternatively, if you have Supabase CLI access:
    supabase login
    supabase link --project-ref higziqzcjmtmkzxbbzik
    supabase db push
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

def verify_migration():
    """Verify that the migration has been applied correctly."""
    from supabase import create_client
    import requests

    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        print("ERROR: Missing SUPABASE_URL or SUPABASE_KEY environment variables")
        return False

    client = create_client(supabase_url, supabase_key)

    print("=" * 60)
    print("Guidelines Table Migration Verification")
    print("=" * 60)

    all_passed = True

    # Check 1: content column exists
    print("\n1. Checking 'content' column...")
    try:
        result = client.table('guidelines').select('content').limit(1).execute()
        print("   ✓ 'content' column exists")
    except Exception as e:
        if 'column' in str(e).lower() and 'does not exist' in str(e).lower():
            print("   ✗ 'content' column MISSING - apply migration!")
            all_passed = False
        else:
            print(f"   ? Error: {e}")
            all_passed = False

    # Check 2: metadata column exists
    print("\n2. Checking 'metadata' column...")
    try:
        result = client.table('guidelines').select('metadata').limit(1).execute()
        print("   ✓ 'metadata' column exists")
    except Exception as e:
        if 'column' in str(e).lower() and 'does not exist' in str(e).lower():
            print("   ✗ 'metadata' column MISSING - apply migration!")
            all_passed = False
        else:
            print(f"   ? Error: {e}")
            all_passed = False

    # Check 3: match_guidelines RPC function exists
    print("\n3. Checking 'match_guidelines' RPC function...")
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }

    url = f'{supabase_url}/rest/v1/rpc/match_guidelines'
    response = requests.post(url, headers=headers, json={
        'query_embedding': [0.0] * 1536,
        'match_threshold': 0.99,
        'match_count': 1
    })

    if response.status_code == 200:
        print("   ✓ 'match_guidelines' RPC function exists and is callable")
    elif response.status_code == 404:
        print("   ✗ 'match_guidelines' RPC function MISSING - apply migration!")
        all_passed = False
    else:
        print(f"   ? Unexpected response: {response.status_code} - {response.text[:100]}")
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ MIGRATION VERIFIED - All checks passed!")
        print("=" * 60)
        return True
    else:
        print("✗ MIGRATION NEEDED - Please apply the migration SQL")
        print("=" * 60)
        print("\nTo apply the migration:")
        print("1. Open Supabase Dashboard SQL Editor")
        print("2. Run the SQL from: supabase/migrations/008_guidelines_add_columns.sql")
        print("\nMigration SQL preview:")
        print("-" * 40)
        migration_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'supabase', 'migrations', '008_guidelines_add_columns.sql'
        )
        if os.path.exists(migration_path):
            with open(migration_path, 'r') as f:
                print(f.read()[:500] + "...")
        return False


if __name__ == "__main__":
    success = verify_migration()
    sys.exit(0 if success else 1)
