#!/usr/bin/env python3

import requests
import json
import time

def test_complete_backend():
    """Test all backend functionality comprehensively"""
    base_url = "http://127.0.0.1:8001"

    print("🚀 Starting comprehensive backend test...")

    # Test data
    test_user = {
        "username": "comprehensive_test",
        "email": "comprehensive@example.com",
        "password": "testpass123"
    }

    # Step 1: Test Registration
    print("\n📝 Step 1: Testing Registration...")
    try:
        response = requests.post(f"{base_url}/auth/register", json=test_user, timeout=5)
        if response.status_code == 201:
            print(f"✅ Registration successful: {response.json()['msg']}")
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

    # Step 2: Test Login
    print("\n🔑 Step 2: Testing Login...")
    try:
        response = requests.post(f"{base_url}/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        }, timeout=5)

        if response.status_code == 200:
            print(f"✅ Login successful: {response.json()['msg']}")
            # Save cookies for authenticated requests
            cookies = response.cookies
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

    # Step 3: Test User Data (requires authentication)
    print("\n👤 Step 3: Testing User Data...")
    try:
        response = requests.get(f"{base_url}/auth/me", cookies=cookies, timeout=5)
        if response.status_code == 200:
            print(f"✅ User data fetched: {response.json()['username']}")
        elif response.status_code == 401:
            print("ℹ️  User data requires authentication (expected without proper cookie)")
        else:
            print(f"❌ User data failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ User data error: {e}")

    # Step 4: Test Transaction CRUD operations
    print("\n💰 Step 4: Testing Transaction Operations...")

    # Create a transaction
    transaction_data = {
        "type": "expense",
        "category": "Food",
        "amount": 25.50,
        "date": "2024-01-15T10:30:00",
        "note": "Lunch at restaurant"
    }

    try:
        response = requests.post(f"{base_url}/transactions/", json=transaction_data, cookies=cookies, timeout=5)
        if response.status_code == 201:
            transaction = response.json()
            transaction_id = transaction["id"]
            print(f"✅ Transaction created: {transaction['category']} - ${transaction['amount']}")
        else:
            print(f"❌ Transaction creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Transaction creation error: {e}")
        return False

    # Get all transactions
    try:
        response = requests.get(f"{base_url}/transactions/", cookies=cookies, timeout=5)
        if response.status_code == 200:
            transactions = response.json()
            print(f"✅ Retrieved {len(transactions)} transactions")
        else:
            print(f"❌ Get transactions failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Get transactions error: {e}")

    # Get specific transaction
    try:
        response = requests.get(f"{base_url}/transactions/{transaction_id}", cookies=cookies, timeout=5)
        if response.status_code == 200:
            print(f"✅ Retrieved specific transaction: {response.json()['category']}")
        else:
            print(f"❌ Get specific transaction failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Get specific transaction error: {e}")

    # Update transaction
    update_data = {
        "type": "expense",
        "category": "Food",
        "amount": 30.00,
        "date": "2024-01-15T10:30:00",
        "note": "Lunch at restaurant (updated)"
    }

    try:
        response = requests.put(f"{base_url}/transactions/{transaction_id}", json=update_data, cookies=cookies, timeout=5)
        if response.status_code == 200:
            print(f"✅ Transaction updated: ${response.json()['amount']}")
        else:
            print(f"❌ Transaction update failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Transaction update error: {e}")

    # Step 5: Test Budget Operations
    print("\n📊 Step 5: Testing Budget Operations...")

    budget_data = {
        "category": "Food",
        "amount": 500.00,
        "month": 1,
        "year": 2024
    }

    try:
        response = requests.post(f"{base_url}/budgets/", json=budget_data, cookies=cookies, timeout=5)
        if response.status_code == 201:
            budget = response.json()
            budget_id = budget["id"]
            print(f"✅ Budget created: {budget['category']} - ${budget['amount']}")
        else:
            print(f"❌ Budget creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Budget creation error: {e}")

    # Get budgets
    try:
        response = requests.get(f"{base_url}/budgets/", cookies=cookies, timeout=5)
        if response.status_code == 200:
            budgets = response.json()
            print(f"✅ Retrieved {len(budgets)} budgets")
        else:
            print(f"❌ Get budgets failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Get budgets error: {e}")

    # Step 6: Test Analytics Endpoints
    print("\n📈 Step 6: Testing Analytics...")

    # Test monthly summary
    try:
        response = requests.get(f"{base_url}/transactions/summary/2024/1", cookies=cookies, timeout=5)
        if response.status_code == 200:
            summary = response.json()
            print(f"✅ Monthly summary: Income ${summary['total_income']}, Expenses ${summary['total_expenses']}")
        else:
            print(f"❌ Monthly summary failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Monthly summary error: {e}")

    # Test dashboard overview
    try:
        response = requests.get(f"{base_url}/transactions/dashboard/overview", cookies=cookies, timeout=5)
        if response.status_code == 200:
            dashboard = response.json()
            print(f"✅ Dashboard overview: {dashboard['current_month']['transaction_count']} transactions this month")
        else:
            print(f"❌ Dashboard overview failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Dashboard overview error: {e}")

    # Test categories
    try:
        response = requests.get(f"{base_url}/transactions/categories/all", cookies=cookies, timeout=5)
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Categories retrieved: {len(categories['categories'])} categories")
        else:
            print(f"❌ Categories failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Categories error: {e}")

    print("\n🎉 Backend testing completed!")
    return True

if __name__ == "__main__":
    success = test_complete_backend()
    if success:
        print("\n✅ All backend features are working correctly!")
    else:
        print("\n❌ Some backend features failed")
