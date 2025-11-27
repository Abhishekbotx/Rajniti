"""
Simple API Routes for Rajniti Election Data

Clean Flask routes following MVC pattern:
- Routes handle HTTP requests/responses
- Controllers handle business logic
- Models define data structure
- Services handle data access
"""

import logging
from flask import Blueprint, jsonify, request

from app.controllers import (
    CandidateController,
    ConstituencyController,
    ElectionController,
    PartyController,
)

logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# Initialize controllers
election_controller = ElectionController()
candidate_controller = CandidateController()
party_controller = PartyController()
constituency_controller = ConstituencyController()


# ==================== ELECTION ROUTES ====================


@api_bp.route("/elections", methods=["GET"])
def get_elections():
    """Get all elections"""
    try:
        elections = election_controller.get_all_elections()
        return jsonify({"success": True, "data": elections, "total": len(elections)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/elections/<election_id>", methods=["GET"])
def get_election(election_id):
    """Get election details"""
    try:
        election = election_controller.get_election_by_id(election_id)
        if not election:
            return jsonify({"success": False, "error": "Election not found"}), 404

        return jsonify({"success": True, "data": election})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ==================== CANDIDATE ROUTES ====================


@api_bp.route("/candidates/search", methods=["GET"])
def search_candidates():
    """Search candidates"""
    try:
        query = request.args.get("q", "").strip()
        election_id = request.args.get("election_id")
        limit = request.args.get("limit", type=int)

        if not query:
            return (
                jsonify({"success": False, "error": 'Query parameter "q" is required'}),
                400,
            )

        results = candidate_controller.search_candidates(query, election_id, limit)

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/elections/<election_id>/candidates", methods=["GET"])
def get_candidates_by_election(election_id):
    """Get candidates by election"""
    try:
        limit = request.args.get("limit", type=int)
        results = candidate_controller.get_candidates_by_election(election_id, limit)

        if not results:
            return jsonify({"success": False, "error": "Election not found"}), 404

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/candidates/<candidate_id>", methods=["GET"])
def get_candidate_by_id(candidate_id):
    """Get candidate details by ID (without needing election_id)"""
    try:
        candidate = candidate_controller.get_candidate_by_id_only(candidate_id)

        if not candidate:
            return jsonify({"success": False, "error": "Candidate not found"}), 404

        return jsonify({"success": True, "data": candidate})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/elections/<election_id>/candidates/<candidate_id>", methods=["GET"])
def get_candidate(election_id, candidate_id):
    """Get candidate details"""
    try:
        candidate = candidate_controller.get_candidate_by_id(candidate_id, election_id)

        if not candidate:
            return jsonify({"success": False, "error": "Candidate not found"}), 404

        return jsonify({"success": True, "data": candidate})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/candidates/party/<party_name>", methods=["GET"])
def get_candidates_by_party(party_name):
    """Get candidates by party"""
    try:
        election_id = request.args.get("election_id")
        results = candidate_controller.get_candidates_by_party(party_name, election_id)

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route(
    "/elections/<election_id>/constituencies/<constituency_id>/candidates",
    methods=["GET"],
)
def get_candidates_by_constituency(election_id, constituency_id):
    """Get candidates by constituency"""
    try:
        results = candidate_controller.get_candidates_by_constituency(
            constituency_id, election_id
        )

        if not results:
            return (
                jsonify(
                    {"success": False, "error": "Election or constituency not found"}
                ),
                404,
            )

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/candidates/winners", methods=["GET"])
def get_all_winners():
    """Get all winning candidates"""
    try:
        election_id = request.args.get("election_id")
        results = candidate_controller.get_winning_candidates(election_id)

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== PARTY ROUTES ====================


@api_bp.route("/elections/<election_id>/parties", methods=["GET"])
def get_parties_by_election(election_id):
    """Get parties by election"""
    try:
        results = party_controller.get_parties_by_election(election_id)

        if not results:
            return jsonify({"success": False, "error": "Election not found"}), 404

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/elections/<election_id>/parties/<party_name>", methods=["GET"])
def get_party_by_name(election_id, party_name):
    """Get party details"""
    try:
        results = party_controller.get_party_by_name(party_name, election_id)

        if not results:
            return (
                jsonify(
                    {"success": False, "error": "Party not found in this election"}
                ),
                404,
            )

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/parties/<party_name>/performance", methods=["GET"])
def get_party_performance(party_name):
    """Get party performance"""
    try:
        election_id = request.args.get("election_id")
        results = party_controller.get_party_performance(party_name, election_id)

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/parties", methods=["GET"])
def get_all_parties():
    """Get all parties"""
    try:
        results = party_controller.get_all_parties()

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== CONSTITUENCY ROUTES ====================


@api_bp.route("/elections/<election_id>/constituencies", methods=["GET"])
def get_constituencies_by_election(election_id):
    """Get constituencies by election"""
    try:
        results = constituency_controller.get_constituencies_by_election(election_id)

        if not results:
            return jsonify({"success": False, "error": "Election not found"}), 404

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route(
    "/elections/<election_id>/constituencies/<constituency_id>", methods=["GET"]
)
def get_constituency(election_id, constituency_id):
    """Get constituency details"""
    try:
        results = constituency_controller.get_constituency_by_id(
            constituency_id, election_id
        )

        if not results:
            return jsonify({"success": False, "error": "Constituency not found"}), 404

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/constituencies/state/<state_code>", methods=["GET"])
def get_constituencies_by_state(state_code):
    """Get constituencies by state"""
    try:
        results = constituency_controller.get_constituencies_by_state(state_code)

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route(
    "/elections/<election_id>/constituencies/<constituency_id>/results", methods=["GET"]
)
def get_constituency_results(election_id, constituency_id):
    """Get constituency results"""
    try:
        results = constituency_controller.get_constituency_results(
            constituency_id, election_id
        )

        if not results:
            return jsonify({"success": False, "error": "Constituency not found"}), 404

        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ==================== ROOT & HEALTH CHECK ====================


@api_bp.route("/", methods=["GET"])
def api_root():
    """API root endpoint"""
    return jsonify(
        {
            "success": True,
            "message": "Welcome to Rajniti Election Data API",
            "version": "1.0.0",
            "endpoints": {
                "elections": "/api/v1/elections",
                "candidates": "/api/v1/candidates/search?q=<query>",
                "parties": "/api/v1/parties",
                "questions": "/api/v1/questions",
                "ask_question": "/api/v1/questions/ask",
                "users": "/api/v1/users",
                "health": "/api/v1/health",
                "documentation": "/api/v1/doc",
            },
            "documentation": "Visit /api/v1/doc for complete API documentation",
        }
    )


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    from app.core.database import check_db_health

    db_status = check_db_health()

    return jsonify(
        {
            "success": True,
            "message": "Rajniti API is healthy",
            "version": "1.0.0",
            "database": {
                "connected": db_status,
                "status": "healthy" if db_status else "not configured or unavailable",
            },
        }
    )


@api_bp.route("/doc", methods=["GET"])
def api_documentation():
    """Complete API documentation in JSON format for developers"""
    return jsonify(
        {
            "success": True,
            "api_version": "1.0.0",
            "base_url": "/api/v1",
            "description": "Rajniti Election Data API - Complete endpoint documentation",
            "endpoints": {
                "root": {
                    "path": "/api/v1/",
                    "method": "GET",
                    "description": "API root with endpoint list",
                    "response": {"success": True, "message": "...", "endpoints": "..."},
                },
                "health": {
                    "path": "/api/v1/health",
                    "method": "GET",
                    "description": "Health check with database status",
                    "response": {
                        "success": True,
                        "message": "Rajniti API is healthy",
                        "version": "1.0.0",
                        "database": {"connected": True, "status": "healthy"},
                    },
                },
                "elections": {
                    "list": {
                        "path": "/api/v1/elections",
                        "method": "GET",
                        "description": "Get all elections",
                        "query_params": None,
                        "response": {"success": True, "data": [], "total": 0},
                    },
                    "details": {
                        "path": "/api/v1/elections/{election_id}",
                        "method": "GET",
                        "description": "Get election details",
                        "path_params": {"election_id": "string - e.g., lok-sabha-2024"},
                        "response": {"success": True, "data": {}},
                    },
                    "candidates": {
                        "path": "/api/v1/elections/{election_id}/candidates",
                        "method": "GET",
                        "description": "Get candidates by election",
                        "query_params": {"limit": "integer (optional)"},
                        "response": {"success": True, "data": []},
                    },
                    "constituencies": {
                        "path": "/api/v1/elections/{election_id}/constituencies",
                        "method": "GET",
                        "description": "Get constituencies by election",
                        "response": {"success": True, "data": []},
                    },
                    "parties": {
                        "path": "/api/v1/elections/{election_id}/parties",
                        "method": "GET",
                        "description": "Get parties by election",
                        "response": {"success": True, "data": []},
                    },
                },
                "candidates": {
                    "search": {
                        "path": "/api/v1/candidates/search",
                        "method": "GET",
                        "description": "Search candidates by name",
                        "query_params": {
                            "q": "string (required) - search query",
                            "election_id": "string (optional)",
                            "limit": "integer (optional)",
                        },
                        "response": {"success": True, "data": {"candidates": []}},
                    },
                    "by_id": {
                        "path": "/api/v1/candidates/{candidate_id}",
                        "method": "GET",
                        "description": "Get candidate by ID",
                        "path_params": {"candidate_id": "string"},
                        "response": {"success": True, "data": {}},
                    },
                    "winners": {
                        "path": "/api/v1/candidates/winners",
                        "method": "GET",
                        "description": "Get all winning candidates",
                        "query_params": {"election_id": "string (optional)"},
                        "response": {"success": True, "data": []},
                    },
                    "by_party": {
                        "path": "/api/v1/candidates/party/{party_name}",
                        "method": "GET",
                        "description": "Get candidates by party",
                        "path_params": {"party_name": "string - URL encoded"},
                        "query_params": {"election_id": "string (optional)"},
                        "response": {"success": True, "data": []},
                    },
                    "by_constituency": {
                        "path": "/api/v1/elections/{election_id}/constituencies/{constituency_id}/candidates",
                        "method": "GET",
                        "description": "Get candidates by constituency",
                        "path_params": {
                            "election_id": "string",
                            "constituency_id": "string",
                        },
                        "response": {"success": True, "data": []},
                    },
                },
                "constituencies": {
                    "by_election": {
                        "path": "/api/v1/elections/{election_id}/constituencies",
                        "method": "GET",
                        "description": "Get constituencies by election",
                        "response": {"success": True, "data": []},
                    },
                    "details": {
                        "path": "/api/v1/elections/{election_id}/constituencies/{constituency_id}",
                        "method": "GET",
                        "description": "Get constituency details",
                        "path_params": {
                            "election_id": "string",
                            "constituency_id": "string",
                        },
                        "response": {"success": True, "data": {}},
                    },
                    "results": {
                        "path": "/api/v1/elections/{election_id}/constituencies/{constituency_id}/results",
                        "method": "GET",
                        "description": "Get constituency results",
                        "path_params": {
                            "election_id": "string",
                            "constituency_id": "string",
                        },
                        "response": {"success": True, "data": {}},
                    },
                    "by_state": {
                        "path": "/api/v1/constituencies/state/{state_code}",
                        "method": "GET",
                        "description": "Get constituencies by state",
                        "path_params": {"state_code": "string - e.g., DL, MH"},
                        "response": {"success": True, "data": []},
                    },
                },
                "parties": {
                    "list": {
                        "path": "/api/v1/parties",
                        "method": "GET",
                        "description": "Get all parties",
                        "response": {"success": True, "data": []},
                    },
                    "by_election": {
                        "path": "/api/v1/elections/{election_id}/parties",
                        "method": "GET",
                        "description": "Get parties by election",
                        "response": {"success": True, "data": []},
                    },
                    "details": {
                        "path": "/api/v1/elections/{election_id}/parties/{party_name}",
                        "method": "GET",
                        "description": "Get party details in election",
                        "path_params": {
                            "election_id": "string",
                            "party_name": "string - URL encoded",
                        },
                        "response": {"success": True, "data": {}},
                    },
                    "performance": {
                        "path": "/api/v1/parties/{party_name}/performance",
                        "method": "GET",
                        "description": "Get party performance",
                        "path_params": {"party_name": "string - URL encoded"},
                        "query_params": {"election_id": "string (optional)"},
                        "response": {"success": True, "data": {}},
                    },
                },
                "questions": {
                    "list": {
                        "path": "/api/v1/questions",
                        "method": "GET",
                        "description": "Get predefined questions",
                        "response": {"success": True, "data": {"questions": []}},
                    },
                    "ask": {
                        "path": "/api/v1/questions/ask",
                        "method": "POST",
                        "description": "Ask a question (semantic search)",
                        "request_body": {
                            "question": "string (required)",
                            "candidate_id": "string (optional)",
                            "n_results": "integer (optional, default: 5)",
                        },
                        "response": {
                            "success": True,
                            "data": {"answer": "...", "candidates": []},
                        },
                    },
                    "answer_predefined": {
                        "path": "/api/v1/questions/{question_id}/answer",
                        "method": "GET",
                        "description": "Answer predefined question",
                        "path_params": {"question_id": "integer"},
                        "query_params": {
                            "candidate_id": "string (optional)",
                            "n_results": "integer (optional, default: 5)",
                        },
                        "response": {
                            "success": True,
                            "data": {"answer": "...", "candidates": []},
                        },
                    },
                },
                "users": {
                    "sync": {
                        "path": "/api/v1/users/sync",
                        "method": "POST",
                        "description": "Sync user from NextAuth",
                        "request_body": {
                            "id": "string (required)",
                            "email": "string (required)",
                            "name": "string (optional)",
                            "profile_picture": "string (optional)",
                        },
                        "response": {"success": True, "data": {}},
                    },
                    "get": {
                        "path": "/api/v1/users/{user_id}",
                        "method": "GET",
                        "description": "Get user by ID",
                        "path_params": {"user_id": "string"},
                        "response": {"success": True, "data": {}},
                    },
                    "update": {
                        "path": "/api/v1/users/{user_id}",
                        "method": "PATCH/PUT",
                        "description": "Update user profile",
                        "path_params": {"user_id": "string"},
                        "request_body": {
                            "username": "string (optional)",
                            "name": "string (optional)",
                            "state": "string (optional)",
                            "city": "string (optional)",
                            "age_group": "string (optional)",
                            "pincode": "string (optional)",
                            "political_ideology": "string (optional)",
                            "onboarding_completed": "boolean (optional)",
                        },
                        "response": {"success": True, "data": {}, "message": "..."},
                    },
                    "check_username": {
                        "path": "/api/v1/users/check-username",
                        "method": "POST",
                        "description": "Check username availability",
                        "request_body": {
                            "username": "string (required)",
                            "user_id": "string (optional)",
                        },
                        "response": {"success": True, "available": True},
                    },
                },
            },
            "response_format": {
                "success": "boolean - indicates if request was successful",
                "data": "object/array - response data",
                "error": "string - error message (only if success is false)",
                "total": "integer - total count (for list endpoints)",
            },
            "status_codes": {
                "200": "Success",
                "400": "Bad Request - invalid parameters",
                "404": "Not Found - resource not found",
                "500": "Internal Server Error",
                "503": "Service Unavailable - service not configured",
            },
            "examples": {
                "search_candidates": {
                    "request": "GET /api/v1/candidates/search?q=modi&election_id=lok-sabha-2024",
                    "response": {
                        "success": True,
                        "data": {
                            "candidates": [
                                {
                                    "candidate_name": "NARENDRA MODI",
                                    "party": "Bharatiya Janata Party",
                                    "constituency": "Varanasi",
                                }
                            ]
                        },
                    },
                },
                "ask_question": {
                    "request": "POST /api/v1/questions/ask",
                    "request_body": {
                        "question": "Who are the candidates with business background?",
                        "n_results": 5,
                    },
                    "response": {
                        "success": True,
                        "data": {
                            "answer": "Based on the search...",
                            "candidates": [],
                        },
                    },
                },
            },
        }
    )


# ==================== QUESTIONS ROUTES ====================


# Lazy initialization for questions service
_questions_service = None


def get_questions_service():
    """Lazy initialization of QuestionsService to avoid import errors."""
    global _questions_service
    if _questions_service is None:
        try:
            from app.services.questions_service import QuestionsService

            _questions_service = QuestionsService()
        except Exception as e:
            logger.warning(f"Failed to initialize QuestionsService: {e}")
            return None
    return _questions_service


@api_bp.route("/questions", methods=["GET"])
def get_predefined_questions():
    """Get top 5 predefined questions based on candidate model."""
    try:
        from app.schemas.questions import PREDEFINED_QUESTIONS

        return jsonify(
            {
                "success": True,
                "data": {
                    "questions": PREDEFINED_QUESTIONS,
                    "total": len(PREDEFINED_QUESTIONS),
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/questions/ask", methods=["POST"])
def ask_question():
    """Ask a question and get answers from the vector database."""
    try:
        data = request.get_json()

        if not data or not data.get("question"):
            return (
                jsonify({"success": False, "error": "Question is required"}),
                400,
            )

        question = data.get("question")
        candidate_id = data.get("candidate_id")
        n_results = data.get("n_results", 5)

        questions_service = get_questions_service()
        if not questions_service:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Questions service not available. Vector DB may not be configured.",
                    }
                ),
                503,
            )

        result = questions_service.answer_question(
            question=question, candidate_id=candidate_id, n_results=n_results
        )

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in ask_question: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/questions/<question_id>/answer", methods=["GET"])
def answer_predefined_question(question_id):
    """Answer a predefined question by its ID."""
    try:
        candidate_id = request.args.get("candidate_id")
        n_results = request.args.get("n_results", default=5, type=int)

        questions_service = get_questions_service()
        if not questions_service:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Questions service not available. Vector DB may not be configured.",
                    }
                ),
                503,
            )

        result = questions_service.answer_predefined_question(
            question_id=question_id, candidate_id=candidate_id, n_results=n_results
        )

        if not result.get("success"):
            return jsonify(result), 404

        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in answer_predefined_question: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
