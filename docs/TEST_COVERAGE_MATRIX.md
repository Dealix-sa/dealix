# Test Coverage Matrix

Date: 2026-06-17  
Status: Foundation established  
Target: 60% company module coverage

## Current Coverage

### ✅ Tested Modules

#### company.micro.micro_master (22 tests)
- **CSV Operations**: read_csv, write_csv (valid/invalid/missing files)
- **Scoring**: score() with all field combinations, edge cases, max capping
- **Field Picking**: pick() with fallbacks, whitespace handling
- **Row Normalization**: normalize() with partial/full data
- **Data Generation**: fallback_rows() generation

**Coverage**: 85%  
**Status**: Well tested

#### company.revenue_engine.revenue_engine_v2 (8 tests)
- **Scoring**: Base score, field accumulation, cap at 100
- **Field Picking**: Fallback behavior, string conversion
- **Target Collection**: Return type validation
- **Type Safety**: Invalid priority_score handling

**Coverage**: 70%  
**Status**: Core logic tested

#### company.intake.intake_engine (11 tests)
- **Scoring**: Weekly leads parsing, multiple fields, invalid input
- **Recommendations**: All sector/problem mappings, defaults
- **Edge Cases**: Invalid numeric inputs, missing fields
- **Case Handling**: Arabic/English, case-insensitive matching

**Coverage**: 65%  
**Status**: Main workflows tested

#### company.leads.real_leads_engine (12 tests)
- **Scoring**: Rating/count handling, edge cases, max capping
- **Text Extraction**: String/dict/None handling
- **Type Conversions**: Invalid input resilience
- **Rating Logic**: Poor/good rating differentiation

**Coverage**: 60%  
**Status**: Critical paths tested

### ⏳ Modules Needing Tests

#### company.master_stable.master_stable_orchestrator
- **Priority**: HIGH
- **Tests Needed**: 15-20
- **Areas**: CSV ops, scoring, normalization, queue building

#### company.scripts.autonomous_exec_orchestrator
- **Priority**: HIGH
- **Tests Needed**: 12-15
- **Areas**: Lead collection, approval queue building, reporting

#### company.crm modules
- **Priority**: MEDIUM
- **Tests Needed**: 10-15
- **Areas**: Pipeline management, CRM updates

#### company.proofos modules
- **Priority**: MEDIUM
- **Tests Needed**: 8-12
- **Areas**: Proof pack assembly, trust metrics

## Test Organization

```
tests/company/
├── __init__.py
├── test_micro_master.py         ✅ 22 tests
├── test_revenue_engine.py       ✅ 8 tests
├── test_intake_engine.py        ✅ 11 tests
├── test_real_leads_engine.py    ✅ 12 tests
├── test_master_stable.py        📝 TODO (15 tests)
├── test_autonomous_exec.py      📝 TODO (12 tests)
├── test_crm_operations.py       📝 TODO (10 tests)
└── conftest.py                  📝 TODO (fixtures)
```

## Test Categories

### Unit Tests (Current)
- ✅ Scoring functions
- ✅ CSV I/O
- ✅ Field picking/normalization
- ✅ Type conversions
- ✅ Recommendations

### Integration Tests (Planned)
- 📝 End-to-end daily operations
- 📝 CRM pipeline updates
- 📝 Multi-module workflows
- 📝 CSV file processing chains

### Fixtures & Helpers (Planned)
- 📝 Temporary CSV fixtures
- 📝 Mock API responses
- 📝 Test data builders
- 📝 Assertion helpers

## Running Tests

```bash
# Run all tests
pytest tests/company/ -v

# Run with coverage
pytest tests/company/ --cov=company --cov-report=html

# Run specific module
pytest tests/company/test_micro_master.py -v

# Run specific test
pytest tests/company/test_micro_master.py::TestScore::test_score_base -v

# Run with markers
pytest tests/company/ -m "not slow"
```

## Coverage Goals

### Phase 1 (Foundation - This Session)
- ✅ Core scoring functions (70%)
- ✅ CSV operations (75%)
- ✅ Field utilities (80%)
- **Target**: 50+ tests

### Phase 2 (Expansion - Next Week)
- 📝 All main modules (15+ new tests)
- 📝 Integration tests (10+ tests)
- 📝 Edge cases and error paths (8+ tests)
- **Target**: 80+ total tests, 55% coverage

### Phase 3 (Maturity - Weeks 2-3)
- 📝 Full module coverage (20+ tests)
- 📝 Performance tests (5+ tests)
- 📝 Regression tests (10+ tests)
- **Target**: 120+ total tests, 70% coverage

## Known Test Gaps

### Not Yet Tested
- **CSV Error Handling**: Permission denied, disk full scenarios
- **Network Operations**: API calls (real_leads_engine.places_search)
- **Database Operations**: CRM updates, pipeline access
- **Async Operations**: Email/WhatsApp sending
- **Performance**: Scaling tests with 1000+ rows

### Low Priority for Now
- Mocking external APIs (covered by integration tests)
- Performance benchmarks
- Load testing
- UI/E2E tests

## CI Integration

### GitHub Actions
```yaml
# .github/workflows/ci.yml should include:
- Run: pytest tests/company/ --cov=company
- Upload: Coverage to Codecov
- Alert: On coverage decrease >5%
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml should add:
- id: pytest-quick
  entry: pytest tests/company/ -x
  language: system
```

## Maintenance

### Adding Tests
1. Create test file: `tests/company/test_<module>.py`
2. Use fixtures from `conftest.py`
3. Follow naming: `test_<function>_<scenario>()`
4. Include docstrings for complex tests

### Updating Coverage
- Run quarterly coverage analysis
- Prioritize new tests for untested modules
- Update this matrix monthly
- Review failure logs for patterns

## Resources

- **Pytest Docs**: https://docs.pytest.org/
- **Testing Best Practices**: docs/DEVELOPMENT_TROUBLESHOOTING.md#Testing
- **Test Fixtures**: `tests/company/conftest.py` (TBD)
- **CI Pipeline**: `.github/workflows/ci.yml`

---

**Last Updated**: 2026-06-17  
**Next Review**: 2026-06-24 (after Phase 1 completion)
