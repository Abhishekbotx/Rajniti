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
                "health": "/api/v1/health",
            },
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
        from app.services.questions_service import PREDEFINED_QUESTIONS

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
