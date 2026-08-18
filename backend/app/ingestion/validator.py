from typing import Dict, Any, Tuple, Optional
from pydantic import ValidationError
from app.schemas.job import NormalizedJobCreate
from app.utils.logger import logger

class RecordValidator:
    """
    Validates normalized job records against Pydantic schemas.
    Catches invalid records without breaking pipeline execution.
    """

    @staticmethod
    def validate(normalized_dict: Dict[str, Any]) -> Tuple[Optional[NormalizedJobCreate], Optional[str]]:
        try:
            record = NormalizedJobCreate(**normalized_dict)
            
            # Additional custom validations
            if not record.title.strip():
                return None, "Validation failed: 'title' cannot be blank."
            if not record.company.strip():
                return None, "Validation failed: 'company' cannot be blank."
            if not record.source_url.strip():
                return None, "Validation failed: 'source_url' cannot be blank."

            return record, None

        except ValidationError as exc:
            error_details = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in exc.errors()])
            logger.warning(f"Record failed Pydantic validation: {error_details}")
            return None, f"Schema validation error: {error_details}"
        except Exception as exc:
            logger.error(f"Unexpected validation exception: {exc}")
            return None, f"Unexpected validation error: {str(exc)}"
