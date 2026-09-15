# Performance Testing

## Scenario

Locust simulates employees who register/login, retrieve services, retrieve requests, and create service requests.

## How To Run

```bash
locust -f tests/performance/locustfile.py --headless -u 5 -r 1 -t 1m --host http://localhost:8000
```

## Acceptance Criteria

- HTTP failure rate remains below the project-defined smoke threshold.
- No endpoint consistently times out under small local smoke load.
- Results are treated as local observations only, not production capacity claims.

## Results

Not executed in this environment during this implementation pass because the integrated Docker/runtime services were not available here.

## Limitations

Local runs depend on workstation resources, seed data, database state, and network conditions. Use these results for regression signals, not sizing.
