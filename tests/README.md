# Users API Test Suite

This directory contains comprehensive tests for the Users API Lambda function.

## Test Structure

```
tests/
├── unit/                 # Unit tests using mocked DynamoDB
│   └── test_handler.py   # Tests for Lambda handler logic
├── integration/          # Integration tests against deployed API
│   └── test_api.py       # End-to-end API tests
├── performance/          # Performance and load tests
│   └── test_load.py      # Concurrent request testing
└── requirements.txt      # Test dependencies
```

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r tests/requirements.txt
```

### Unit Tests

Run unit tests (no deployment required):
```bash
pytest tests/unit/ -v
```

### Integration Tests

Set your deployed API endpoint and run integration tests:
```bash
export API_ENDPOINT=https://your-api-id.execute-api.region.amazonaws.com/stage
pytest tests/integration/ -v
```

### Performance Tests

Run performance tests against deployed API:
```bash
export API_ENDPOINT=https://your-api-id.execute-api.region.amazonaws.com/stage
pytest tests/performance/ -v
```

### All Tests

Use the test runner to execute all test suites:
```bash
python run_tests.py
```

## Test Coverage

### Unit Tests
- ✅ GET /users - List all users
- ✅ GET /users/{userid} - Get user by ID
- ✅ GET /users/{userid} - Non-existent user
- ✅ PUT /users - Create new user
- ✅ PUT /users - Create user with existing ID
- ✅ PUT /users/{userid} - Update existing user
- ✅ DELETE /users/{userid} - Delete user
- ✅ Unsupported routes
- ✅ Invalid JSON handling
- ✅ Error handling

### Integration Tests
- ✅ Full CRUD operations
- ✅ CORS headers validation
- ✅ Error scenarios
- ✅ Data persistence verification

### Performance Tests
- ✅ Concurrent user creation
- ✅ GET endpoint performance
- ✅ Response time validation

## Test Data

Unit tests use mocked DynamoDB with predefined test users:
- John Doe (ID: f8216640-91a2-11eb-8ab9-57aa454facef)
- Jane Doe (ID: 31a9f940-917b-11eb-9054-67837e2c40b0)

Integration and performance tests create and clean up their own test data.