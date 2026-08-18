from abc import ABC, abstractmethod
from typing import List, Dict, Any

class JobSource(ABC):
    """
    Abstract base class for all job ingestion data source adapters.
    Decouples ingestion pipeline logic from source-specific protocols (RSS, REST, Mock).
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Returns the unique identifier string for this job source."""
        pass

    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """
        Fetches raw job records from the remote source.
        Returns a list of unparsed, raw dictionaries representing job items.
        """
        pass
