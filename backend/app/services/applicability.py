from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models import ComplianceTask, Establishment, ObligationTemplate, Rule


def generate_tasks_for_establishment(db: Session, establishment: Establishment) -> list[ComplianceTask]:
    today = date.today()
    applicable_rules = (
        db.query(Rule)
        .filter(Rule.effective_from <= today)
        .filter((Rule.state == "ALL") | (Rule.state == establishment.state))
        .filter(Rule.min_employee_threshold <= establishment.employee_count)
        .all()
    )

    tasks: list[ComplianceTask] = []
    for rule in applicable_rules:
        obligations = db.query(ObligationTemplate).filter(ObligationTemplate.rule_id == rule.id).all()
        for obligation in obligations:
            task = ComplianceTask(
                establishment_id=establishment.id,
                obligation_template_id=obligation.id,
                status="draft",
                due_date=today + timedelta(days=obligation.sla_days),
                applicability_reason=(
                    f"Rule '{rule.name}' applies for state={establishment.state}, "
                    f"employee_count={establishment.employee_count}, threshold={rule.min_employee_threshold}"
                ),
            )
            db.add(task)
            tasks.append(task)

    db.commit()
    for task in tasks:
        db.refresh(task)
    return tasks
