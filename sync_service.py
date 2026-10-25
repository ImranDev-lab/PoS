import json
from sqlalchemy.orm import Session
from ..models import OfflineSyncQueue


def get_pending_sync(db: Session):
    return db.query(OfflineSyncQueue).filter(OfflineSyncQueue.status == "pending").all()


def apply_offline_changes(db: Session, payload: list):
    results = []
    for item in payload:
        queue = OfflineSyncQueue(
            table_name=item.get("table_name", ""),
            record_id=item.get("record_id", ""),
            operation=item.get("operation", "insert"),
            payload=json.dumps(item.get("payload", {})),
        )
        db.add(queue)
        results.append({"queued": True, "record_id": item.get("record_id")})
    db.commit()
    return results