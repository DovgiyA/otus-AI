#!/usr/bin/env python
"""
Integration test script for Mini-Survey Application.
Tests both backend API endpoints and database functionality.
"""

import requests
import json
import time
import sqlite3
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
API_BASE = f"{BACKEND_URL}/api"
# Database path - handle both running from root or backend directory
root_db = Path(__file__).parent / "backend" / "survey.db"
backend_db = Path("survey.db")
DB_PATH = root_db if root_db.exists() or not backend_db.exists() else backend_db

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_section(title):
    """Print section header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{title}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_pass(message):
    """Print success message"""
    print(f"{GREEN}✓ {message}{RESET}")

def print_fail(message):
    """Print failure message"""
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    """Print info message"""
    print(f"{YELLOW}ℹ {message}{RESET}")

def test_backend_running():
    """Test if backend is running"""
    print_section("Test 1: Backend Health Check")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        if response.status_code == 200:
            print_pass("Backend is running on port 8000")
            print(f"  Response: {response.json()}")
            return True
        else:
            print_fail(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_fail("Cannot connect to backend on http://localhost:8000")
        print_info("Make sure backend is running: cd backend && python main.py")
        return False
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_get_questions():
    """Test GET /api/questions endpoint"""
    print_section("Test 2: GET /api/questions")
    try:
        response = requests.get(f"{API_BASE}/questions", timeout=5)
        
        if response.status_code != 200:
            print_fail(f"API returned status {response.status_code}")
            return False
        
        questions = response.json()
        
        if not isinstance(questions, list):
            print_fail("Questions response is not a list")
            return False
        
        if len(questions) == 0:
            print_fail("No questions returned")
            return False
        
        print_pass(f"Loaded {len(questions)} questions")
        
        # Print question details
        for q in questions[:3]:
            print(f"  Q{q['id']}: {q['text'][:50]}... [{q['type']}]")
        
        if len(questions) > 3:
            print(f"  ... and {len(questions) - 3} more")
        
        return True
    
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_submit_answers(questions):
    """Test POST /api/answers endpoint"""
    print_section("Test 3: POST /api/answers")
    
    # Prepare test answers
    answers = [
        {"question_id": 1, "answer_value": "Test User"},
        {"question_id": 2, "answer_value": "Developer"},
        {"question_id": 3, "answer_value": "5+ лет"},
        {"question_id": 4, "answer_value": "Python, JavaScript"},
        {"question_id": 5, "answer_value": "Backend"},
    ]
    
    try:
        payload = {"answers": answers}
        response = requests.post(
            f"{API_BASE}/answers",
            json=payload,
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print_fail(f"API returned status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        result = response.json()
        
        if not result.get("success"):
            print_fail("Response indicates failure")
            print(f"  Response: {result}")
            return False
        
        print_pass(f"Successfully submitted {len(answers)} answers")
        print(f"  Message: {result['message']}")
        
        return True
    
    except Exception as e:
        print_fail(f"Error: {e}")
        return False


def test_create_submission():
    """Test POST /api/submissions endpoint (new)"""
    print_section("Test 6: POST /api/submissions (NEW)")
    
    # Prepare test submission
    submission = {
        "participant_name": "Ivan Petrov",
        "participant_email": "ivan@example.com",
        "answers": [
            {"question_id": 1, "answer_value": "Ivan Petrov"},
            {"question_id": 2, "answer_value": "Developer"},
            {"question_id": 3, "answer_value": "3-5 лет"},
            {"question_id": 4, "answer_value": "Python, Go, JavaScript"},
            {"question_id": 5, "answer_value": "Full-Stack"},
        ]
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/submissions",
            json=submission,
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print_fail(f"API returned status {response.status_code}")
            print(f"  Response: {response.text}")
            return None
        
        result = response.json()
        
        if not result.get("success"):
            print_fail("Response indicates failure")
            print(f"  Response: {result}")
            return None
        
        submission_id = result.get("data", {}).get("submission_id")
        print_pass(f"Successfully created submission ID: {submission_id}")
        print(f"  Message: {result['message']}")
        
        return submission_id
    
    except Exception as e:
        print_fail(f"Error: {e}")
        return None


def test_list_submissions():
    """Test GET /api/submissions endpoint (new)"""
    print_section("Test 7: GET /api/submissions (NEW)")
    
    try:
        response = requests.get(
            f"{API_BASE}/submissions",
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print_fail(f"API returned status {response.status_code}")
            return []
        
        submissions = response.json()
        
        if not isinstance(submissions, list):
            print_fail("Submissions response is not a list")
            return []
        
        print_pass(f"Loaded {len(submissions)} submissions")
        
        if len(submissions) > 0:
            print_info("Recent submissions:")
            for sub in submissions[:3]:
                print(f"  - {sub['participant_name']} ({sub['participant_email']}) - {sub['answer_count']} ответов")
        
        return submissions
    
    except Exception as e:
        print_fail(f"Error: {e}")
        return []


def test_get_submission_detail(submission_id):
    """Test GET /api/submissions/{id} endpoint (new)"""
    print_section("Test 8: GET /api/submissions/{id} (NEW)")
    
    try:
        response = requests.get(
            f"{API_BASE}/submissions/{submission_id}",
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print_fail(f"API returned status {response.status_code}")
            return False
        
        submission = response.json()
        
        print_pass(f"Loaded submission details for {submission['participant_name']}")
        print(f"  Email: {submission['participant_email']}")
        print(f"  Answers: {len(submission['answers'])}")
        
        if len(submission['answers']) > 0:
            print_info("First answer:")
            first_ans = submission['answers'][0]
            print(f"  Q: {first_ans['question_text'][:50]}...")
            print(f"  A: {first_ans['answer_value'][:50]}...")
        
        return True
    
    except Exception as e:
        print_fail(f"Error: {e}")
        return False


def test_delete_submission(submission_id):
    """Test DELETE /api/submissions/{id} endpoint (new)"""
    print_section("Test 9: DELETE /api/submissions/{id} (NEW)")
    
    try:
        response = requests.delete(
            f"{API_BASE}/submissions/{submission_id}",
            timeout=5,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            print_fail(f"API returned status {response.status_code}")
            return False
        
        result = response.json()
        
        if not result.get("success"):
            print_fail("Response indicates failure")
            return False
        
        print_pass(f"Successfully deleted submission {submission_id}")
        print(f"  Message: {result['message']}")
        
        return True
    
    except Exception as e:
        print_fail(f"Error: {e}")
        return False

def test_database():
    """Test database has data"""
    print_section("Test 4: Database Verification")
    
    if not DB_PATH.exists():
        print_fail(f"Database file not found at {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Check questions table
        cursor.execute("SELECT COUNT(*) FROM questions")
        q_count = cursor.fetchone()[0]
        
        if q_count == 0:
            print_fail("No questions in database")
            conn.close()
            return False
        
        print_pass(f"Database has {q_count} questions")
        
        # Check answers table
        cursor.execute("SELECT COUNT(*) FROM answers")
        a_count = cursor.fetchone()[0]
        
        print_pass(f"Database has {a_count} answers")
        
        if a_count > 0:
            # Show recent answers
            cursor.execute("""
                SELECT a.answer_value, q.text
                FROM answers a
                JOIN questions q ON a.question_id = q.id
                ORDER BY a.created_at DESC
                LIMIT 3
            """)
            
            recent = cursor.fetchall()
            print_info("Recent answers:")
            for answer, question in recent:
                print(f"  - {question[:40]}... → {answer[:40]}...")
        
        conn.close()
        return True
    
    except Exception as e:
        print_fail(f"Database error: {e}")
        return False

def test_cors():
    """Test CORS headers"""
    print_section("Test 5: CORS Configuration")
    
    try:
        response = requests.options(
            f"{API_BASE}/questions",
            headers={"Origin": "http://localhost:3000"},
            timeout=5
        )
        
        cors_origin = response.headers.get("Access-Control-Allow-Origin", "Not set")
        cors_methods = response.headers.get("Access-Control-Allow-Methods", "Not set")
        
        print_pass(f"CORS Origin: {cors_origin}")
        print_pass(f"CORS Methods: {cors_methods}")
        
        if "http://localhost:3000" in cors_origin or "*" in cors_origin:
            print_pass("CORS configured for frontend")
            return True
        else:
            print_fail("CORS may not be configured for localhost:3000")
            return False
    
    except Exception as e:
        print_fail(f"CORS check error: {e}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}Mini-Survey Application - Integration Tests{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Run tests
    results = []
    
    # Test 1: Backend running
    if not test_backend_running():
        print_fail("Backend is not running. Cannot continue tests.")
        return
    
    results.append(("Backend Health Check", True))
    
    # Test 2: Get questions
    if test_get_questions():
        results.append(("GET /api/questions", True))
    else:
        results.append(("GET /api/questions", False))
    
    time.sleep(0.5)
    
    # Test 3: Submit answers (legacy endpoint)
    if test_submit_answers(None):
        results.append(("POST /api/answers (legacy)", True))
    else:
        results.append(("POST /api/answers (legacy)", False))
    
    time.sleep(0.5)
    
    # Test 4: Database
    if test_database():
        results.append(("Database Verification", True))
    else:
        results.append(("Database Verification", False))
    
    # Test 5: CORS
    if test_cors():
        results.append(("CORS Configuration", True))
    else:
        results.append(("CORS Configuration", False))
    
    time.sleep(0.5)
    
    # Test 6: Create submission (NEW)
    submission_id = test_create_submission()
    if submission_id:
        results.append(("POST /api/submissions (NEW)", True))
    else:
        results.append(("POST /api/submissions (NEW)", False))
    
    time.sleep(0.5)
    
    # Test 7: List submissions (NEW)
    submissions = test_list_submissions()
    if len(submissions) > 0:
        results.append(("GET /api/submissions (NEW)", True))
    else:
        results.append(("GET /api/submissions (NEW)", False))
    
    time.sleep(0.5)
    
    # Test 8: Get submission detail (NEW)
    if submission_id and test_get_submission_detail(submission_id):
        results.append(("GET /api/submissions/{id} (NEW)", True))
    elif not submission_id:
        results.append(("GET /api/submissions/{id} (NEW)", False))
    
    time.sleep(0.5)
    
    # Test 9: Delete submission (NEW)
    if submission_id and test_delete_submission(submission_id):
        results.append(("DELETE /api/submissions/{id} (NEW)", True))
    elif not submission_id:
        results.append(("DELETE /api/submissions/{id} (NEW)", False))
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = f"{GREEN}PASS{RESET}" if success else f"{RED}FAIL{RESET}"
        print(f"  {status} - {name}")
    
    print()
    if passed == total:
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}✓ All {total} tests passed!{RESET}")
        print(f"{GREEN}Application is ready.{RESET}")
        print(f"{GREEN}{'='*60}{RESET}")
    else:
        print(f"{RED}{'='*60}{RESET}")
        print(f"{RED}✗ {total - passed}/{total} tests failed.{RESET}")
        print(f"{RED}Please check errors above and restart.{RESET}")
        print(f"{RED}{'='*60}{RESET}")

if __name__ == "__main__":
    main()
