#!/home/kels/Documents/projects/netAutomation/autoMate/test_napalm/bin/python3

import sys,ansible_runner #ansible_playbook_runner was initially used



def index():
    out, err, rc = ansible_runner.run_command(
        executable_cmd='ansible-playbook',
        cmdline_args=[
            '/home/kels/Documents/projects/netAutomation/autoMate/ansible_test/playbook.yaml',
            '-i',
            '/home/kels/Documents/projects/netAutomation/autoMate/ansible_test/host.yml',
            # '-vvvv',
            # '-k',
            # '-e',
            # 'ansible_sudo_pass="admin"',
        ],
        json_mode=True,
        quiet=True,
        # passwords=['admin']
        # finished_callback
        # cancel_callback
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        # error_fd=sys.stderr,
    )
    print("rc: {}".format(rc))
    print("out: {}".format(out))
    print("err: {}".format(err))


if __name__ == '__main__':
    #sys.argv = ["programName.py","--input","test.txt","--output","tmp/test.txt"]
    index()