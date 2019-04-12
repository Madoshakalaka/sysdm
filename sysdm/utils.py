import subprocess


def get_output(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, _) = proc.communicate()
    return out.decode().strip()


def is_unit_running(unit):
    return get_output('systemctl is-active {unit}'.format(unit=unit)) == "active"


def is_unit_enabled(unit):
    return get_output('systemctl is-enabled {unit}'.format(unit=unit)) == "enabled"


def read_command_from_unit(systempath, service_name):
    with open(systempath + "/" + service_name + ".service") as f:
        for line in f.read().split("\n"):
            if line.startswith("ExecStart="):
                return line[10:].strip()


def read_ps_aux_by_unit(systempath, unit):
    cmd = read_command_from_unit(systempath, unit)
    z = get_output("ps ax -o pid,%cpu,%mem,ppid,thcount,args -ww")

    for num, line in enumerate(z.split("\n")):
        if num == 0:
            continue
        pid, cpu, mem, ppid, thcount, *rest = line.split()
        if ppid != "1":
            continue
        rest = " ".join(rest)
        if cmd.endswith(rest) or rest.endswith(cmd):
            return pid, cpu, mem, thcount
