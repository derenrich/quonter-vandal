
from dataclasses import dataclass
import toolforge
from config import DB_NAME


@dataclass
class LogLine:
    document: str
    oldrevid: int
    currevid: int
    prediction: str
    data: str


CREATE_TABLE = """
CREATE OR REPLACE TABLE results (
    id INT NOT NULL AUTO_INCREMENT,
    document VARCHAR(4096) NOT NULL,
    oldrevid INT NOT NULL,
    currevid INT NOT NULL,
    prediction VARCHAR(4096) NOT NULL,
    data VARCHAR(4096) NOT NULL,
    PRIMARY KEY (id)
);
"""


class ResultsLogger:
    def __init__(self):
        self._tool_db = toolforge.toolsdb(DB_NAME)

    def log(self, log_line: LogLine):
        with self._tool_db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO results (document, oldrevid, currevid, prediction, data)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (log_line.document, log_line.oldrevid,
                 log_line.currevid, log_line.prediction, log_line.data)
            )
        self._tool_db.commit()
