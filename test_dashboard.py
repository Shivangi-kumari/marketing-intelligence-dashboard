#!/usr/bin/env python3
"""
Test script for Marketing Intelligence Dashboard
This script tests the data loading and basic functionality.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

def test_data_loading():
    """Test if data files can be loaded correctly."""
    print("🧪 Testing data loading...")
    
    try:
        # Test business data
        business_df = pd.read_csv('data/business.csv')
        print(f"✅ Business data loaded: {len(business_df)} rows")
        
        # Test Facebook data
        facebook_df = pd.read_csv('data/Facebook.csv')
        print(f"✅ Facebook data loaded: {len(facebook_df)} rows")
        
        # Test Google data
        google_df = pd.read_csv('data/Google.csv')
        print(f"✅ Google data loaded: {len(google_df)} rows")
        
        # Test TikTok data
        tiktok_df = pd.read_csv('data/TikTok.csv')
        print(f"✅ TikTok data loaded: {len(tiktok_df)} rows")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_data_processing():
    """Test data processing functions."""
    print("🧪 Testing data processing...")
    
    try:
        # Load data
        business_df = pd.read_csv('data/business.csv')
        facebook_df = pd.read_csv('data/Facebook.csv')
        
        # Convert dates
        business_df['date'] = pd.to_datetime(business_df['date'])
        facebook_df['date'] = pd.to_datetime(facebook_df['date'])
        
        # Test basic calculations
        total_revenue = business_df['total revenue'].sum()
        total_spend = facebook_df['spend'].sum()
        total_attributed_revenue = facebook_df['attributed revenue'].sum()
        
        roas = total_attributed_revenue / total_spend if total_spend > 0 else 0
        
        print(f"✅ Total Revenue: ${total_revenue:,.2f}")
        print(f"✅ Total Spend: ${total_spend:,.2f}")
        print(f"✅ ROAS: {roas:.2f}x")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return False

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported")
        
        import pandas as pd
        print("✅ Pandas imported")
        
        import plotly.express as px
        import plotly.graph_objects as go
        print("✅ Plotly imported")
        
        import numpy as np
        print("✅ NumPy imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Marketing Intelligence Dashboard - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Data Loading Test", test_data_loading),
        ("Data Processing Test", test_data_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard is ready to run.")
        print("Run: python run_dashboard.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
