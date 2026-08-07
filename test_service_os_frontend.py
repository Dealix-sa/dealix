from pathlib import Path


def test_service_os_frontend_page_exists():
    page = Path('apps/web/app/service-os/page.tsx')
    assert page.exists()
    text = page.read_text(encoding='utf-8')
    assert 'Dealix Service OS' in text
    assert 'serviceOsSnapshot' in text
    assert '/book' in text


def test_service_os_snapshot_contract_exists():
    snapshot = Path('apps/web/lib/service-os-snapshot.ts')
    assert snapshot.exists()
    text = snapshot.read_text(encoding='utf-8')
    assert 'service_os_ready' in text
    assert 'live_sends: 0' in text
    assert 'final_commitments: 0' in text
    assert 'approvalGates' in text


def test_service_os_snapshot_generator_exists():
    generator = Path('generate_service_os_snapshot.py')
    assert generator.exists()
    text = generator.read_text(encoding='utf-8')
    assert 'SERVICE_OS_FRONTEND_SNAPSHOT_READY=1' in text
    assert 'run_os16.build_payload' in text
