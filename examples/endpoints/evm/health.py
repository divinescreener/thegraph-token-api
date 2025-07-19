#!/usr/bin/env python3
"""Health Check Example - Check API health and connectivity."""

import os
import sys
import anyio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))
from token_api import TokenAPI


async def main():
    print("API Health Check")
    print("=" * 16)
    
    api = TokenAPI()
    
    try:
        # Check API health
        print("\nChecking API health...")
        health_status = await api.health()
        print(f"Status: {health_status}")
        
        if health_status.lower() == "ok":
            print("✅ API is healthy")
        else:
            print("⚠️ API may have issues")
        
        # Test connectivity with simple call
        print("\nTesting connectivity...")
        test_data = await api.evm.balances("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", limit=1)
        
        if test_data:
            print(f"✅ API call successful - received {len(test_data)} result(s)")
        else:
            print("⚠️ No data returned")
        
        print("\n✅ Health check completed!")
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")


if __name__ == "__main__":
    anyio.run(main)