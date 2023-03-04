from sqlalchemy import and_
from dataaccess.entity.procReport import ProcReport


def store_user_ast_proc_repot(data: dict):
    proc_report = ProcReport.query.filter(and_())
