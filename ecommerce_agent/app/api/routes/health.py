from fastapi import APIRouter

from tests.test_setup import test_llm

router = APIRouter(prefix="/health")

@router.get("/")
def health():
    return {"status": "ok", "agents": ["supervisor", "support", "operations", "research"]}

@router.get("/llm")
def llm_health() -> dict[str, str]:
    return test_llm()