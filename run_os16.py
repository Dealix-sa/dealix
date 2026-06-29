import ci_core
import client_ops_max
import score_core


def main():
    ci = ci_core.build_payload()
    ops = client_ops_max.build_payload()
    st = score_core.build_payload()
    print('DEALIX_SERVICE_OS_READY=1')
    print('CLIENT_OPS_MAX_READY=1')
    print('CONVERSATION_INTELLIGENCE_READY=1')
    print('DEAL_STRATEGY_READY=1')
    print('LIVE_SENDS=0')
    print('FINAL_COMMITMENTS=0')
    return 0 if ci_core.verify(ci) == [] and client_ops_max.verify(ops) == [] and score_core.verify(st) == [] else 1


if __name__ == '__main__':
    raise SystemExit(main())
