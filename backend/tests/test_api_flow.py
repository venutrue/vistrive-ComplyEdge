from datetime import date


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_end_to_end_platform_flow(client):
    login_resp = client.post("/api/v1/auth/login", json={"email": "admin@acme.test"})
    assert login_resp.status_code == 200
    assert login_resp.json()["mfa_required"] is True

    mfa_resp = client.post("/api/v1/auth/mfa/verify", json={"email": "admin@acme.test", "otp_code": "123456"})
    assert mfa_resp.status_code == 200
    assert mfa_resp.json()["verified"] is True

    tenant_resp = client.post(
        "/api/v1/tenants",
        json={"legal_name": "Acme India Pvt Ltd", "primary_contact_email": "admin@acme.test"},
    )
    assert tenant_resp.status_code == 201
    tenant_id = tenant_resp.json()["id"]

    login_resp = client.post("/api/v1/auth/login", json={"email": "admin@acme.test", "tenant_id": tenant_id})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}", "X-Tenant-ID": tenant_id}

    mfa_resp = client.post("/api/v1/auth/mfa/verify", json={"email": "admin@acme.test", "otp_code": "123456"})
    assert mfa_resp.status_code == 200
    assert mfa_resp.json()["verified"] is True

    role_resp = client.post("/api/v1/users/roles", json={"name": "Compliance Admin"}, headers=headers)
    role_resp = client.post("/api/v1/users/roles", json={"name": "Compliance Admin"})
    assert role_resp.status_code == 201
    role_id = role_resp.json()["id"]

    user_resp = client.post(
        "/api/v1/users",
        json={
            "tenant_id": tenant_id,
            "email": "manager@acme.test",
            "full_name": "Compliance Manager",
            "role_id": role_id,
        },
        headers=headers,
    )
    assert user_resp.status_code == 201

    legal_entity_resp = client.post(
        "/api/v1/legal-entities",
        json={"tenant_id": tenant_id, "name": "Acme Legal Entity", "cin": "U123", "pan": "ABCDE1234F"},
        headers=headers,
    )
    assert legal_entity_resp.status_code == 201
    legal_entity_id = legal_entity_resp.json()["id"]

    establishment_resp = client.post(
        "/api/v1/establishments",
        json={
            "legal_entity_id": legal_entity_id,
            "name": "Bengaluru HQ",
            "state": "Karnataka",
            "employee_count": 150,
        },
        headers=headers,
    )
    assert establishment_resp.status_code == 201
    establishment_id = establishment_resp.json()["id"]

    reg = client.post("/api/v1/rules/regulations", json={"code_name": "Code on Wages"}, headers=headers)
    reg = client.post("/api/v1/rules/regulations", json={"code_name": "Code on Wages"})
    regulation_id = reg.json()["id"]

    rule = client.post(
        "/api/v1/rules",
        json={
            "regulation_id": regulation_id,
            "name": "Monthly wage register",
            "state": "Karnataka",
            "min_employee_threshold": 50,
            "effective_from": str(date.today()),
            "source_reference": "Code on Wages Section X",
        },
        headers=headers,
    )
    rule_id = rule.json()["id"]

    client.post(
        "/api/v1/rules/obligations",
        json={"rule_id": rule_id, "name": "Submit wage statement", "cadence": "monthly", "sla_days": 10},
        headers=headers,
    )

    gen = client.post("/api/v1/tasks/generate", json={"establishment_id": establishment_id}, headers=headers)
    )

    gen = client.post("/api/v1/tasks/generate", json={"establishment_id": establishment_id})
    assert gen.status_code == 201

    filing = client.post(
        "/api/v1/filings",
        json={"establishment_id": establishment_id, "form_name": "Monthly Register", "period_label": "2026-04"},
        headers=headers,
    )
    filing_id = filing.json()["id"]

    ev = client.post(
        "/api/v1/filings/evidence",
        json={"filing_id": filing_id, "file_name": "register.pdf", "storage_path": "s3://bucket/register.pdf"},
        headers=headers,
    )
    assert ev.status_code == 201

    notice = client.post(
        "/api/v1/notices",
        json={"establishment_id": establishment_id, "title": "Inspector notice"},
        headers=headers,
    )
    )
    assert ev.status_code == 201

    notice = client.post("/api/v1/notices", json={"establishment_id": establishment_id, "title": "Inspector notice"})
    assert notice.status_code == 201

    incident = client.post(
        "/api/v1/incidents",
        json={
            "establishment_id": establishment_id,
            "category": "Safety",
            "severity": "medium",
            "summary": "Near miss incident",
        },
        headers=headers,
    )
    assert incident.status_code == 201

    payroll = client.post(
        "/api/v1/payroll/validate",
        json={
            "establishment_id": establishment_id,
            "min_wage": 10000,
            "paid_wage": 11000,
            "overtime_hours": 20,
        },
        headers=headers,
    )
    assert payroll.status_code == 200
    )
    assert payroll.status_code == 200
    assert payroll.json()["compliant"] is True

    notification = client.post(
        "/api/v1/notifications",
        json={
            "tenant_id": tenant_id,
            "channel": "email",
            "subject": "Task due",
            "body": "A compliance task is due soon",
        },
        headers=headers,
    )
    assert notification.status_code == 201
    notification_id = notification.json()["id"]

    sent = client.post(f"/api/v1/notifications/{notification_id}/send", headers=headers)
    assert sent.status_code == 200
    assert sent.json()["status"] == "sent"

    bundle = client.get(f"/api/v1/inspections/{establishment_id}/bundle", headers=headers)
    assert bundle.status_code == 200

    dashboard = client.get("/api/v1/dashboard/summary", headers=headers)
    sent = client.post(f"/api/v1/notifications/{notification_id}/send")
    assert sent.status_code == 200
    assert sent.json()["status"] == "sent"

    bundle = client.get(f"/api/v1/inspections/{establishment_id}/bundle")
    assert bundle.status_code == 200

    dashboard = client.get("/api/v1/dashboard/summary")
    assert dashboard.status_code == 200

    copilot = client.post(
        "/api/v1/copilot/query",
        json={"tenant_id": tenant_id, "question": "What applies to Karnataka establishment?"},
        headers=headers,
    )
    assert copilot.status_code == 200
    assert copilot.json()["requires_human_review"] is True
