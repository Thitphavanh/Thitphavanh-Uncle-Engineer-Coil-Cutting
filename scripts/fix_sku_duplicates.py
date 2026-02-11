import sqlite3
from django.db import connection, transaction
from coil.models import CoilPallet, CoilOut

# We need raw SQL to see 'name' since it's not in the model anymore (removed in 0014)
# but exists in DB (rev 0010) and is part of the duplicate check.
def fix():
    print("Starting SKU duplicate cleanup...")
    with connection.cursor() as cursor:
        # Fetch all SKUs data relevant for comparison
        # using COALESCE to handle NULLs as empty strings for consistent grouping
        cursor.execute("""
            SELECT id, 
                   COALESCE(name, ''), 
                   COALESCE(Type0, ''), 
                   COALESCE(Type1, ''), 
                   COALESCE(Type2, ''), 
                   COALESCE(thickness, ''), 
                   COALESCE(width, ''), 
                   COALESCE(length, ''), 
                   COALESCE(color, ''), 
                   COALESCE(grade, ''), 
                   manufacturer_id, 
                   COALESCE(note1, ''), 
                   COALESCE(note2, '')
            FROM coil_sku
        """)
        rows = cursor.fetchall()
    
    # Group by content signature
    groups = {}
    for row in rows:
        sku_id = row[0]
        # Signature is everything except ID
        signature = row[1:] 
        if signature not in groups:
            groups[signature] = []
        groups[signature].append(sku_id)

    # Process duplicates
    with transaction.atomic():
        duplicates_found = 0
        for signature, ids in groups.items():
            if len(ids) > 1:
                duplicates_found += 1
                ids.sort()
                master_id = ids[0]
                dup_ids = ids[1:]
                print(f"Found {len(ids)} duplicates for signature {signature[:3]}... Merging {dup_ids} into master {master_id}")
                
                # Update references (Merge)
                pallets_updated = CoilPallet.objects.filter(type0_id__in=dup_ids).update(type0_id=master_id)
                coilouts_updated = CoilOut.objects.filter(sku_id__in=dup_ids).update(sku_id=master_id)
                
                if pallets_updated: print(f"  - Updated {pallets_updated} CoilPallets")
                if coilouts_updated: print(f"  - Updated {coilouts_updated} CoilOuts")

                # Delete duplicates
                # Use raw SQL to delete to avoid any model validation/signal issues since model mismatch
                with connection.cursor() as cursor:
                     placeholders = ','.join(['?'] * len(dup_ids))
                     cursor.execute(f"DELETE FROM coil_sku WHERE id IN ({placeholders})", dup_ids)
    
    print(f"Cleanup complete. Processed {duplicates_found} groups of duplicates.")

fix()
