import subprocess, sys

COMMANDS = [
    [sys.executable, 'scripts/dealix_v13_master_readiness.py'],
    [sys.executable, 'scripts/dealix_launch_decision_report.py'],
    [sys.executable, 'scripts/dealix_workflow_inventory.py'],
    [sys.executable, 'scripts/dealix_migration_order_check.py'],
]

def main():
    for cmd in COMMANDS:
        print(f'\n$ {" ".join(cmd)}')
        subprocess.run(cmd, check=True)
    print('\nOK: Dealix V13 daily consolidation run complete')

if __name__ == '__main__':
    main()
