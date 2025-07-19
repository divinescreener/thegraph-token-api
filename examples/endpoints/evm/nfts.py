#!/usr/bin/env python3
"""NFT Example - Get NFT ownership, collection info, and activities."""

import os
import sys
import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
from token_api import TokenAPI


async def main():
    print("NFT Example")
    print("=" * 11)
    
    api = TokenAPI()
    vitalik = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    
    try:
        # Get NFT ownership
        print(f"\nNFTs owned by {vitalik[:10]}...:")
        nfts = await api.evm.nfts.ownerships(vitalik, limit=5)
        
        for i, nft in enumerate(nfts, 1):
            name = (nft.name or 'Unnamed')[:20]
            token_id = str(nft.token_id)
            if len(token_id) > 6:
                token_id = token_id[:6] + "..."
            
            print(f"  {i}. {name} #{token_id}")
        
        # Get collection info
        print("\nCryptoPunks Collection:")
        collection = await api.evm.nfts.collection("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        
        if collection:
            name = collection.name
            supply = collection.total_supply
            owners = collection.owners
            print(f"  {name}: {supply} items, {owners} owners")
        
        # Get recent activities
        print("\nRecent Activities:")
        activities = await api.evm.nfts.activities("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb", limit=3)
        
        for i, activity in enumerate(activities, 1):
            activity_type = activity.activity_type
            token_id = activity.token_id
            from_addr = activity.from_address[:8] + "..."
            to_addr = activity.to[:8] + "..."
            
            print(f"  {i}. {activity_type} #{token_id}: {from_addr} → {to_addr}")
        
        print("\n✅ NFT data retrieved successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    anyio.run(main)