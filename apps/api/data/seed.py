"""
Synthetic seed data for YemenJPT development.
SYNTHETIC / DEVELOPMENT DATA — not real intelligence.
All claims are fictional fixtures.
"""
import asyncio
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'packages', 'contracts', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import httpx

API = "http://localhost:8000"

SEED_DATA = {
    "cases": [
        {
            "title": "[SYNTHETIC] Yemen Currency Crisis Investigation",
            "description": "Development fixture: tracks fictional currency depreciation events.",
            "research_question": "What are the synthetic causes of currency instability?",
        },
        {
            "title": "[SYNTHETIC] Aden Infrastructure Report",
            "description": "Development fixture: synthetic infrastructure change detection.",
            "research_question": "What synthetic infrastructure changes occurred in the Aden fixture?",
        },
    ],
    "research_items": [
        {
            "question": "[SYNTHETIC] The fictional entity Alpha-1 claimed currency reserves dropped 40%.",
            "case_index": 0,
        },
        {
            "question": "[SYNTHETIC] Counter-claim: Beta-Org stated reserves increased 10% in the same period.",
            "case_index": 0,
        },
        {
            "question": "[SYNTHETIC] Infrastructure observation: Bridge-X in fictional Aden location shows change.",
            "case_index": 1,
        },
    ],
}

async def seed():
    print("Seeding YemenJPT with SYNTHETIC development data...")
    async with httpx.AsyncClient(base_url=API, timeout=30) as client:
        # Check API health
        health = await client.get("/health")
        if health.status_code != 200:
            print(f"ERROR: API not running at {API}")
            return

        case_ids = []

        # Create cases
        for case_data in SEED_DATA["cases"]:
            r = await client.post("/api/v1/cases", json=case_data)
            if r.status_code == 201:
                cid = r.json()["case_id"]
                case_ids.append(cid)
                print(f"✓ Created case: {case_data['title'][:50]}... [{cid}]")
            else:
                print(f"✗ Failed case: {r.status_code}")
                case_ids.append(None)

        await asyncio.sleep(0.2)

        # Submit research items
        for item in SEED_DATA["research_items"]:
            ci = case_ids[item["case_index"]]
            if ci:
                r = await client.post("/api/v1/research", json={
                    "question": item["question"],
                    "case_id": ci,
                })
                if r.status_code == 200:
                    print(f"✓ Research submitted: mission={r.json()['mission_id']}")
                else:
                    print(f"✗ Failed research: {r.status_code}")

        await asyncio.sleep(2)

        # Show final state
        cases_r = await client.get("/api/v1/cases")
        print(f"\nFinal state: {cases_r.json()['total']} cases in system")
        for c in cases_r.json()["items"]:
            print(f"  • [{c['status']}] {c['title'][:60]}")

    print("\nSeed complete. All data is SYNTHETIC / DEVELOPMENT fixtures.")

if __name__ == "__main__":
    asyncio.run(seed())
