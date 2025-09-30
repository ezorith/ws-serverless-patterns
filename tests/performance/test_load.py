# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import concurrent.futures
import time
import requests
import os
import pytest
from statistics import mean, median

API_ENDPOINT = os.getenv('API_ENDPOINT')

@pytest.fixture
def api_client():
    if not API_ENDPOINT:
        pytest.skip("API_ENDPOINT environment variable not set")
    return requests.Session()

def create_user(session, user_data):
    """Create a user and measure response time"""
    start_time = time.time()
    response = session.put(f"{API_ENDPOINT}/users", json=user_data)
    end_time = time.time()
    return {
        'status_code': response.status_code,
        'response_time': end_time - start_time,
        'user_id': response.json().get('userid') if response.status_code == 200 else None
    }

def get_users(session):
    """Get all users and measure response time"""
    start_time = time.time()
    response = session.get(f"{API_ENDPOINT}/users")
    end_time = time.time()
    return {
        'status_code': response.status_code,
        'response_time': end_time - start_time,
        'user_count': len(response.json()) if response.status_code == 200 else 0
    }

class TestPerformance:
    
    def test_concurrent_user_creation(self, api_client):
        """Test creating multiple users concurrently"""
        num_users = 10
        user_data = {"name": "Load Test User", "email": "loadtest@example.com"}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(create_user, requests.Session(), user_data)
                for _ in range(num_users)
            ]
            
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all requests succeeded
        successful_requests = [r for r in results if r['status_code'] == 200]
        assert len(successful_requests) == num_users
        
        # Check response times
        response_times = [r['response_time'] for r in successful_requests]
        avg_response_time = mean(response_times)
        median_response_time = median(response_times)
        
        print(f"Average response time: {avg_response_time:.3f}s")
        print(f"Median response time: {median_response_time:.3f}s")
        
        # Assert reasonable response times (adjust thresholds as needed)
        assert avg_response_time < 2.0, f"Average response time too high: {avg_response_time:.3f}s"
        assert max(response_times) < 5.0, f"Max response time too high: {max(response_times):.3f}s"
        
        # Clean up created users
        for result in successful_requests:
            if result['user_id']:
                api_client.delete(f"{API_ENDPOINT}/users/{result['user_id']}")
    
    def test_get_users_performance(self, api_client):
        """Test GET /users endpoint performance"""
        # Create some test data first
        test_users = []
        for i in range(5):
            response = api_client.put(f"{API_ENDPOINT}/users", json={
                "name": f"Perf Test User {i}",
                "email": f"perftest{i}@example.com"
            })
            if response.status_code == 200:
                test_users.append(response.json()['userid'])
        
        # Test multiple GET requests
        num_requests = 20
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(get_users, requests.Session())
                for _ in range(num_requests)
            ]
            
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Verify all requests succeeded
        successful_requests = [r for r in results if r['status_code'] == 200]
        assert len(successful_requests) == num_requests
        
        # Check response times
        response_times = [r['response_time'] for r in successful_requests]
        avg_response_time = mean(response_times)
        
        print(f"GET /users average response time: {avg_response_time:.3f}s")
        assert avg_response_time < 1.0, f"GET /users response time too high: {avg_response_time:.3f}s"
        
        # Clean up
        for user_id in test_users:
            api_client.delete(f"{API_ENDPOINT}/users/{user_id}")